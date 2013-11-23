from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def homepage():
	return 'homepage!'

@app.route('/<post_name>.html')
def post(post_name):
	return render_template('posts.html', post_name=post_name)

if __name__ == '__main__':
	app.run()