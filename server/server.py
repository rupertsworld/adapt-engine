from flask import Flask, Response, send_file, request
from flask_cors import CORS
from uuid import uuid4
from server.helpers import generate_header, bytes_from_audio, encode
from datetime import datetime
from app.main import Main
import adapt

app = Flask(__name__, static_folder="../www")
CORS(app, origins='*')

sessions = {}
generators = []

render_length = 0.5
sample_rate = 44100
stream_buffer_secs = render_length * 0.5
bits_per_sample = 32
channels = 2

@app.route("/initialize", methods=["POST"])
def init():
    sess_id = str(uuid4())
    sessions[sess_id] = adapt.Session(Main)
    return { "sess_id": sess_id }

@app.route("/<string:sess_id>/update", methods=["POST"])
def update(sess_id):
    params = request.get_json()
    sessions[sess_id].update_params(params)
    return "OK!"

@app.route("/stream/<string:sess_id>.<string:fmt>")
def stream(sess_id, fmt):
    if not sess_id in sessions:
        sessions[sess_id] = adapt.Session(Main)
    
    def generate():
        end_time = datetime.now().timestamp()
        is_first_run = True

        while True:
            curr_time = datetime.now().timestamp()
            if (end_time - curr_time) > stream_buffer_secs: continue
            chunk = sessions[sess_id].render(render_length)
            yield encode(chunk, fmt=fmt, header=is_first_run)
            is_first_run = False
            end_time += render_length

    return Response(generate(), mimetype=f"audio/{fmt}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)