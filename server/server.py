import select, subprocess, numpy
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

render_length = 2
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

@app.route("/<string:sess_id>/chunk/<int:counter>.<string:fmt>")
def chunk(sess_id, counter, fmt):
    if not sess_id in sessions: init_session(sess_id)
    sessions[sess_id].update_params({ "excitement": 0.9 })
    # if counter <= metadata[sess_id]["chunk_count"]:
    #     return Response(metadata[sess_id]["last_chunk"], mimetype=f"audio/{fmt}")
    
    args = request.args.to_dict()
    print(request.args.to_dict())
    if "duration_secs" in args:
        duration_secs = float(args["duration_secs"])
    else:
        duration_secs = render_length
    
    print(duration_secs)

    chunk = sessions[sess_id].render(duration_secs)
    data = encode(chunk, fmt=fmt)
    metadata[sess_id]["last_chunk"] = data
    metadata[sess_id]["chunk_count"] += 1
    return Response(data, mimetype=f"audio/{fmt}")

# @app.route("/<string:sess_id>/stream/index.<string:fmt>")
# def stream(sess_id, fmt):
#     if not sess_id in sessions:
#         sessions[sess_id] = adapt.Session(Main)
    
#     sessions[sess_id].update_params({ "excitement": 0.9 })

#     if "range" in request.headers:
#         print("Received range request")
#         chunk = sessions[sess_id].render(render_length)
#         data = encode(chunk, fmt=fmt, header=True)
#         return Response(data, mimetype=f"audio/{fmt}", status=206)

#     print("Not range request")
#     def generate():
#         end_time = datetime.now().timestamp()
#         is_first_run = True

#         while True:
#             curr_time = datetime.now().timestamp()
#             if (end_time - curr_time) > stream_buffer_secs: continue
#             chunk = sessions[sess_id].render(render_length)
#             yield encode(chunk, fmt=fmt, header=is_first_run)
#             is_first_run = False
#             end_time += render_length

#     return Response(generate(), mimetype=f"audio/{fmt}")

# def get_synthetic_audio(num_samples):
#     audio = numpy.random.rand(num_samples).astype(numpy.float32) * 2 - 1
#     assert audio.max() <= 1.0
#     assert audio.min() >= -1.0
#     assert audio.dtype == numpy.float32
#     return audio


# def response():
#     pipe = subprocess.Popen(
#         'ffmpeg -f f32le -acodec pcm_f32le -ar 24000 -ac 1 -i pipe: -f mp3 pipe:'
#         .split(),
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE)
#     poll = select.poll()
#     poll.register(pipe.stdout, select.POLLIN)
#     while True:
#         pipe.stdin.write(get_synthetic_audio(24000).tobytes())
#         while poll.poll(0):
#             yield pipe.stdout.readline()


@app.route("/<string:sess_id>/stream.mp3", methods=['GET'])
def stream(sess_id):
    if not sess_id in sessions:
        sessions[sess_id] = adapt.Session(Main)

    if "range" in request.headers:
        print("Received range request")
        chunk = sessions[sess_id].render(render_length)
        data = encode(chunk, 'mp3')
        return Response(data, mimetype=f"audio/mpeg", status=206)

    print("here")
    def generate():
        end_time = datetime.now().timestamp()
        print("Generating end time")
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