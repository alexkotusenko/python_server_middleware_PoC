
from flask import Flask, request, Response, jsonify
import json
import requests

app = Flask(__name__)

PORT_NUMBER=6910

@app.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo():
    response = {
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.get_json(silent=True),
        "data": request.data.decode('utf-8')
    }
    return jsonify(response)

# vikunja
@app.route('/vikunja/', methods=['GET'])
def vikunja_proxy():
    response = {
        "host": request.headers["Host"],
        "url": request.url
    }
    return jsonify(response)

@app.route('/vikunja/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def vikunja_proxy_subpath(subpath):
    response = {
        "url": request.url,
        "subpath": "/"+subpath,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT_NUMBER)
