"""
    I am using queue.Queue() instead of collections.deque() because of stability issues and
    make sure they are thread safe in a way.
"""
import multiprocessing
from src.utils.data_class import LabelDataClass
data_queue = multiprocessing.Queue()
label_queue: "multiprocessing.Queue[LabelDataClass]" = multiprocessing.Queue()
eeg_queue = multiprocessing.Queue()
keyboard_queue = multiprocessing.Queue()
