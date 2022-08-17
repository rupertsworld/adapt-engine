import select, subprocess, numpy, re
from flask import Flask, Response, send_file, request
from flask_cors import CORS
from uuid import uuid4
from server.helpers import encode
from datetime import datetime
from app.main import Main
import adapt

app = Flask(__name__, static_folder="../www")
CORS(app, origins='*')

sessions = {}
metadata = {}

render_length = 0.5
sample_rate = 44100
stream_buffer_secs = render_length * 0.5
bits_per_sample = 32
channels = 2

def init_session(sess_id):
    sessions[sess_id] = adapt.Session(Main)
    metadata[sess_id] = { "chunk_count": -1, "last_chunk": None }

@app.route("/initialize", methods=["POST"])
def init():
    sess_id = str(uuid4())
    init_session(sess_id)
    return { "sess_id": sess_id }

@app.route("/<string:sess_id>/update", methods=["POST"])
def update(sess_id):
    params = request.get_json()
    sessions[sess_id].update_params(params)
    return "OK"

@app.route("/<string:sess_id>/stream.mp3", methods=['GET'])
def stream(sess_id):
    if not sess_id in sessions:
        sessions[sess_id] = adapt.Session(Main)

    if "range" in request.headers and not re.search("bytes=[0-9]*-$", request.headers['range']):
        # This is a hack that handles range requests from Safari
        chunk = sessions[sess_id].render(render_length)
        data = encode(chunk, 'mp3')
        return Response(data, mimetype=f"audio/mpeg", status=206)

    def generate():
        end_time = datetime.now().timestamp()
        
        pipe = subprocess.Popen(
            'ffmpeg -f s16le -acodec pcm_s16le -ar 44100 -ac 2 -i pipe: -f mp3 pipe:'
            .split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        poll = select.poll()
        poll.register(pipe.stdout, select.POLLIN)

        while True:
            curr_time = datetime.now().timestamp()
            if (end_time - curr_time) > stream_buffer_secs: continue
            audio = sessions[sess_id].render(render_length)
            pipe.stdin.write(audio)
            print("render length", end_time)
            end_time += render_length
        
            while poll.poll(0):
                yield pipe.stdout.readline()
                
    return Response(
        generate(),
        headers={
            # NOTE: Ensure stream is not cached.
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
        },
        mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)