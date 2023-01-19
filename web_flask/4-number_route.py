#!/usr/bin/python3
"""The followiong scripts starts a Flask web application:"""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_hbnb():
    """Return  “Hello HBNB!” string when route quired"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hello_hbnb2():
    """Return a "HBNB" string when quired."""
    return "HBNB"


@app.route('/c/<text>')
def C_is_fun(text):
    """Returns string “C ” followed by the value of the text variable
    when quired"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python/')
@app.route('/python/<text>')
def python_is_cool(text='is cool'):
    """Return a string “Python ”, followed by the value of the text variable
    when quired"""
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>')
def is_it_number(n=None):
    """Return string  “n is a number” only if n is an integer"""
    return str(n) + ' is a number'

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
