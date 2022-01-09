import warnings
import numpy as np
import antropy as ant
from typing import Tuple, List
from sklearn.preprocessing import normalize
from scipy.stats import skew, kurtosis
import pyeeg
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)


def statistical_features(row: np.ndarray, sampling_frequency: float) -> list:
    """Source: https://github.com/forrestbao/pyeeg"""
    bands = [0.5, 4, 7, 12, 30]
    """Power Spectral Intensity"""
    psi, power_ratio = pyeeg.bin_power(X=row, Band=bands, Fs=sampling_frequency)
    """Hjorth parameters: Hjorth mobility & complexity"""
    hjorth = pyeeg.hjorth(row)
    """Approximate Entropy"""
    approximate_ent = ant.app_entropy(row)
    """Petrosian Fractal Dimension"""
    pfd = pyeeg.pfd(row)
    """Higuchi Fractal Dimension"""
    """ Source for Kmax"""
    """  - https://www.researchgate.net/post/Is-there-any-algorithm-to-select-the-K-max-in-Higuchis-Fractal-dimension"""
    hfd = pyeeg.hfd(X=row, Kmax=6)
    """Spectral Entropy"""
    spectral_ent = pyeeg.spectral_entropy(X=row, Band=bands, Fs=sampling_frequency, Power_Ratio=power_ratio)
    """Skewness"""
    skewness = skew(row)
    """Detrended Fluctuation Analysis"""
    dfa = pyeeg.dfa(row)
    """Hurst Exponent"""  # Gives an error
    # hurst = pyeeg.hurst(row)
    """Kurtosis"""
    kurt = kurtosis(row)
    feature_vector = list(psi) + list(hjorth)
    for feature in [approximate_ent, pfd, hfd, spectral_ent, skewness, dfa, kurt]:
        feature_vector.append(feature)
    return feature_vector


def extract_features(data: List[np.ndarray], sampling_frequency: float) -> Tuple[List[np.ndarray], List[int]]:
    """Source: https://ieeexplore.ieee.org/document/9061628"""
    data_array = np.concatenate((data[0], data[1], data[2], data[3], data[4]), axis=0)
    statistical_features_array = np.apply_along_axis(func1d=statistical_features, arr=data_array,
                                                     axis=-1, sampling_frequency=sampling_frequency)
    statistical_features_list = [normalize(X=item, axis=0).flatten() for item in statistical_features_array]
    # Create Labels
    labels = []
    for i in range(len(data)):
        label = [i for _ in range(data[i].shape[0])]
        labels += label
    return statistical_features_list, labels
