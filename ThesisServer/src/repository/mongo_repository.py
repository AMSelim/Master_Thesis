import pymongo
import threading
from datetime import datetime
from dacite import from_dict
from dataclasses import asdict
from src.utils.data_class import MongoReadDataClass
from src.utils.program_queues import repository_write_queue


class MongoRepository(threading.Thread):
    def __init__(self, host: str, port: int, db_name: str):
        super().__init__()
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.counter = 0

    def write_document(self):
        while True:
            if repository_write_queue.empty() is not True:
                data = repository_write_queue.get()
                collection = self.db[str(data.participant_id)]
                data_dict = asdict(data)
                data_dict["time_stamp"] = datetime.now().time().strftime("%H:%M:%S.%f")
                data_dict["data_id"] = self.counter
                collection.insert_one(data_dict)
                print(f"File{self.counter}Written")
                self.counter += 1

    def read_data(self, db_name: str, participant_id: str):
        db = self.client[db_name]
        collection = db[participant_id]
        result = []
        for doc in collection.find():
            document_dataclass = from_dict(data_class=MongoReadDataClass, data=doc)
            result.append(document_dataclass)
        return result

    def run(self):
        print("Entered Mongo Writer")
        self.write_document()
