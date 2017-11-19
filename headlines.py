import feedparser
from flask import Flask
from flask import render_template
from flask import request
import time

app = Flask(__name__)

RSS_FEEDS = {'kosmo': 'http://www.kosmonautix.cz/rubrika/micro/feed/',
             'lupa': 'https://www.lupa.cz/rss/clanky/',
             'zive': 'https://www.zive.cz/rss/sc-47/',
             'root': 'https://www.root.cz/rss/zpravicky/'}


@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "kosmo"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    gen_time = time.strftime("%d-%m-%Y %H:%M:%S")
    return render_template("home.html",
                           site=feed['feed'],
                           gen_time=gen_time,
                           articles=feed['entries'])


if __name__ == '__main__':
    app.run(host='192.168.240.237', port=5000, debug=True)
