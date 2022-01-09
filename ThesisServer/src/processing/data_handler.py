import multiprocessing
import threading
import numpy as np
from src.utils.program_queues import input_queue, repository_write_queue
from src.utils.data_class import IncomingDataClass, ProcessingDataClass


class UseCase(threading.Thread):
    def __init__(self, processing_input_queue: multiprocessing.Queue):
        super().__init__()
        self.processing_input_queue = processing_input_queue

    def reformat_data(self, received_data: IncomingDataClass) -> ProcessingDataClass:
        shape = (received_data.channels, received_data.sample_number)
        eeg_data_decoded = np.reshape(np.frombuffer(buffer=received_data.eeg_data, dtype=float), newshape=shape)
        reformatted_data = ProcessingDataClass(eeg_data=eeg_data_decoded,
                                               speech_type=received_data.speech_type,
                                               speech_label=received_data.speech_label,
                                               participant_id=received_data.participant_id,
                                               end_of_level=received_data.end_of_level)
        return reformatted_data

    def run(self):
        while True:
            if input_queue.empty() is False:
                data = input_queue.get()
                repository_write_queue.put(data)
                reformatted_data = self.reformat_data(data)
                self.processing_input_queue.put(reformatted_data)
