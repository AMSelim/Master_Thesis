import numpy as np
import pandas as pd
import pywt
import threading
import multiprocessing
from sklearn import svm, preprocessing
from src.utils.data_class import ProcessingDataClass


class Processing(multiprocessing.Process):
    def __init__(self, processing_input_queue: multiprocessing.Queue):
        super().__init__()
        self.silent_feature_queue: "multiprocessing.Queue[tuple]" = multiprocessing.Queue()
        self.counter = 0
        self.overt_feature_vectors = None
        self.classifier = None
        self.processing_input_queue = processing_input_queue
        self.label_encoder = preprocessing.LabelEncoder()
        self.label_encoder.fit(["up", "left", "right", "pick", "push"])

    def feature_extraction(self, data: pd.Series) -> []:
        wp = pywt.WaveletPacket(data=data, wavelet="sym7", mode='symmetric', maxlevel=5)
        levels = wp.get_level(5, order="natural")
        result_pdf = pd.DataFrame()
        x = 0
        for node in levels:
            data_wp = node.data
            result_pdf[x] = data_wp
            x += 1
        feature_mean = result_pdf.mean()
        feature_std = result_pdf.std()
        feature_var = result_pdf.var()
        feature_kurtosis = result_pdf.kurtosis()
        feature_skewness = result_pdf.skew()
        feature_avg_energy = result_pdf.pow(2).sum(axis=0) / result_pdf.shape[0]
        # Zero-crossing function
        #   Source: https://tsfel.readthedocs.io/en/latest/_modules/tsfel/feature_extraction/features.html#zero_cross
        feature_zero_crossing_rate = result_pdf.apply(lambda i: len(np.where(np.diff(np.sign(i)))[0]), axis=0)
        extracted_features_array = np.concatenate((feature_mean.values, feature_std.values,
                                                   feature_var.values, feature_kurtosis.values,
                                                   feature_skewness.values, feature_avg_energy,
                                                   feature_zero_crossing_rate)).tolist()
        return extracted_features_array

    def classification(self, silent_features, label, participant_id):
        if self.classifier is None:
            self.classifier = svm.SVC()
            self.classifier.fit(self.overt_feature_vectors[:, :-1], self.overt_feature_vectors[:, -1])
            print("Classifier Was None!")
        file_name = f"./results/results_{participant_id}.txt"
        predicted_speech_label = self.classifier.predict(silent_features)
        try:
            expected_speech_label = label
            predicted_speech_label_1 = int(predicted_speech_label[0].split('.')[0])
            result = f"Expected Label: {self.label_encoder.inverse_transform([expected_speech_label])}" \
                     f", Predicted Label: " \
                     f"{self.label_encoder.inverse_transform([predicted_speech_label_1])} \n"
        except Exception:
            print(Exception)
            result = f"Expected Label: {label}" \
                     f", Predicted Label: " \
                     f"{predicted_speech_label} \n"
        print(result)
        with open(file_name, "a") as text_file:
            text_file.write(result)

    def data_handling(self, data: ProcessingDataClass):
        pandas_data_frame = pd.DataFrame(data.eeg_data)
        pandas_data_frame = pandas_data_frame.iloc[:-3, :]
        speech_type = data.speech_type
        speech_label = data.speech_label.lower()
        end_of_level = data.end_of_level
        pandas_features = pandas_data_frame.apply(func=self.feature_extraction, axis="columns")
        feature_list = pandas_features.to_list()
        feature_array = np.asarray(feature_list).flatten()
        print("Features Extracted")
        if speech_label != "empty":
            print(speech_label)
            speech_label = self.label_encoder.transform([speech_label])
            if speech_type.lower() == "overt":
                if self.overt_feature_vectors is None:
                    self.overt_feature_vectors = np.append(feature_array, speech_label)
                    self.overt_feature_vectors = np.reshape(self.overt_feature_vectors,
                                                            (1, self.overt_feature_vectors.shape[0]))
                else:
                    feature_label_array = np.append(feature_array, speech_label)
                    feature_label_array = np.reshape(feature_label_array, (1, feature_label_array.shape[0]))
                    self.overt_feature_vectors = np.append(self.overt_feature_vectors, feature_label_array, axis=0)
                if end_of_level == 2:
                    print("Classifier Training in Progress")
                    self.classifier = svm.SVC()
                    self.classifier.fit(self.overt_feature_vectors[:, :-1], self.overt_feature_vectors[:, -1])
                    print("Classifier Ready")
            elif speech_type.lower() == "silent":
                feature_array = np.reshape(feature_array, (1, feature_array.shape[0]))
                self.classification(feature_array, speech_label, data.participant_id)

    def listener(self):
        print("Processing Queue Listening")
        while True:
            if not self.processing_input_queue.empty():
                print("Message Received")
                incoming_data = self.processing_input_queue.get()
                processing_thread = threading.Thread(target=self.data_handling, args=(incoming_data, ))
                processing_thread.start()

    def run(self):
        print("Processing Started")
        self.listener()
