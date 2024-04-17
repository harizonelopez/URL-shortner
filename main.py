from flask import Flask, render_template, request, redirect
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = "aladinh00-01montext"
url_mapping = {}

def generate_short_url(url):
    hash_object = hashlib.sha256(url.encode())
    short_code = hash_object.hexdigest()[:8]
    return short_code

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None  
    message_error = "OOPS!!, The URL is not found."
    if request.method == 'POST':
        long_url = request.form.get('long_url')  
        short_code = generate_short_url(long_url)
        url_mapping[short_code] = long_url
        short_url = request.host_url + 'shorten/' + short_code  

    return render_template('index.html', short_url=short_url, message_error=message_error)

@app.route('/shorten/<short_code>')  
def redirect_to_original(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return '404 ERROR!! URL not found'

@app.route('/history')
def history():
    error = request.args.get("message_error")
    return render_template("history.html", message_error=message_error)

if __name__ == "__main__":
    app.run(debug=True)
