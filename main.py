from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
urls = {}
index = 0

@app.route('/urls/<slug>')
def get_url(slug):
	global urls
	return jsonify({'url':urls.get(slug), 'slug':slug})

@app.route('/urls')
def get_urls():
	global urls
	return jsonify([{'url':url, 'slug':slug} for slug, url in urls.items()])

@app.route('/urls', methods=['POST'])
def post_url():
	global urls, index
	data = request.get_json()
	urls[str(index)] = data['url']
	index += 1
	return jsonify({'url':data['url'], 'slug':str(index-1)})

if __name__ == "__main__":
	app.run(debug=True)