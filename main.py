from flask import Flask, render_template, request, redirect, jsonify
import redis, base62

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
slug_prefix = 'slug_'
url_prefix = 'url_'


@app.route('/urls/<slug>')
def get_url(slug):
    url = r.hget(slug_prefix + slug, 'url')
    if url:
        r.hincrby(slug_prefix + slug, 'visited')
    return redirect(url)


@app.route('/urls')
def get_urls():
    return jsonify([{'url':r.hget(key,'url'),
                     'slug':key[len(slug_prefix):],
                     'visited':r.hget(key,'visited')}
                    for key in r.scan_iter(match=slug_prefix + '*')])


@app.route('/urls', methods=['POST'])
def post_url():
    data = request.get_json()
    slug = r.get(url_prefix + data['url'])
    if not slug:
        slug = base62.encode(r.incr('next_url_id'))
        r.hmset(slug_prefix + slug, {'url': data['url'], 'visited': 0})
        r.set(url_prefix + data['url'], slug)
    return jsonify({'url':data['url'], 'slug':slug})


if __name__ == "__main__":
    app.run(debug=True)








