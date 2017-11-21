import config as sv
import datetime
import feedparser
import json
import time
import urllib.request
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request

app = Flask(__name__)


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return sv.DEFAULTS[key]


@app.route("/")
def home():
    gen_time = time.strftime("%d-%m-%Y %H:%M:%S")

    # get customized headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # save cookies and return template
    response = make_response(render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies),
                           gen_time=gen_time))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

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
    return to_rate / frm_rate, parsed.keys()


if __name__ == '__main__':
    app.run(host='192.168.240.237', port=5000, debug=True)
