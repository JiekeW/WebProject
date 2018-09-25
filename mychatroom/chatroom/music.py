import requests
import json,re

#QQ音乐
#最新音乐
new_song = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8¬ice=0&platform=h5&needNewCode=1&tpl=3&page=detail&type=top&topid=27&_=1519963122923'
 
#随机音乐
random_song = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8¬ice=0&platform=h5&needNewCode=1&tpl=3&page=detail&type=top&topid=36&_=1520777874472'

def search_song(search, n=30):
    search_url = 'http://s.music.qq.com/fcgi-bin/music_search_new_platform?t=0&n=%d&aggr=1&cr=1&loginUin=0&inCharset=GB2312&outCharset=utf-8&notice=0&platform=jqminiframe.json&needNewCode=0&p=1&catZhida=0&remoteplace=sizer.newclient.next_song&w=%s' %(n, search)

    re_text = requests.get(search_url).text
    res = json.loads(re_text[9:-1])['data']['song']['list']
    result = []
    for i in res:
        song = i['f'].split('|')
        try:
            total_name = song[1]
            name = re.findall(r'(.*?)\(.*;\)',total_name)[0]
            singer = song[3]
            # time = int(song[7])
            songmid = song[-5]
            result.append([name, singer, songmid])
        except Exception as e:
            continue
    return result

# url = 'http://ws.stream.qqmusic.qq.com/C100'+songmid+'.m4a?fromtag=0&guid=126548448