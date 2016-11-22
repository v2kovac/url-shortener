from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.urls import url_fix
from urlparse import urlparse
import redis, base62

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
slug_prefix = 'slug_'
url_prefix = 'url_'


@app.route('/<slug>')
def redirect_url(slug):
    url = r.hget(slug_prefix + slug, 'url')
    if url:
        r.hincrby(slug_prefix + slug, 'visited')
        o = urlparse(url)
        if not o.scheme:
            url = 'http://' + url
    return redirect(url)


@app.route('/urls/<slug>')
def get_url(slug):
    url = r.hget(slug_prefix + slug, 'url')
    visited = r.hget(slug_prefix + slug, 'visited')
    return jsonify({'url': url, 'slug': slug, 'visited': visited})


@app.route('/urls')
def get_urls():
    return jsonify([{'url':r.hget(key,'url'),
                     'slug':key[len(slug_prefix):],
                     'visited':r.hget(key,'visited')}
                    for key in r.scan_iter(match=slug_prefix + '*')])


@app.route('/urls', methods=['POST'])
def post_url():
    data = request.get_json()
    url = url_fix(data['url'])
    slug = r.get(url_prefix + url)
    if not slug:
        slug = base62.encode(r.incr('next_url_id'))
        r.hmset(slug_prefix + slug, {'url': url, 'visited': 0})
        r.set(url_prefix + url, slug)
    return jsonify({'url': url, 'slug': slug})


if __name__ == "__main__":
    app.run(debug=True)








