import mne
import numpy as np
from mne.decoding import CSP
from typing import Tuple, List, Union
from src.utils.data_classes import OneVsAll


def compute_features(number_of_components: int, fit_data: np.ndarray, fit_labels: np.ndarray,
                     transform_data: np.ndarray, transform_data_2: np.ndarray = None) -> \
        Union[List[np.ndarray], Tuple[List[np.ndarray], List[np.ndarray]]]:
    """
     - We fit the CSP on the data of the class of interest as one label along with the random data of the combination
       of the remaining classes as the other label.
     - Afterwards we only transform the data of interest.
     - If transform_data_2 is sent, then we transform it based on the already fitted csp.
    """
    csp = CSP(n_components=number_of_components, reg=None, log=None, norm_trace=False, transform_into='csp_space',
              component_order="mutual_info")
    mne.set_log_level(False)
    csp.fit(fit_data, fit_labels)
    csp_features_array = csp.transform(transform_data)
    csp_features_vectors = [data.flatten() for data in csp_features_array]
    if transform_data_2 is not None:
        csp_features_array_2 = csp.transform(transform_data_2)
        csp_features_vectors_2 = [data.flatten() for data in csp_features_array_2]
        return csp_features_vectors, csp_features_vectors_2
    else:
        return csp_features_vectors


def extract_features(data_pairs: List[OneVsAll], number_of_components: int, data_pairs_2: List[OneVsAll] = None) \
        -> Union[Tuple[List[np.ndarray], List[int]], Tuple[List[np.ndarray], List[int], List[np.ndarray], List[int]]]:
    """
    :param data_pairs: It contains 5 instances of type OneVsAll.
                       Each containing the main class and random class, data and labels.
    :param data_pairs_2: Same as data_pairs, but will be transformed based on the fitted csp on data_pairs
    :param number_of_components: Number of components for the CSP extraction
    :return: CSP data and labels, each as one list of Numpy Arrays.
    """
    data_list = []
    labels_list = []
    if data_pairs_2:
        data_list_2 = []
        labels_list_2 = []
        for data_instance_1, data_instance_2 in zip(data_pairs, data_pairs_2):
            """
            To extract the CSP features for each label
            """
            data_fit = np.concatenate((data_instance_1.main_class, data_instance_1.random_class), axis=0)
            labels_fit = np.reshape(np.asarray(data_instance_1.main_labels + data_instance_1.random_labels),
                                    (data_fit.shape[0],))
            features, features_2 = compute_features(number_of_components=number_of_components,
                                                    fit_data=data_fit,
                                                    fit_labels=labels_fit,
                                                    transform_data=data_instance_1.main_class,
                                                    transform_data_2=data_instance_2.main_class)
            data_list += features
            labels_list += data_instance_1.main_labels
            data_list_2 += features_2
            labels_list_2 += data_instance_2.main_labels
        return data_list, labels_list, data_list_2, labels_list_2
    else:
        for data_instance in data_pairs:
            """
            To extract the CSP features for each label
            """
            data_fit = np.concatenate((data_instance.main_class, data_instance.random_class), axis=0)
            labels_fit = np.reshape(np.asarray(data_instance.main_labels + data_instance.random_labels),
                                    (data_fit.shape[0],))
            features = compute_features(number_of_components=number_of_components,
                                        fit_data=data_fit,
                                        fit_labels=labels_fit,
                                        transform_data=data_instance.main_class)
            data_list += features
            labels_list += data_instance.main_labels
        return data_list, labels_list
