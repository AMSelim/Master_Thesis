from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class OneVsAll:
    __slots__ = ["main_class", "random_class", "main_labels", "random_labels"]
    main_class: np.ndarray
    random_class: np.ndarray
    main_labels: List[int]  # []
    random_labels: List[int]
