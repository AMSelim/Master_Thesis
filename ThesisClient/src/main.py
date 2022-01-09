import multiprocessing
import threading
import yaml
from src.eeg_api.eeg_api import eeg_data_api
from src.adapters.grpc_client import Client
from src.utils.flask_application import flask_main
from src.eeg_api.data_handler import DataHandler
from src.utils.queues import keyboard_queue, eeg_queue, label_queue, data_queue
from src.utils.keyboard_listener import KeyboardListen


if __name__ == '__main__':
    with open("../documents/config.YAML", "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    server_url = cfg['grpc']['host']
    participant_id = cfg['participant']['id']
    eeg_api = multiprocessing.Process(target=eeg_data_api, args=(participant_id,
                                                                 keyboard_queue,
                                                                 eeg_queue,
                                                                 label_queue))
    grpc_client = Client(server_url=server_url, data_queue=data_queue)
    data_handler = DataHandler(participant_id=participant_id,
                               eeg_queue=eeg_queue,
                               data_queue=data_queue)
    flask_thread = threading.Thread(target=flask_main, args=(label_queue, ))
    keyboard_thread = KeyboardListen(keyboard_queue=keyboard_queue)
    keyboard_thread.start()
    grpc_client.start()
    data_handler.start()
    flask_thread.start()
    eeg_api.start()
