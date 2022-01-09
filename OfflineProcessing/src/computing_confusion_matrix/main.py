"""
This code is made to display and save certain confusion matrices for the participants.
"""

import yaml as yaml
import numpy as np
from src.preprocessing.read_data import read_data
from src.preprocessing.filter_data import filter_data
from src.utils.one_vs_all_setup import setup
from src.feature_extraction.common_spatial_patterns_features import extract_features as extract_csp_features
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from typing import List


def write_results(true_labels, predicted_labels, results_file_path, participant_id, speech_type, fold_id, process_type):
    accuracy = accuracy_score(y_true=true_labels, y_pred=predicted_labels)
    cm = confusion_matrix(y_true=true_labels, y_pred=predicted_labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=["up", "left", "right", "pick", "push"])
    disp.plot()
    plt.savefig(f"../../results/specific_results/{speech_type}/{process_type}_participant_{participant_id}_{fold_id}.png")
    with open(results_file_path, "a") as text_file:
        text_file.write(f"{accuracy}\t")


def classify_data(training_data_list: List[np.ndarray], training_labels_list: List[int],
                  testing_data_list: List[np.ndarray], testing_labels_list: List[int],
                  results_file_path: str, classifier_id: int, participant_id: int, speech_type: str, fold_id: int,
                  process_type):
    if classifier_id == 1:
        clf = SVC(gamma="auto", kernel="rbf", probability=True, random_state=0)
    elif classifier_id == 2:
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    elif classifier_id == 3:
        clf = RandomForestClassifier(random_state=0)
    elif classifier_id == 4:
        clf = RandomForestClassifier(random_state=0, n_estimators=450)
    elif classifier_id == 5:
        clf = RandomForestClassifier(random_state=0, criterion="entropy")
    elif classifier_id == 6:
        clf = RandomForestClassifier(random_state=0, n_estimators=50)
    elif classifier_id == 7:
        clf = RandomForestClassifier(random_state=0, n_estimators=300)
    else:
        clf = KNeighborsClassifier(n_neighbors=7)
    clf.fit(X=training_data_list, y=training_labels_list)
    predicted_labels = clf.predict(testing_data_list)
    write_results(true_labels=testing_labels_list, predicted_labels=predicted_labels, results_file_path=results_file_path,
                  participant_id=participant_id, speech_type=speech_type, fold_id=fold_id, process_type=process_type)
    with open(results_file_path, "a") as text_file:
        text_file.write("\n")


