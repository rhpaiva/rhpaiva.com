from flask import Flask
from flask import render_template

import json
import re as regexp
import os.path

app = Flask(__name__)

supported_languages = set(['pt', 'en', 'de'])
post_file           = 'posts/%(lang)s/%(post)s.html'

@app.route('/')
def home():
    return render_template('index.html')

# TODO: we should really create "catchers" for each param here instead of
# checking them inside the function
@app.route('/<language>/<post_uri>.html')
def post(language, post_uri):
    return render_post(language, post_uri)

def render_post(language, post_uri):
    is_valid_name     = regexp.search('^[0-9\-\_a-z]+$', post_uri)
    is_valid_language = language in supported_languages
    path              = post_file % {'lang': language, 'post': post_uri}

    if (
        not is_valid_name or
        not is_valid_language or
        not file_exists('templates/' + path)
    ):
        return render_template('404.html'), 404

    i18n = read_json('i18n/pt.json')

    return render_template(path, 
            lang = i18n, 
            vars = {
                'post_uri': post_uri, 
                'language': language
            }
    )

def read_json(path):
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except Exception, e:
        raise e

    return data


# Using 'open' here to avoid a race condition. More on this:
# stackoverflow.com/questions/82831/how-do-i-check-if-a-file-exists-using-python
def file_exists(path):
    try:
        with open(path):
            return True
    except IOError:
        return False

@app.errorhandler(404)
def error_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True)
    #app.run()
