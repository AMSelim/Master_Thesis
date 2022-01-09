import threading
import grpc
import src.adapters.data_stream_handler_pb2 as data_stream_handler_pb2
import src.adapters.data_stream_handler_pb2_grpc as data_stream_handler_pb2_grpc


class Client(threading.Thread):

    def __init__(self, server_url: str, data_queue):
        super().__init__()
        print("Client Started")
        self.channel = grpc.insecure_channel(server_url)
        self.stub = data_stream_handler_pb2_grpc.DataStreamHandlerStub(self.channel)
        self.api_data = None
        self.meta_data = None
        self.data_queue = data_queue

    def exchange_data(self):
        while True:
            try:
                if self.data_queue.empty() is False:
                    self.api_data = self.data_queue.get()
                    self.meta_data = \
                        data_stream_handler_pb2.MetaData(channels=self.api_data.meta_data.channels,
                                                         participant_id=self.api_data.meta_data.participant_id,
                                                         number_of_samples=self.api_data.meta_data.number_of_samples)
                    incoming_data = self.api_data
                    data = data_stream_handler_pb2.Data(value=incoming_data.eeg_data,
                                                        type=incoming_data.speech_type,
                                                        label=incoming_data.speech_label,
                                                        headset_information=self.meta_data,
                                                        end_of_level=incoming_data.end_of_level)
                    self.stub.exchange_eeg_data(data)
            except grpc.RpcError as error:
                print(error)

    def __silent_data_handler(self):
        silent_data = self.api_data
        data = data_stream_handler_pb2.Data(value=silent_data.eeg_data,
                                            type=silent_data.speech_type,
                                            label=silent_data.speech_label,
                                            headset_information=self.meta_data)
        yield data

    def run(self) -> None:
        self.exchange_data()
