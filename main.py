from flask import Flask, request, jsonify
import local
import db
import json
import downloader as yt
import comands
import bot
from ast import literal_eval as dictionary
import data
#import telegram
import dbworker



Token = 'Your token'
listid = []
#URL = "https://api.telegram.org/bot{}/".format(Token)
URL = 'your_ip'
app = Flask(__name__)
#bote = telegram.Bot(token=Token)
def write_INF(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# @app.route('/set_webhook', methods=['GET', 'POST'])
# def set_webhook():
#     s = bote.setWebhook('https://%s:443/HOOK' % URLip, certificate=open('/etc/ssl/server.crt', 'rb'))
#     if s:
#         print(s)
#         return "webhook setup ok"
#     else:
#         return "webhook setup failed"

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r["message"]["from"]['id']
        try:
            audio = r["message"]['audio']
        except KeyError:
            audio = False
        if audio:
            if chat_id == 523228078:
                caption = r['message']['caption']
                info = dictionary(caption)
                audio = r['message']['audio']['file_id']
                thumbnail = info['thumbnail']
                chat_idUser = info['chat_id']
                ms_id2 = info['ms_id2']
                size = info['size']
                lang = db.get_language(chat_idUser)
                if thumbnail is None:
                    thumbnail =\
                        'http://i.piccy.info/i9/93bdb9542229f0b2fc366232b702a3b6/1576344239/83541/1352570/thumb.jpg'
                dbworker.delete(str(chat_idUser) + str(info['ytid']))
                bot.sendAudioCapt(info['chat_id'], size, thumb=thumbnail, tg_id=audio, title=info['name'])
                bot.editMessageText(chat_idUser, ms_id2, local.text['' + lang + '']['loading2'])
                yt.delLog(chat_idUser, info['ms_id'], ms_id2)
                data.addmusic(info['ytid'], audio, size)
            return jsonify(r)
        try:
            call = r["callback_query"]
        except KeyError:
            call = False
        if call:
            calbackid= r["callback_query"]["id"]
            calldata = r["callback_query"]['data']
            cond = r["callback_query"]['message']['text']
            message_id = r["callback_query"]['message']['message_id']
            bot.callBack(calldata, chat_id, cond, message_id, calbackid)
            return jsonify(r)
        try:
            text = r["message"]["text"]
        except KeyError:
            text = False
        if text:
            text = r["message"]["text"]
            lang = db.get_language(chat_id)
            try:
                func = local.comands[''+text.lower()+'']
            except KeyError:
                func = False
            if func:
                comands.comands(chat_id, text, lang)
            else:
                ytid = yt.video_id(text)
                if ytid:
                    user = r["message"]["from"]
                    urlmes_id = r["message"]["message_id"]
                    if urlmes_id not in listid:
                        listid.append(urlmes_id)
                        mes_id = bot.sendMessage(chat_id, local.text[''+lang+'']['loading'])
                        tgid = data.findmusic(ytid)
                        if tgid:
                            bot.editMessageText(chat_id, mes_id, local.text[''+lang+'']['loading1'])
                            bot.sendAudioCapt(chat_id, data.findsize(ytid), tg_id=tgid)
                            bot.editMessageText(chat_id, mes_id, local.text['' + lang + '']['loading2'])
                            yt.delLog(chat_id, urlmes_id, mes_id)
                        else:
                            yt.func(text, user, chat_id, urlmes_id, mes_id)
                    else:
                        pass
                else:
                    bot.sendMessage(chat_id, local.text['' + lang + '']['linkformat'])
            return jsonify(r)
        else:
            lang = db.get_language(chat_id)
            bot.sendMessage(chat_id, local.text[''+lang+'']['linkformat'])


if __name__ == '__main__':
    app.run()