import db
import requests
import local
import json
import bot
from threading import Thread

def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute

Token = '1025274697:AAF2Bxjy7NNvYSHR-YwyFCg3f5ymeyr2-TE'

URL = "https://api.telegram.org/bot{}/".format(Token)

@thread
def comands(chat_id, text, lang):
    if text == '/start':
        start(chat_id)
    elif text == '/help':
        help(chat_id, lang)
    elif text == '/lang':
        langfunc(chat_id, lang)
    elif text == '/settings':
        setting(chat_id, lang)

#@thread
def start(chat_id):
    url = URL + "sendMessage"
    reply = json.dumps({'inline_keyboard': [[{'text': '🇺🇸 English', 'callback_data': 'en'}],
                                            [{'text': '🇺🇦 Українська', 'callback_data': 'ua'}],
                                            [{'text': '🇷🇺 Русский', 'callback_data': 'ru'}]]})
    jsonic = {'chat_id': chat_id, 'text': 'Choose your language and let\'s go(Выберите язык и погнали)',
            'parse_mode': 'HTML', 'disable_web_page_preview': True, 'reply_markup': reply}
    r = requests.post(url, json=jsonic)
    return r.json()

#@thread
def langfunc(chat_id, lang):
    url = URL + "sendMessage"
    reply = json.dumps({'inline_keyboard': [[{'text': '🇺🇸 English', 'callback_data': 'en'}],
                                            [{'text': '🇺🇦 Українська', 'callback_data': 'ua'}],
                                            [{'text': '🇷🇺 Русский', 'callback_data': 'ru'}]]})
    jsonic = {'chat_id': chat_id, 'text': local.text[''+lang+'']['lang'],
            'parse_mode': 'HTML', 'disable_web_page_preview': True, 'reply_markup': reply}
    r = requests.post(url, json=jsonic)
    return r.json()

#@thread
def help(chat_id, lang):
    data = {'chat_id': chat_id, 'video': local.text[''+lang+'']['video']}
    bot.sendMessage(text=local.text[''+lang+'']['help'], id=chat_id)
    resp = requests.post(URL + "sendVideo", data=data)
    return resp.json()

#@thread
def setting(chat_id, lang):
    url = URL + "sendMessage"
    num = str(db.getlog(chat_id))
    reply = json.dumps({'inline_keyboard': [[{'text': local.text[''+lang+'']['way']+num, 'callback_data': 'log'+num}]]})
    jsonic = {'chat_id': chat_id, 'text': local.text['' + lang + '']['log'],
              'parse_mode': 'HTML', 'disable_web_page_preview': True, 'reply_markup': reply}
    r = requests.post(url, json=jsonic)
    return r.json()