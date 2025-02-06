
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


@app.route('/vikunja/<path:path>', methods=['GET', 'POST'])
def vikunja_subpath(path):

    # Exclude static assets from being processed by the middleware
    # if path.startswith('assets/') or path == 'favicon.ico':
    #     return requests.get(f"http://46.38.245.74:3456/{path}").content
    #if path.startswith(('assets/', 'images/', 'icons/')) or path.endswith(('.png', '.jpg', '.jpeg', '.ico', '.svg')):
    #    return requests.get(f"http://46.38.245.74:3456/{path}").content
    if path.startswith(('assets/', 'images/', 'icons/')) or path.endswith(('.png', '.jpg', '.jpeg', '.ico', '.svg')):
        r = requests.get(f"http://46.38.245.74:3456/{path}")
        # Copy the upstream content type (or fallback to 'application/octet-stream')
        content_type = r.headers.get('Content-Type', 'application/octet-stream')
        return Response(r.content, status=r.status_code, headers={'Content-Type': content_type})
    

    app.logger.info(f"🚨 /vikunja/{path} requested!")
    # 1. Forward the request to Vikunja

    headers = {k:v for k,v in request.headers.items() if k.lower() != 'host'}
    headers['Accept-Encoding'] = 'gzip, deflate'
    resp = requests.request(
        method=request.method,
        # url=f"http://vikunja:3456/{path}",  # /login, /api/v1/info, etc.
        # url=f"http://localhost:3456/{path}", 
        url=f"http://46.38.245.74:3456/{path}",
        #headers={k:v for k,v in request.headers if k.lower() != 'host'},
        headers=headers,
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
    headers['X-Flask-Handled'] = 'true'
    headers.pop('Content-Encoding', None)  # Remove Content-Encoding if present
    if 'Location' in headers:
        app.logger.info(f"🔍 Redirect detected: {headers['Location']}")  # Debugging output
        if headers['Location'].startswith('/'):
            headers['Location'] = f"/vikunja{headers['Location']}"
        elif headers['Location'].startswith('/vikunja'):
            app.logger.info("🚨 Prevented duplicate /vikunja/")
        else:
            headers['Location'] = headers['Location']  # Keep external URLs untouched
    
    # 4. Return the modified response to the client
    return Response(content, resp.status_code, headers)

@app.route('/vikunja/', methods=['GET', 'POST'])
def vikunja_alone():
    app.logger.info("🚨 /vikunja/ requested!")
    # 1. Forward the request to Vikunja
    headers = {k:v for k,v in request.headers.items() if k.lower() != 'host'}
    headers['Accept-Encoding'] = 'gzip, deflate'
    resp = requests.request(
        method=request.method,
        # url=f"http://vikunja:3456/",  # /login, /api/v1/info, etc.
        # url=f"http://localhost:3456/",
        url=f"http://46.38.245.74:3456",
        #headers={k:v for k,v in request.headers if k.lower() != 'host'},
        headers=headers,
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
    headers['X-Flask-Handled'] = 'true'
    if 'Location' in headers:
        app.logger.info(f"🔍 Redirect detected: {headers['Location']}")  # Debugging output
        if headers['Location'].startswith('/'):
            headers['Location'] = f"/vikunja{headers['Location']}"
        elif headers['Location'].startswith('/vikunja'):
            app.logger.info("🚨 Prevented duplicate /vikunja/")
        else:
            headers['Location'] = headers['Location']  # Keep external URLs untouched

    # 4. Return the modified response to the client
    return Response(content, resp.status_code, headers)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT_NUMBER, debug=True)
