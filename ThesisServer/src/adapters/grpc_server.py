import grpc
import threading
from concurrent import futures
import src.adapters.data_stream_handler_pb2 as data_stream_handler_pb2
import src.adapters.data_stream_handler_pb2_grpc as data_stream_handler_pb2_grpc
from src.utils.data_class import IncomingDataClass
from src.utils.program_queues import input_queue, output_queue


def extract_data(received_data: data_stream_handler_pb2.Data) -> IncomingDataClass:
    """
    :param received_data: This is the message Data defined in the proto file.
    :return: It is converted to a dataclass of type IncomingDataClass() which holds all the information
             regarding the data stream.
    """
    return_data = IncomingDataClass(eeg_data=received_data.value, speech_type=received_data.type,
                                    speech_label=received_data.label,
                                    channels=received_data.headset_information.channels,
                                    sample_number=received_data.headset_information.number_of_samples,
                                    participant_id=received_data.headset_information.participant_id,
                                    end_of_level=received_data.end_of_level)
    return return_data


class DataStreamHandlerServicer(data_stream_handler_pb2_grpc.DataStreamHandlerServicer, threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def exchange_eeg_data(self, request, context):
        """
        # This function is the implementation of exchange_overt_data rpc defined in the proto file.
        :param request: The received message of type Data defined in the proto file.
        :param context:
        :return: It returns an empty response of message type Param
        """
        input_data = extract_data(received_data=request)
        input_queue.put(input_data)
        return data_stream_handler_pb2.Param()

    def run(self) -> None:
        data_stream_handler_pb2_grpc.add_DataStreamHandlerServicer_to_server(
            DataStreamHandlerServicer(self.port), self.server)
        self.server.add_insecure_port(self.port)
        print("Server Started")
        self.server.start()
        self.server.wait_for_termination()
