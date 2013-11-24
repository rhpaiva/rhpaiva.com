from flask import Flask
from flask import render_template
import re as regexp
import os.path

app = Flask(__name__)

supported_languages = set(['pt', 'en', 'de'])
post_file           = 'posts/%(lang)s/%(post)s.html'

@app.route('/')
def home():
    return render_template('home.html')

# TODO: we should really create "catchers" for each param here instead of
# checking them inside the function
@app.route('/<language>/<post_name>.html')
def post(language, post_name):
    return render_post(language, post_name)

def render_post(language, post_name):
    is_valid_name     = regexp.search('^[0-9\-\_a-z]+$', post_name)
    is_valid_language = language in supported_languages
    path              = post_file % {'lang': language, 'post': post_name}

    if (
        not is_valid_name or 
        not is_valid_language or
        not file_exists('templates/' + path)
    ):
        return render_template('404.html'), 404

    return render_template(path, post_name = post_name, language = language)


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
    #app.run(debug=True)
    app.run()