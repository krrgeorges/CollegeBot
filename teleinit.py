import logging
from telegram.ext import MessageHandler, CommandHandler, Updater, Filters
from datetime import datetime
import telegram

from college_info import College_Information

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def log(string):
    from datetime import datetime
    i = datetime.now()
    print(i.strftime('%Y/%m/%d %H:%M:%S')+" : "+string)


def start(bot,update):
    log("Bot started on " +str(update.message.chat_id)+" with name "+update.message.from_user.first_name+" "+update.message.from_user.last_name)
    bot.send_message(chat_id=update.message.chat_id,text="Hello, "+update.message.from_user.first_name)

def logic_handle(bot,update):
    bool = False
    msg = update.message.text.replace("?","").split()

    locsword = ["location","Location","LOCATION"]
    if any(geo in msg for geo in locsword) and bool==False:
        bool = True
        bot.sendLocation(chat_id=update.message.chat_id,latitude=19.0411339,longitude=72.8613285)
        route = "<b>Main landmarks en route from Sion Station to College:</b>\n*Axis Bank\n*Hotel Gurukrupa\n"
        bot.send_message(chat_id=update.message.chat_id,text=route,parse_mode=telegram.ParseMode.HTML)
        log("Sent location info to "+update.message.from_user.first_name)
        
    contactwords = ["Contact","contact","CONTACT"]
    if any(cont in msg for cont in contactwords) and bool==False:
        bool = True
        College_Information().send_contact(bot,update)

    newsword = ["news","News","NEWS"]
    if any(news in msg for news in newsword) and bool==False:
        bool = True
        College_Information().send_news(bot,update)
        

def contact_info(bot,update):
    College_Information().send_contact(bot,update)

def college_news(bot,update):
    College_Information().send_news(bot,update)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    bot.send_message(chat_id=update.message.chat_id,text="Some error has occured.")


updater = Updater("310268149:AAGiqhyEzC6dyLVyGDW0T5DsSnlPOgMWjiI")

dp = updater.dispatcher

dp.add_handler(CommandHandler("start",start))

dp.add_handler(CommandHandler("contact",contact_info))

dp.add_handler(CommandHandler("news",college_news))
    
dp.add_handler(MessageHandler(Filters.text,logic_handle))

dp.add_error_handler(error)

log("Bot initiated")

updater.start_polling()

updater.idle()
