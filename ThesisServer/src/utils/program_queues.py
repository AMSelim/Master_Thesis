"""
    #   I am using queue.Queue() instead of collections.deque() because of stability issues and
        make sure they are thread safe.
"""
import queue
from multiprocessing import Queue
from src.utils.data_class import ProcessingDataClass

repository_write_queue = queue.Queue()
processing_input_queue: "Queue[ProcessingDataClass]" = Queue()
input_queue = queue.Queue()
output_queue = queue.Queue()
