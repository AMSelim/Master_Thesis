import logging
import yaml
from src.repository.mongo_repository import MongoRepository
from src.adapters.grpc_server import DataStreamHandlerServicer
from src.processing.data_handler import UseCase
from src.processing.processing import Processing
from src.utils.program_queues import processing_input_queue


def main():
    logging.basicConfig()
    with open("../documents/config.YAML", "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    grpc_port = cfg['grpc']['port']
    repository_parameters = cfg['repository']
    server = DataStreamHandlerServicer(port=grpc_port)
    repository = MongoRepository(host=repository_parameters['host'],
                                 port=repository_parameters['port'],
                                 db_name=repository_parameters['name'])
    # NOTE: multiprocessing.Queue() needs to be passed as a parameter, otherwise it didn't work as expected.
    processing = Processing(processing_input_queue=processing_input_queue)
    processing.start()
    use_case = UseCase(processing_input_queue=processing_input_queue)
    server.start()
    repository.start()
    use_case.start()


if __name__ == '__main__':
    main()
