"""
    This code was not used in the actual application, that is why it is not mentioned nor documented.
    This code is separated from the rest on purpose.
    This code is used to collect timestamps for wrong words that the participants says during the data collection.
"""
import flask
from flask import render_template
import yaml
from datetime import datetime

global timestamp_file_name
app = flask.Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add_time')
def add_time():
    time_stamp = datetime.now().time().strftime("%H:%M:%S.%f") + "\n"
    with open(timestamp_file_name, "a") as text_file:
        text_file.write(time_stamp)
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    with open("../../documents/config.YAML", "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
    participant_id = cfg["participant"]["id"]
    timestamp_file_name = f"../../results/timestamps_{participant_id}.txt"
    app.run(host=cfg["flask"]["host"], port=cfg["flask"]["port"])