def process_data(participant_id: int, notch_type: str, filter_type: str, components: int, classifier_id: int, process_type):
    events_dict: dict = {"Overt_Up": 11, "Overt_Left": 12, "Overt_Right": 13, "Overt_Pick": 14, "Overt_Push": 15,
                         "Silent_Up": 21, "Silent_Left": 22, "Silent_Right": 23, "Silent_Pick": 24, "Silent_Push": 25}
    sampling_frequency: float = 500.0
    montage_path = "../../documents/AC-64.bvef"
    with open("../../documents/config.YAML", "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    fif_file_path: str = f"../../data/participant_{participant_id}.fif"
    results_file_path: str = f"../../results/specific_results/participant_{participant_id}.txt"
    data_to_delete: dict = cfg[f"participant_{participant_id}"]["data_to_delete"]
    channels_to_drop = cfg[f"participant_{participant_id}"]["channels_to_drop"]
    # Load Data
    overt_data, silent_data = read_data(fif_file_path=fif_file_path, events_dict=events_dict,
                                        data_to_delete=data_to_delete, montage_path=montage_path,
                                        channels_to_drop=channels_to_drop)
    # Filter Data
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
    """CSP Feature Extraction"""
    data_combinations = [[overt_data_pairs, silent_data_pairs_training_1, silent_data_pairs_testing_1],
                         [overt_data_pairs, silent_data_pairs_training_2, silent_data_pairs_testing_2],
                         [overt_data_pairs, silent_data_pairs_training_3, silent_data_pairs_testing_3],
                         [overt_data_pairs, silent_data_pairs_training_4, silent_data_pairs_testing_4]]
    """Classify Data"""
    fold_id = 1
    for data_instance in data_combinations:
        overt_training_pairs, silent_training_pairs, silent_testing_pairs = data_instance
        overt_data_list, overt_labels_list, silent_data_testing, silent_labels_testing = \
            extract_csp_features(data_pairs=overt_training_pairs, number_of_components=components,
                                 data_pairs_2=silent_testing_pairs)
        classify_data(training_data_list=overt_data_list, training_labels_list=overt_labels_list,
                      testing_data_list=silent_data_testing, testing_labels_list=silent_labels_testing,
                      results_file_path=results_file_path, participant_id=participant_id, classifier_id=classifier_id,
                      speech_type="transfer", fold_id=fold_id, process_type=process_type)
        silent_data_training, silent_labels_training, silent_data_testing, silent_labels_testing = \
            extract_csp_features(data_pairs=silent_training_pairs, number_of_components=components,
                                 data_pairs_2=silent_testing_pairs)
        classify_data(training_data_list=silent_data_training, training_labels_list=silent_labels_training,
                      testing_data_list=silent_data_testing, testing_labels_list=silent_labels_testing,
                      results_file_path=results_file_path, participant_id=participant_id, classifier_id=classifier_id,
                      speech_type="standard", fold_id=fold_id, process_type=process_type)
        fold_id += 1

    print("Participant Done")


if __name__ == '__main__':
    # ["iir_notch", "butter_notch"], ["a15", "maurice"]
    # 2: GB, 4: RF_450, 5: RF_entropy, 7: RF_300
    parameters = [[2, "butter_notch", "maurice",  6,  7, "transfer"],
                  [7, "iir_notch",     "a15",     7,  4, "transfer"],
                  [8, "butter_notch",  "maurice", 5,  4, "transfer"],
                  [9, "butter_notch",  "maurice", 6,  4, "transfer"],
                  [10, "iir_notch",    "a15",     5,  2, "transfer"],
                  [11, "iir_notch",    "a15",     4,  2, "transfer"],
                  [12, "butter_notch", "maurice", 11, 5, "transfer"],
                  [13, "butter_notch", "maurice", 7,  4, "transfer"],
                  [14, "butter_notch", "maurice", 4,  7, "transfer"],
                  [15, "butter_notch", "maurice", 6,  4, "transfer"],
                  [16, "butter_notch", "maurice", 9,  4, "transfer"],
                  [17, "iir_notch",    "a15",     11, 5, "transfer"],
                  [18, "iir_notch",    "a15",     6,  2, "transfer"],
                  [19, "butter_notch", "maurice", 4,  4, "transfer"],
                  [20, "iir_notch",    "a15",     4,  2, "transfer"],
                  [2,  "butter_notch", "maurice", 11, 4, "standard"],
                  [7,  "butter_notch", "maurice", 8,  4, "standard"],
                  [8,  "butter_notch", "maurice", 10, 4, "standard"],
                  [9,  "butter_notch", "maurice", 11, 4, "standard"],
                  [10, "butter_notch", "a15",     9,  4, "standard"],
                  [11, "butter_notch", "maurice", 12, 4, "standard"],
                  [12, "butter_notch", "maurice", 12, 4, "standard"],
                  [13, "butter_notch", "maurice", 12, 4, "standard"],
                  [14, "butter_notch", "maurice", 11, 4, "standard"],
                  [15, "butter_notch", "maurice", 11, 4, "standard"],
                  [16, "butter_notch", "maurice", 9,  4, "standard"],
                  [17, "iir_notch",    "a15",     4,  2, "standard"],
                  [18, "iir_notch",    "a15",     6,  2, "standard"],
                  [19, "butter_notch", "maurice", 5,  4, "standard"],
                  [20, "butter_notch", "maurice", 10, 4, "standard"]]
    for parameter in parameters:
        process_data(participant_id=parameter[0], notch_type=parameter[1], filter_type=parameter[2],
                     components=parameter[3], classifier_id=parameter[4], process_type=parameter[5])
