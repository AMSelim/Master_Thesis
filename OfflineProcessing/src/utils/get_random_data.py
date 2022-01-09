import random
import numpy as np
from typing import List


def get_random_data(data: List[np.ndarray], number_per_class: int = 20) -> np.ndarray:
    """
    :param data: A list of arrays of shape: (Number_Of_Epochs, Number_Of_Channels, Number_Of_Samples)
    :param number_per_class: Number of random epochs per class
    :return: A single array of shape: (Number_Of_Epochs, Number_Of_Channels, Number_Of_Samples)
    """
    random_data_list = []
    for i in range(len(data)):
        random_data_list += random.choices(random.sample(list(data[i]), len(data[i])), k=number_per_class)
    random_data_array = np.asarray(random_data_list)
    return random_data_array
