import multiprocessing

import flask
from flask import request
import json
from src.utils.data_class import LabelDataClass

global labels_queue
app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    json_data = json.loads(request.data)
    label_list = json_data["Value"].split('_')
    data_label_information = LabelDataClass(speech_type=label_list[0],
                                            speech_label=label_list[1],
                                            end_of_level=int(label_list[2]))
    labels_queue.put(data_label_information)
    status_code = flask.Response(status=200)
    return status_code


def flask_main(label_queue: multiprocessing.Queue):
    global labels_queue
    labels_queue = label_queue
    app.run(host="0.0.0.0", port="5005")
