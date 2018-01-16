import requests
import telegram
import xml.etree.ElementTree as ET
# from bs4 import BeautifulSoup
from telegram.ext import Filters, CommandHandler, Updater
from random import randint
from string import Template

updater = Updater(token='502007891:AAHHvj0UJr6GEk1TInHtC_867qaDQhtw6Ps')
dispatcher = updater.dispatcher

def webcam(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo='http://www.vorarlberg-alpenregion.at/inc/webcam/lib/slir/?w=1280&q=100&i=/inc/webcam/img/webcam_4225&rnd=%s' % randint(0, 99999))

def neige(bot, update):
    r = requests.get("http://www.myweather2.com/developer/weather.ashx?uac=Vuu25Od2xg&uref=f7b729e0-e564-4077-9579-0ba7475b5d7f")
    tree = ET.fromstring(r.text)
    snow_report = tree.find("snow_report")
    date = snow_report.find("report_date").text
    upper_snow_depth = snow_report.find("upper_snow_depth").text
    lower_snow_depth = snow_report.find("lower_snow_depth").text
    last_snow_date = snow_report.find("last_snow_date").text

    report_template = Template("*Bulletin de neige du $date*\nEn haut des pistes : $upper_snow_depth cm\nEn bas des pistes : $lower_snow_depth cm\nDernière chute de neige : $last_snow_date")
    report = report_template.substitute(date=date,
                               upper_snow_depth=upper_snow_depth,
                               lower_snow_depth=lower_snow_depth,
                               last_snow_date=last_snow_date)
    bot.send_message(chat_id=update.message.chat_id, text=report, parse_mode=telegram.ParseMode.MARKDOWN)

    # r = requests.get("https://www.skiinfo.fr/vorarlberg/brandnertal/bulletin-neige.html")
    # soup = BeautifulSoup(r.text, "html.parser")
    # date = soup.select("#snow_conditions div div ul li.left strong")[0].string
    # temp_upper = soup.select("#snow_conditions div ul._report.sr_weather_table.clearfix li._report_content ul li.station.summit div.weather div.temp.below")[0].string
    # temp_lower = soup.select("#snow_conditions div ul._report.sr_weather_table.clearfix li._report_content ul li.station.base div.weather div.temp.above")[0].text
    # snow_upper = soup.select("ul.sr_snow_depth_stations li.elevation.upper .bluePill")[0].string
    # snow_lower = soup.select("ul.sr_snow_depth_stations li.elevation.lower .bluePill")[0].string
    # bot.send_message(chat_id=update.message.chat_id, text="*Bulletin du %s*\nConditions en haut : %s %s\nConditions en bas : %s %s" % (date, snow_upper, temp_upper, snow_lower, temp_lower), parse_mode=telegram.ParseMode.MARKDOWN)


webcam_handler = CommandHandler('webcam', webcam)
dispatcher.add_handler(webcam_handler)
neige_handler = CommandHandler('neige', neige)
dispatcher.add_handler(neige_handler)

updater.start_polling()
