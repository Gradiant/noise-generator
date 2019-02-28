from flask import Flask, jsonify, request, render_template
from noise_generator import Noise
import logging
import os

app = Flask(__name__)

parallel = os.getenv('PARALLEL', 10)

noises_dict = dict()
noise_current_id = 0

@app.route('/api/noises', methods=['GET'])
def get_noises():
    return jsonify({'noises': list([noises_dict[endpoint].as_dict() for endpoint in noises_dict.keys()])})


@app.route('/api/noises/<nose_id>', methods=['GET'])
def get_noise(noise_id):
    noise_id = int(noise_id)
    if noise_id in noises_dict:
        return jsonify(noises_dict[noise_id].as_dict())
    else:
        return 'Endpoint noise {} not found'.format(noise_id), 404

@app.route('/api/noises', methods=['POST'])
def post_noise():
    global noise_current_id
    noise_id = noise_current_id
    noise_current_id = noise_current_id + 1
    json_request = request.get_json()
    logging.debug('post noise -> {}'.format(json_request))
    endpoint_ip = json_request['endpoint_ip']
    endpoint_port = json_request.get('endpoint_port', 5201)
    bw = json_request.get('bw', None)
    timeout = json_request.get('timeout', None)
    noise = Noise(noise_id, endpoint_ip, endpoint_port, bw, timeout, parallel)
    noises_dict[noise_id] = noise
    return jsonify(noise.as_dict())


@app.route('/api/noises/<noise_id>/stop', methods=['POST'])
def stop_noise(noise_id):
    noise_id = int(noise_id)
    if noise_id in noises_dict:
        noise = noises_dict[noise_id]
        noise.stop()
        return '', 200
    else:
        return 'Endpoint Noise {} not found'.format(noise_id), 404

@app.route('/api/noises/<noise_id>', methods=['DELETE'])
def delete_noise(noise_id):
    noise_id = int(noise_id)
    if noise_id in noises_dict:
        noise = noises_dict[noise_id]
        noise.stop()
        noises_dict.pop(noise_id)
        return '', 200
    else:
        return 'Endpoint Noise {} not found'.format(noise_id), 404


@app.route('/')
def index():
    return render_template('index.html')


logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.getLevelName('DEBUG'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
