from flask import Flask,render_template,request,redirect
import hashlib
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


url_database = {}

@app.route('/shortener',methods=['POST'])
def shortener():
    # long link is converted to short link
    long_url= request.form.get('long_url')
    unique_id = hashlib.sha256(long_url.encode()).hexdigest()
    short_url = unique_id[:8]
    
    # short links mapped to long links are saved in the json file
    data = json.load(open('shortened_urls.json', 'r')) if 'shortened_urls.json' in os.listdir() else {}
    data[short_url] = long_url


    json.dump(data, open('shortened_urls.json', 'w'), indent=4)    
    return render_template('short.html',short_url=f"http://127.0.0.1:5000/{short_url}")



@app.route('/<short_url>')
def download(short_url):
    with open('shortened_urls.json') as file:
        db = json.load(file)

        if db[short_url]:
            long_url = db[short_url]
            return redirect(long_url)
        else:
            return "Short URL not found", 404




if __name__ == '__main__':
    app.run(debug=True)
