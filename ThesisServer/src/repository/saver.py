import yaml
import joblib
import numpy as np
from dataclasses import asdict
from mongo_repository import MongoRepository

"""
This Code reads the data from the Mongo Database and converts it to a python dictionary for later use, 
by saving it as a joblib file. Because it is easier to access afterwards for processing in other projects. 
"""
participant_id = 1

with open("../../documents/config.YAML", "r") as file:
    cfg = yaml.load(file, Loader=yaml.FullLoader)
repository_parameters = cfg['repository']
repository = MongoRepository(host=repository_parameters["host"], port=repository_parameters["port"],
                             db_name=port=repository_parameters["name"])
data = repository.read_data(db_name="thesis_repository", participant_id=f"{participant_id}")

x = data
y = []
for item in x:
    """
    Here we decode the eeg data from raw bytes to a numpy array 
    """
    data_dict = asdict(item)
    shape = (item.channels, item.sample_number)
    eeg_data_decoded = np.reshape(np.frombuffer(buffer=item.eeg_data, dtype=float), newshape=shape)
    data_dict['eeg_data'] = eeg_data_decoded
    y.append(data_dict)
joblib.dump(y, f"participant_{participant_id}.joblib")
