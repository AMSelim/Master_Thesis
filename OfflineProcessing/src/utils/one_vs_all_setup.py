import numpy as np
from typing import List
from src.utils.get_random_data import get_random_data
from src.utils.data_classes import OneVsAll


def setup(data: List[np.ndarray], number_per_random_class: int = 20) -> List[OneVsAll]:
    result_pairs = []
    for i in range(len(data)):
        intermediate_data = data.copy()
        main_class = intermediate_data.pop(i)
        random_class = get_random_data(data=intermediate_data, number_per_class=number_per_random_class)
        main_labels = [i for _ in range(len(main_class))]
        random_labels = [7 for _ in range(len(random_class))]
        result = OneVsAll(main_class=main_class, random_class=random_class,
                          main_labels=main_labels, random_labels=random_labels)
        result_pairs.append(result)
    return result_pairs
