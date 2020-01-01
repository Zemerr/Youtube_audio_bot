import youtube_dl
import os
import re
import db
from urllib.parse import urlparse
import requests
import bot
import local
from threading import Timer
import dbworker
import time
import subprocess
import bot
import main
import data
from threading import Thread

proxy = [None, 'proxy']
lst = []
def thread(fn):
    def execute(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute

def video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    o = urlparse(url)
    if o.netloc == 'youtu.be':
        return o.path[1:]
    elif o.netloc in ('www.youtube.com', 'youtube.com'):
        if o.path == '/watch':
            id_index = o.query.index('v=')
            return o.query[id_index+2:id_index+13]
        elif o.path[:7] == '/embed/':
            return o.path.split('/')[2]
        elif o.path[:3] == '/v/':
            return o.path.split('/')[2]
    return False

def delLog(chat_id, url_mes, mes_id):
    log = db.getlog(chat_id)
    if str(log) == '1':
        Timer(2, bot.deleteMessageLog2, [chat_id, mes_id]).start()
    if str(log) == '2':
        Timer(2, bot.deleteMessageLog2, [chat_id, url_mes, mes_id]).start()
    times = db.gettimes(chat_id)
    if times is None:
        db.addtimes(1, chat_id)
    else:
        db.addtimes(times + 1, chat_id)


def namevid(videoid):
    url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + str(videoid) + \
          '&key=AIzaSyCTq4yNi9LlYSPsSasrYlVh8_l-VtLkYvk'
    r = requests.get(url).json()
    name = r['items'][-1]['snippet']['title']
    try:
        thumb = r['items'][-1]['snippet']["thumbnails"]['standard']['url']
    except KeyError:
        try:
            thumb = r['items'][-1]['snippet']["thumbnails"]['high']['url']
        except KeyError:
            try:
                thumb = r['items'][-1]['snippet']["thumbnails"]['medium']['url']
            except KeyError:
                thumb = r['items'][-1]['snippet']["thumbnails"]['default']['url']
    return name, thumb





def dowload(url, user, chat_id, url_mes, mes_id, proxy, tryis):
    lang = db.get_language(chat_id)
    def update_tqdm(information):
        downloaded = information['downloaded_bytes']
        finish = information['total_bytes']
        bot.editMessageText(583128078, mes_id, local.text[''+lang+'']['loadingproc'] %
                            (str(int(float((int(downloaded) / int(finish))) * 100)) + '%'))
    id = video_id(url)
    inform = namevid(id)
    title = inform[0]
    name = re.sub(r'[^A-Za-zА-Яа-яА-яа-я亚-阿0-9-.;#%& ]', '_', title)
    ydl_opts = {
        'proxy': proxy,
        'noplaylist': True,
        'nooverwrites': True,
        'format': '140',
        'outtmpl': name + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'progress_hooks': [update_tqdm],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    try:
        inf = ydl.extract_info(url)
        duration = inf['duration']
        thumbnail = inform[1]
    except Exception as e:
        if 'Error 429' in str(e):
            if tryis == 0:
                tryis = 1
                dowload(url, user, chat_id, url_mes, mes_id, proxy[1], tryis)
        else:
            delLog(chat_id, url_mes, mes_id)
            print(e)
            bot.sendError(chat_id, mes_id, str(e), url, str(user))
            return False
    return name, mes_id, title, duration, thumbnail

def action(chat_id, videoid):
    print('y')
    def inf():
        print('t')
        while dbworker.get_current_state(str(chat_id) + str(videoid)):
            time.sleep(1)
            bot.sendChatAction(chat_id)
    p = Timer(0, inf)
    p.start()

def deleteFile(name):
    time.sleep(1)
    try:
        os.remove(name + '.m4a')
    except PermissionError as e:
        bot.sendMessage(-1001396479175, text=str(e))
        time.sleep(1.5)
        try:
            os.remove(name + '.m4a')
        except PermissionError as e:
            bot.sendMessage(-1001396479175, text=str(e))
        bot.sendMessage(-1001396479175, text='А не всё ок\n')

def sendFile(name, videoid, title, chat_id, ms_id1, ms_id2, duration, thumbnail):
    compsize = round(int(os.path.getsize(name + '.m4a')) / int(1048576), 2)
    dbworker.set_state(str(chat_id) + str(videoid), True)
    action(chat_id, videoid)
    if compsize >= 49:
        file = name + '.m4a'
        BOT_NAME = '@testaudio1202bot'
        title = title.replace('"', "'")
        stroka = 'python agent.py "' + str(file) + '" ' + str(chat_id) + ' ' + str(videoid) + ' ' + str(BOT_NAME) +\
                 ' ' + str(duration) + ' ' + str(0) + ' ' + str(compsize) + ' ' + str(ms_id1) + ' ' + str(ms_id2) + \
                 ' "' + str(title) + '"' + ' "' + str(thumbnail) + '"'
        subprocess.check_call(stroka, shell=True)
        Timer(2, deleteFile, [name])
    else:
        lang = db.get_language(chat_id)
        dbworker.delete(str(chat_id) + str(videoid))
        audio = bot.sendAudioCapt(chat_id, str(compsize), thumb=thumbnail, file=name, title=title)
        bot.editMessageText(chat_id, ms_id2, local.text['' + lang + '']['loading2'])
        #data.addmusic(videoid, audio, compsize)
        delLog(chat_id, ms_id1, ms_id2)
        deleteFile(name)

@thread
def func(url, user, chat_id, url_mes, mes_id):
    tryis = 0
    first = dowload(url, user, chat_id, url_mes, mes_id, proxy[0], tryis)
    if first:
        lang = db.get_language(chat_id)
        name = first[0]
        mes_id = first[1]
        title = first[2]
        duration = first[3]
        thumbnail = first[4]
        id = video_id(url)
        bot.editMessageText(chat_id, mes_id, local.text[''+lang+'']['loading1'])
        sendFile(name=name, videoid=id, title=title, chat_id=chat_id, ms_id1=url_mes, ms_id2=mes_id,
                 duration=duration, thumbnail=thumbnail)






