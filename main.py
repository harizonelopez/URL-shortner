from flask import Flask, render_template, request, redirect
import hashlib

app = Flask(__name__)
url_mapping = {}

def generate_short_url(url):
    hash_object = hashlib.sha256(url.encode())
    short_code = hash_object.hexdigest()[:8]
    return short_code

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get('url')
        short_code = generate_short_url(long_url)
        url_mapping[short_code] = long_url
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_original(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return 'URL not found'

if __name__ == '__main__':
    app.run(debug=True)
