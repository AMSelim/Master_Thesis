import multiprocessing
import threading
import numpy as np
from src.utils.data_class import DataClass, MetaDataClass


class DataHandler(threading.Thread):
    def __init__(self, participant_id: int, eeg_queue: multiprocessing.Queue, data_queue):
        super().__init__()
        self.counter = 1
        self.participant_id = participant_id
        self.eeg_queue = eeg_queue
        self.data_queue = data_queue
        self.speech_type = None
        self.end_of_level = 0

    def handle_data(self):
        while True:
            if not self.eeg_queue.empty():
                data = self.eeg_queue.get()
                eeg_data = data[0]
                label = data[1]
                print(eeg_data.shape)
                if isinstance(label, str):
                    speech_type = self.speech_type
                    speech_label = label
                else:
                    speech_type = label.speech_type
                    speech_label = label.speech_label
                    self.end_of_level = label.end_of_level
                    self.speech_type = speech_type

                meta_data = MetaDataClass(channels=eeg_data.shape[0], number_of_samples=eeg_data.shape[1],
                                          participant_id=self.participant_id)
                data = np.ndarray.tobytes(eeg_data)
                generated_data_2 = DataClass(eeg_data=data, speech_type=speech_type, speech_label=speech_label,
                                             meta_data=meta_data, end_of_level=self.end_of_level)
                self.data_queue.put(generated_data_2)
                print("Data Pushed")
                self.counter += 1

    def run(self) -> None:
        self.handle_data()
