import multiprocessing
import time
from EEGTools.Recorders.LiveAmpRecorder.liveamp_recorder import LiveAmpRecorder as Recorder
from src.utils.data_class import LabelDataClass


def eeg_data_api(participant_id: int, keyboard_queue: multiprocessing.Queue, eeg_queue: multiprocessing.Queue,
                 label_queue: multiprocessing.Queue):
    participant_id = participant_id
    keyboard_queue = keyboard_queue
    label_queue: "multiprocessing.Queue[LabelDataClass]" = label_queue
    eeg_queue = eeg_queue
    eeg_events = {"Empty": 1, "EndOfEvent": 2, "EndOfLevel": 3, "EndOfParadigm": 4, "space_bar": 5,
                  "Overt_Up": 11, "Overt_Left": 12, "Overt_Right": 13, "Overt_Pick": 14, "Overt_Push": 15,
                  "Silent_Up": 21, "Silent_Left": 22, "Silent_Right": 23, "Silent_Pick": 24, "Silent_Push": 25}
    end_of_level = 0
    recorder = Recorder()
    recorder.set_event_dict(eeg_events)
    recorder.connect()
    recorder.start_recording()
    print("Recorder Ready")
    while True:
        if not keyboard_queue.empty():
            condition = keyboard_queue.get()
            if (condition == "record") and (not label_queue.empty()):
                recorder.refresh()
                a = recorder.get_data().shape[1]
                recorder.set_event(eeg_events["space_bar"])
                time.sleep(2)
                if label_queue.empty():
                    label = "Empty"
                    event = eeg_events[label]
                else:
                    label = label_queue.get()
                    event = eeg_events[f"{label.speech_type}_{label.speech_label}"]
                    end_of_level = label.end_of_level
                recorder.refresh()
                recorder.set_event(event)
                time.sleep(2)
                recorder.refresh()
                eeg_data = recorder.get_data()[:, a:]
                eeg_queue.put((eeg_data, label))
                recorder.set_event(eeg_events["EndOfEvent"])
                if end_of_level == 1:
                    recorder.set_event(eeg_events["EndOfLevel"])
                elif (end_of_level == 2) or (end_of_level == 3):
                    recorder.set_event(eeg_events["EndOfParadigm"])
            elif condition == "quit":
                recorder.stop_recording()
                time.sleep(2)
                recorder.disconnect()
                recorder.save(f"participant_{participant_id}_eeg", "../eeg_samples/", save_additional=True)
        else:
            recorder.refresh()
            time.sleep(0.1)
