
from flask import Flask, request, Response, jsonify
import json
import requests

app = Flask(__name__)

PORT_NUMBER=6910

# echo - for debugging
# vikunja - for vikunja

@app.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo_alone():
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

@app.route('/echo/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo_subpath(path):
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
# @app.route('/vikunja/', methods=['GET'])
# def vikunja_proxy():
#     response = {
#         "host": request.headers["Host"],
#         "url": request.url
#     }
#     return jsonify(response)

# @app.route('/vikunja/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def vikunja_proxy_subpath(subpath):
#     response = {
#         "url": request.url,
#         "subpath": "/"+subpath,
#     }
#     return jsonify(response)

@app.route('/vikunja/<path:path>', methods=['GET', 'POST'])
def vikunja_subpath(path):
    # 1. Forward the request to Vikunja
    resp = requests.request(
        method=request.method,
        url=f"http://vikunja:3456/{path}",  # /login, /api/v1/info, etc.
        headers={k:v for k,v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    
    # 2. Modify the response content
    content = resp.text.replace('href="/', 'href="/vikunja/') \
                      .replace('src="/', 'src="/vikunja/') \
                      .replace('url("/', 'url("/vikunja/')
    
    # 3. Modify redirect headers (if present)
    headers = dict(resp.headers)
    if 'Location' in headers:
        if headers['Location'].startswith('/'):
            headers['Location'] = f"/vikunja{headers['Location']}"
        elif headers['Location'].startswith('/vikunja'):
            # Prevent double "/vikunja/vikunja/"
            pass  # Do nothing
        else:
            headers['Location'] = headers['Location']  # Keep external URLs untouched
    
    # 4. Return the modified response to the client
    return Response(content, resp.status_code, headers)

@app.route('/vikunja/', methods=['GET', 'POST'])
def vikunja_alone():
    # 1. Forward the request to Vikunja
    resp = requests.request(
        method=request.method,
        url=f"http://vikunja:3456/",  # /login, /api/v1/info, etc.
        headers={k:v for k,v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    
    # 2. Modify the response content
    content = resp.text.replace('href="/', 'href="/vikunja/') \
                      .replace('src="/', 'src="/vikunja/') \
                      .replace('url("/', 'url("/vikunja/')
    
    # 3. Modify redirect headers (if present)
    headers = dict(resp.headers)
    if 'Location' in headers:
        if headers['Location'].startswith('/'):
            headers['Location'] = f"/vikunja{headers['Location']}"
        elif headers['Location'].startswith('/vikunja'):
            # Prevent double "/vikunja/vikunja/"
            pass  # Do nothing
        else:
            headers['Location'] = headers['Location']  # Keep external URLs untouched
                
    # 4. Return the modified response to the client
    return Response(content, resp.status_code, headers)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT_NUMBER)
