import db
import requests
import local
import json
from urllib.request import urlopen as read
from threading import Thread

Token = '1025274697:AAF2Bxjy7NNvYSHR-YwyFCg3f5ymeyr2-TE'

URL = "https://api.telegram.org/bot{}/".format(Token)

def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute

def deleteMessage(chat_id, mes_id):
    url = URL + "deleteMessage"
    json = {'chat_id': chat_id, 'message_id': mes_id}
    r = requests.post(url, json=json)
    return r.json()

def sendChatAction(chat_id):
    url = URL + "sendChatAction"
    json = {'chat_id': chat_id, 'action': 'upload_audio'}
    r = requests.post(url, json=json)
    return r.json()

def editMessageText(chat_id, mes_id, text):
    url = URL + "editMessageText"
    json = {'chat_id': chat_id, 'message_id': mes_id, 'text': text, 'parse_mode': 'HTML',
            'disable_web_page_preview': True}
    r = requests.post(url, json=json)
    return r.json()

def deleteMessageLog2(chat_id, mes_id1, mes_id2):
    url = URL + "deleteMessage"
    json = {'chat_id': chat_id, 'message_id': mes_id1}
    r = requests.post(url, json=json)
    jsonic = {'chat_id': chat_id, 'message_id': mes_id2}
    resp = requests.post(url, json=jsonic)
    return r.json(), resp.json()

def sendMessage(id, text='Smth wrong!', disable_web_page_preview=True):
    url = URL + "sendMessage"
    json = {'chat_id': id, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': disable_web_page_preview}
    r = requests.post(url, json=json).json()
    try:
        id = r['result']['message_id']
    except KeyError:
        id = None
    return id

def sendAudioCapt(chat_id, size, title=None, thumb=None, file=False, tg_id=False):
    url = URL + "sendAudio"
    if thumb is not None:
        thumbail = read(thumb).read()
    else:
        thumbail = None
    if file:
        with open(file + '.m4a', 'rb') as f:
            data = {'chat_id': chat_id, 'caption': "<a href=\"http://t.me/YTAudioVoiceBot?start=share"+str(chat_id)
                    + "\">YTAudioVoiceBot</a>: ""<i>" + str(size)+"Mb</i>", 'parse_mode': 'HTML', 'title': title}
            files = {'audio': f, 'thumb': thumbail}
            r = requests.post(url, files=files, data=data).json()
            f.close()
        return r["result"]['audio']['file_id']
    if tg_id:

        data = {'chat_id': chat_id, 'audio': tg_id, 'caption': "<a href=\"http://t.me/YTAudioVoiceBot?start=share"
                + str(chat_id) + "\">YTAudioVoiceBot</a>: ""<i>" + str(size) + "Mb</i>", 'parse_mode': 'HTML'}
        files = {'thumb': thumbail}
        r = requests.post(url, files=files, data=data)

def sendError(chat_id, mes_id, er, url, inf):
    lang = db.get_language(chat_id)
    editMessageText(chat_id, mes_id, text=local.text[''+lang+'']['loadinger'])
    sendMessage(chat_id, local.text[''+lang+'']['error'])
    sendMessage(-1001396479175, text=er+'\n'+url+'\n'+inf, disable_web_page_preview=False)

@thread
def callBack(calldata, chat_id, cond, message_id, calbackid):
    if calldata == 'log2':
        lang = db.get_language(chat_id)
        reply = json.dumps({'inline_keyboard': [[{'text': local.text['' + lang + '']['way'] + '3',
                                                  'callback_data': 'log3'}]]})
        jsonic1 = {'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply}
        requests.post(URL + "editMessageReplyMarkup", json=jsonic1)
        jsonic = {'callback_query_id': calbackid, 'text': local.text['' + lang + '']['way3']}
        requests.post(URL + 'answerCallbackQuery', json=jsonic)
        db.editlog(chat_id, 3)
    if calldata == 'log3':
        lang = db.get_language(chat_id)
        reply = json.dumps({'inline_keyboard': [[{'text': local.text['' + lang + '']['way'] + '1',
                                                  'callback_data': 'log1'}]]})
        jsonic1 = {'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply}
        requests.post(URL + "editMessageReplyMarkup", json=jsonic1)
        jsonic = {'callback_query_id': calbackid, 'text': local.text['' + lang + '']['way1']}
        requests.post(URL + 'answerCallbackQuery', json=jsonic)
        db.editlog(chat_id, 1)
    if calldata == 'log1':
        lang = db.get_language(chat_id)
        reply = json.dumps({'inline_keyboard': [[{'text': local.text['' + lang + '']['way'] + '2',
                                                  'callback_data': 'log2'}]]})
        jsonic1 = {'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply}
        requests.post(URL + "editMessageReplyMarkup", json=jsonic1)
        jsonic = {'callback_query_id': calbackid, 'text': local.text['' + lang + '']['way2']}
        requests.post(URL + 'answerCallbackQuery', json=jsonic)
        db.editlog(chat_id, 2)
    if calldata == 'ru':
        status = db.add_user(chat_id, "ru", 1, 0, 2)
        if status:
            if cond == 'Choose your language and let\'s go(Выберите язык и погнали)':
                text = str(local.text["ru"]["start"])
                sendMessage(chat_id, text)
            else:
                text = str(local.text["ru"]["lang1"])
                sendMessage(chat_id, text)
        else:
            sendMessage(chat_id, text="Что-то пошло не так(. Попробуй позже")
    if calldata == 'ua':
        status = db.add_user(chat_id, "ua", 1, 0, 2)
        if status:
            if cond == 'Choose your language and let\'s go(Выберите язык и погнали)':
                text = str(local.text["ua"]["start"])
                sendMessage(chat_id, text)
            else:
                text = str(local.text["ua"]["lang1"])
                sendMessage(chat_id, text)
        else:
            sendMessage(chat_id, text="Щось пішло не так(. Спробуй пізніше")
    if calldata == 'en':
        status = db.add_user(chat_id, "en", 1, 0, 2)
        if status:
            if cond == 'Choose your language and let\'s go(Выберите язык и погнали)':
                text = str(local.text["en"]["start"])
                sendMessage(chat_id, text)
            else:
                text = str(local.text["en"]["lang1"])
                sendMessage(chat_id, text)
        else:
            sendMessage(chat_id, text="Smth wrong(. Try later")
