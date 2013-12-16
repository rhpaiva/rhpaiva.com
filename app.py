from flask import Flask
from flask import render_template

import json
import os.path
import locale

app = Flask(__name__)

supported_languages = set(['pt', 'en', 'de'])
page_file           = 'pages/%(lang)s/%(page)s.html'

@app.route('/')
@app.route('/<language>/')
def route_home(language = 'en'):
    is_valid_language = language in supported_languages

    if not is_valid_language:
        return render_template('404.html'), 404

    index = read_json('posts.json')['posts'][language]
    vars  = {'posts': index, 'format_datetime': format_datetime}

    return render_page(language, 'index', vars)

# TODO: we should really create "catchers" for each param here instead of
# checking them inside the function
@app.route('/<language>/<page_uri>.html')
def route_page(language, page_uri):
    return render_page(language, page_uri)

def render_page(language, page_uri, vars = {}):
    import re as regexp

    is_valid_name     = regexp.search('^[0-9\-\_a-z]+$', page_uri)
    is_valid_language = language in supported_languages
    path              = page_file % {'lang': language, 'page': page_uri}

    if (
        not is_valid_name or
        not is_valid_language or
        not file_exists('templates/' + path)
    ):
        return render_template('404.html'), 404

    i18n = read_json('i18n/' + language + '.json')

    # must cast to string otherwise we'll have a
    # ValueError: too many values to unpack
    locale_lang = str(i18n['locale']) + '.utf8'

    locale.setlocale(locale.LC_TIME, locale_lang)

    vars['language']        = language
    vars['format_datetime'] = format_datetime
    vars['uri']             = language + '/' + page_uri

    return render_template(path, lang = i18n, vars = vars)

def create_slug(string):
    import unicodedata

    string = string.replace('?', '').replace('!', '').replace(' ', '-').lower()
    string = unicode(string, 'utf-8')

    return ''.join(c for c in unicodedata.normalize('NFD', string)
            if unicodedata.category(c) != 'Mn')

def read_json(path):
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except Exception, e:
        raise e

    return data

def format_datetime(date, output_format, input_format = '%Y-%m-%d'):
    from datetime import datetime
    return datetime.strptime(date, input_format).strftime(output_format)

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
    # register the filter
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.run(debug = True, host='0.0.0.0')
    #app.run()