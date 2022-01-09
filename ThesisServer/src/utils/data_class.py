from dataclasses import dataclass
import numpy as np


@dataclass
class IncomingDataClass:
    __slots__ = ["eeg_data", "speech_type", "speech_label", "channels", "sample_number", "participant_id",
                 "end_of_level"]
    eeg_data: bytes
    speech_type: str
    speech_label: str
    channels: int
    sample_number: int
    participant_id: int
    end_of_level: int


@dataclass
class ProcessingDataClass:
    __slots__ = ["eeg_data", "speech_type", "speech_label", "participant_id", "end_of_level"]
    eeg_data: np.array
    speech_type: str
    speech_label: str
    participant_id: int
    end_of_level: int


@dataclass
class SparkProcessingDataClass:
    __slots__ = ["eeg_data", "speech_type", "speech_label", "participant_id"]
    eeg_data: []
    speech_type: str
    speech_label: str
    participant_id: int


@dataclass
class MongoReadDataClass:
    __slots__ = ["eeg_data", "speech_type", "speech_label", "channels", "sample_number", "participant_id",
                 "time_stamp", "end_of_level", "data_id"]
    eeg_data: bytes
    speech_type: str
    speech_label: str
    channels: int
    sample_number: int
    participant_id: int
    time_stamp: str
    end_of_level: int
    data_id: int
