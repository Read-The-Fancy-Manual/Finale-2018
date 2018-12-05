import os, hashlib
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

KEY = 0x57616e6e6120726561647a203f203e626574612e6861636b6e646f2e636f6d3c


app = Flask(__name__)


def encrypt(license):
    hashes = []
    for line in license:
        hashes.append(int(hashlib.sha256(line).hexdigest(), 16))
    if len(hashes) == 0:
        return 0
    return reduce((lambda x, y: x^y), hashes)
def check(license):
    if encrypt(license) == KEY:
        return 'sigsegv{X0R_c4n_be_misus3d__p3rte__}'
    else:
        return 'Wrong license file.'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        return check(file)
    return '''
    <!doctype html>
    <title>Feed me wid y0ur license !</title>
    <h1>Feed me wid y0ur license !</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <button type=submit value=Upload>Send dat b1tch!</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
