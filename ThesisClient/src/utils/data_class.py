from dataclasses import dataclass


@dataclass
class MetaDataClass:
    __slots__ = ['channels', 'number_of_samples', 'participant_id']
    channels: int
    number_of_samples: int
    participant_id: int


@dataclass
class DataClass:
    __slots__ = ['eeg_data', 'speech_type', 'speech_label', 'meta_data', 'end_of_level']
    eeg_data: bytes
    speech_type: str
    speech_label: str
    meta_data: MetaDataClass
    end_of_level: int


@dataclass
class LabelDataClass:
    __slots__ = ['speech_type', 'speech_label', 'end_of_level']
    speech_type: str
    speech_label: str
    end_of_level: int  # 0: False, 1: True, 2: End of Paradigm
