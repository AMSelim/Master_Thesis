import yaml as yaml
import numpy as np
from joblib import Parallel, delayed
from src.preprocessing.read_data import read_data
from src.preprocessing.filter_data import filter_data
from src.utils.one_vs_all_setup import setup
from src.feature_extraction.common_spatial_patterns_features import extract_features as extract_csp_features
from src.classification.classify import classify_data


def main(participant_id: int):
    events_dict: dict = {"Overt_Up": 11, "Overt_Left": 12, "Overt_Right": 13, "Overt_Pick": 14, "Overt_Push": 15,
                         "Silent_Up": 21, "Silent_Left": 22, "Silent_Right": 23, "Silent_Pick": 24, "Silent_Push": 25}
    sampling_frequency: float = 500.0
    montage_path = "../documents/AC-64.bvef"
    with open("../documents/config.YAML", "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    fif_file_path: str = f"../data/participant_{participant_id}.fif"
    results_file_path: str = f"../results/overt_vs_silent/participant_{participant_id}.txt"
    data_to_delete: dict = cfg[f"participant_{participant_id}"]["data_to_delete"]
    channels_to_drop = cfg[f"participant_{participant_id}"]["channels_to_drop"]
    # Load Data
    overt_data, silent_data = read_data(fif_file_path=fif_file_path, events_dict=events_dict,
                                        data_to_delete=data_to_delete, montage_path=montage_path,
                                        channels_to_drop=channels_to_drop)
    # Filter Data
    for notch_type, filter_type in zip(["iir_notch", "butter_notch"], ["a15", "maurice"]):
        with open(results_file_path, "a") as text_file:
            text_file.write(f"Filter {notch_type} {filter_type}\n")
        overt_data_filtered = [filter_data(notch_type=notch_type, filter_type=filter_type,
                                           sampling_frequency=sampling_frequency,
                                           overt_data=True, data=overt_class) for overt_class in overt_data]
        silent_data_filtered = [filter_data(notch_type=notch_type, filter_type=filter_type,
                                            sampling_frequency=sampling_frequency,
                                            overt_data=False, data=silent_class) for silent_class in silent_data]
        # Shuffle the data within each class
        rng = np.random.default_rng(seed=42)
        for data in silent_data_filtered:
            """
            Shuffles the data instance itself
            """
            rng.shuffle(data, axis=0)
        # Extract Features
        """Split Silent Data for CSP Extraction"""
        silent_testing_data_1 = [data[:20] for data in silent_data_filtered]
        silent_testing_data_2 = [data[20:40] for data in silent_data_filtered]
        silent_testing_data_3 = [data[40:60] for data in silent_data_filtered]
        silent_testing_data_4 = [data[60:] for data in silent_data_filtered]
        silent_training_data_1 = [data[20:] for data in silent_data_filtered]
        silent_training_data_2 = [np.concatenate((data[:20], data[40:]), axis=0) for data in silent_data_filtered]
        silent_training_data_3 = [np.concatenate((data[:40], data[60:]), axis=0) for data in silent_data_filtered]
        silent_training_data_4 = [data[:60] for data in silent_data_filtered]
        """Compute setup for feature extraction"""
        overt_data_pairs = setup(overt_data_filtered)
        silent_data_pairs_testing_1 = setup(silent_testing_data_1, number_per_random_class=5)
        silent_data_pairs_testing_2 = setup(silent_testing_data_2, number_per_random_class=5)
        silent_data_pairs_testing_3 = setup(silent_testing_data_3, number_per_random_class=5)
        silent_data_pairs_testing_4 = setup(silent_testing_data_4, number_per_random_class=5)
        silent_data_pairs_training_1 = setup(silent_training_data_1, number_per_random_class=15)
        silent_data_pairs_training_2 = setup(silent_training_data_2, number_per_random_class=15)
        silent_data_pairs_training_3 = setup(silent_training_data_3, number_per_random_class=15)
        silent_data_pairs_training_4 = setup(silent_training_data_4, number_per_random_class=15)
        """CSP Feature Extraction and Classification"""
        data_combinations = [[overt_data_pairs, silent_data_pairs_training_1, silent_data_pairs_testing_1],
                             [overt_data_pairs, silent_data_pairs_training_2, silent_data_pairs_testing_2],
                             [overt_data_pairs, silent_data_pairs_training_3, silent_data_pairs_testing_3],
                             [overt_data_pairs, silent_data_pairs_training_4, silent_data_pairs_testing_4]]
        for components in range(4, 13):
            for data_instance in data_combinations:
                overt_training_pairs, silent_training_pairs, silent_testing_pairs = data_instance
                overt_data_list, overt_labels_list, silent_data_testing, silent_labels_testing = \
                    extract_csp_features(data_pairs=overt_training_pairs, number_of_components=components,
                                         data_pairs_2=silent_testing_pairs)
                classify_data(training_data_list=overt_data_list, training_labels_list=overt_labels_list,
                              testing_data_list=silent_data_testing, testing_labels_list=silent_labels_testing,
                              results_file_path=results_file_path)
                silent_data_training, silent_labels_training, silent_data_testing, silent_labels_testing = \
                    extract_csp_features(data_pairs=silent_training_pairs, number_of_components=components,
                                         data_pairs_2=silent_testing_pairs)
                classify_data(training_data_list=silent_data_training, training_labels_list=silent_labels_training,
                              testing_data_list=silent_data_testing, testing_labels_list=silent_labels_testing,
                              results_file_path=results_file_path)
        print("Participant Half Done")
    print("Participant Done")


if __name__ == '__main__':
    Parallel(n_jobs=2)(delayed(main)(participant_id) for participant_id in [15, 16])
