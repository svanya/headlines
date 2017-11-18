import feedparser
from flask import Flask
from flask import render_template
import time

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])


#     """<html>
#         <body>
#                 <h1>{0} Headlines </h1>
#                 <b>{1}</b> <br/>
#                 <i>{2}</i> <br/>
#                 <p>{3}</p> <br/>
#                 <b>Generovano: {4}</b> <br/>
#         </body>
# </html>""".format(publication.upper(), first_article.get("title"),
#                   first_article.get("published"),
#                   first_article.get("summary"),
#                   time.strftime("%d-%m-%Y %H:%M:%S"))


if __name__ == '__main__':
    app.run(host='192.168.240.237', port=5000, debug=True)
