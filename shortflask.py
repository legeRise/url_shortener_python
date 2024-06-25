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
    return render_template('short.html',short_url=short_url)



@app.route('/<short_url>')
def download(short_url):
    if os.path.exists('shortened_urls.json'):
        with open('shortened_urls.json') as file:
            db = json.load(file)
        long_url = db.get(short_url)
        if long_url:
            return redirect(long_url)
        else:
            return "Error: URL not found in database", 404
    else:
        return "Error: URL database not found", 404




if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=9200)
