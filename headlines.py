import config as sv
import feedparser
import json
import time
import urllib.request
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def home():
    gen_time = time.strftime("%d-%m-%Y %H:%M:%S")
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = sv.DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = sv.DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = sv.DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = sv.DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)
    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           gen_time=gen_time
                           )


def get_news(query):
    if not query or query.lower() not in sv.RSS_FEEDS:
        publication = sv.DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(sv.RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.request.quote(query)
    url = sv.WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read().decode('utf8')
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']
                   }
    return weather


def get_rate(frm, to):
    all_currency = urllib.request.urlopen(sv.CURRENCY_URL).read().decode('utf8')
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate


if __name__ == '__main__':
    app.run(host='192.168.240.237', port=5000, debug=True)
