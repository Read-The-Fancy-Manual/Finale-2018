from flask import Flask, json, render_template, request, redirect, url_for
import mysql.connector
import os
import socket

from allvars import ALL_VARS
from authorized import AUTHORIZED_VARS

flag = 'sigsegv{1s0l4t10n_mY_455}'
app = Flask(__name__)

def opendb():
    config = {
        'user': 'pdebugging',
        'password': 'yo2yoh4xoomah2xee2Hij6aiSh6oajee4Eecie0thoh3Xeithi',
        'host': 'db',
        'port': '3306',
        'database': 'ProductionDebugging'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    return (connection, cursor)

def closedb(connection, cursor):
    cursor.close()
    connection.close()

@app.route("/")
def main():
    return redirect(url_for('showSignUp'))

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signIn', methods=['POST'])
def signIn():
    print 'HIT'
    _name     = request.form.get('inputName')
    _password = request.form.get('inputPassword')
    _varset   = request.form.get('debugVar')
    _varval   = request.form.get('debugVal')

    if not _name or not _password:
        return json.dumps({'message': '<span>Some fields are missing</span>'})

    if _varset and _varval:
        if not _varset.replace("_", "").replace("-", "").isalnum():
            return json.dumps({'html': '<span>Set variable and value fields can only contain chars in [_\-0-9A-Za-z]</span>'})
        if not _varval.replace("_", "").replace("-", "").isalnum():
            return json.dumps({'html': '<span>Set variable and value fields can only contain chars in [_\-0-9A-Za-z]</span>'})
        if _varset in ALL_VARS and not _varset in AUTHORIZED_VARS or "global" in _varset.lower():
            return json.dumps({'html': '<span>Forbidden variable name!</span>'})
        if "--" in _varset or "--" in _varval:
            return json.dumps({'html': '<span>Comments are forbidden!</span>'})

    if not _name.isalnum() or not _password.isalnum():
        return json.dumps({'html': '<span>Name and password fields can only contain chars in [0-9A-Za-z]</span>'})

    if _name and _password:
        (connection, cursor) = opendb()

        if _varset and _varval:
            reqset = "SET @{} = '{}'"
            if _varset in AUTHORIZED_VARS:
                reqset = "SET @@session.{} = '{}'"
            cursor.execute(reqset.format(_varset, _varval))

        req = "SELECT * FROM tbl_user WHERE login='{}' AND password='{}'"
        cursor.execute(req.format(_name, _password))

        data = [(login, password) for (login, password) in cursor]
        closedb(connection, cursor)

        if len(data) != 0 and data[0][0] == 'admin':
            return json.dumps({'gg': 'GG! Flag: {}!'.format(flag)})
        else:
            return json.dumps({'error': 'No user found with these credentials.'})

@app.route('/signUp', methods=['POST'])
def signUp():
    _name     = request.form.get('inputName')
    _password = request.form.get('inputPassword')

    if not _name or not _password:
        return json.dumps({'message': '<span>Some fields are missing</span>'})

    if not _name.isalnum() or not _password.isalnum():
        return json.dumps({'html': '<span>Fields can only contain chars in [0-9A-Za-z]'})

    if _name and _password:
        (connection, cursor) = opendb()
        cursor.callproc("sp_createUser", [_name, _password])

        for result in cursor.stored_results():
            data = result.fetchall()

        closedb(connection, cursor)

        if len(data) is 0:
            return json.dumps({'message': 'User created successfully!'})
        else:
            return json.dumps({'error': str(data[0])})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001)
