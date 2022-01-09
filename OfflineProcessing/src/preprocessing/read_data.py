import mne
import numpy as np
from typing import Tuple, List


def read_data(events_dict: dict, fif_file_path: str, montage_path: str, data_to_delete: dict = None,
              channels_to_drop: List[str] = None) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    :param events_dict: In the form of {"Label": Event_ID}
    :param fif_file_path: Location in the file system
    :param montage_path: Location in the file system
    :param data_to_delete: In the form of {"Label": [Word_ID, Word_ID]}
        {"Overt_Up": [], "Overt_Left": [], "Overt_Right": [], "Overt_Pick": [], "Overt_Push": []}
    :param channels_to_drop: In the form of ["Channel_Name"]
    :return: arrays of shape: (Number_Of_Epochs, Number_Of_Channels, Number_Of_Samples)
    """
    try:
        raw = mne.io.read_raw_fif(fif_file_path)
    except Exception:
        print("\nCheck File Path")
        raise Exception
    """Set the montage"""
    montage = mne.channels.read_custom_montage(montage_path, head_size=0.085)
    raw.set_montage(montage)
    """Extract the events from the dataset"""
    raw_events = raw.info["events"]
    events = [event["list"].tolist() for event in raw_events]
    """Extract the epochs from the data with a 0.1 second overlap before and after the window"""
    """while applying a baseline correction"""
    epochs = mne.Epochs(raw, events, event_id=events_dict, tmin=-0.1, tmax=2.1, preload=True, baseline=(-0.1, 0))
    """In case of bad channels"""
    if channels_to_drop:
        epochs.drop_channels(channels_to_drop)
    """Extract event related data, and remove last three channels (Accelerometer channels)"""
    eeg_data = {event_key: np.delete(epochs[event_key].get_data(), [-3, -2, -1], axis=1)
                for event_key in events_dict.keys()}
    """Remove the mis-stated words during overt speech collection by ID"""
    if data_to_delete:
        overt_up = np.delete(eeg_data["Overt_Up"], data_to_delete["Overt_Up"], axis=0)
        overt_left = np.delete(eeg_data["Overt_Left"], data_to_delete["Overt_Left"], axis=0)
        overt_right = np.delete(eeg_data["Overt_Right"], data_to_delete["Overt_Right"], axis=0)
        overt_pick = np.delete(eeg_data["Overt_Pick"], data_to_delete["Overt_Pick"], axis=0)
        overt_push = np.delete(eeg_data["Overt_Push"], data_to_delete["Overt_Push"], axis=0)
    else:
        overt_up = eeg_data["Overt_Up"]
        overt_left = eeg_data["Overt_Left"]
        overt_right = eeg_data["Overt_Right"]
        overt_pick = eeg_data["Overt_Pick"]
        overt_push = eeg_data["Overt_Push"]
    silent_up = eeg_data["Silent_Up"]
    silent_left = eeg_data["Silent_Left"]
    silent_right = eeg_data["Silent_Right"]
    silent_pick = eeg_data["Silent_Pick"]
    silent_push = eeg_data["Silent_Push"]
    overt_data = [overt_up, overt_left, overt_right, overt_pick, overt_push]
    silent_data = [silent_up, silent_left, silent_right, silent_pick, silent_push]
    return overt_data, silent_data
