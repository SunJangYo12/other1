# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import re
import json
from time import time
from random import random
import warnings
import logging
from models import *
from index import *
import os

try:
    from urllib.parse import urlencode
    basestring = (str, bytes)
except ImportError:
    from urllib import urlencode
    basestring = basestring

# Python 2's `input` executes the input, whereas `raw_input` just returns the input
try:
    input = raw_input
except NameError:
    pass

# Log settings
log = logging.getLogger("client")
log.setLevel(logging.DEBUG)
# Creates the console handler
handler = logging.StreamHandler()
log.addHandler(handler)

#: Default list of user agents
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/601.1.10 (KHTML, like Gecko) Version/8.0.5 Safari/601.1.10",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; ; NCT50_AAP285C84A1328) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"
]

LIKES = {
    'large': EmojiSize.LARGE,
    'medium': EmojiSize.MEDIUM,
    'small': EmojiSize.SMALL,
    'l': EmojiSize.LARGE,
    'm': EmojiSize.MEDIUM,
    's': EmojiSize.SMALL
}


css = "{position:relative;}.b .dd{display:block;padding-bottom:4px;}.dc{padding-bottom:8px;padding-top:8px;}.b .cz{border-top:1px solid #bec3c9;}.b tr td.cb{padding:6px;vertical-align:middle;}.b tr td.bz{padding-bottom:1px;}.b .cn{background:inherit;padding-top:6px;}.b .cn .cv input{height:45px;margin-left:3px;padding:0 12px 0 12px;}.b .bt{background:#f5f6f7;}.ca{display:block;font-size:small;margin:2px;padding:6px 12px 6px 12px;text-align:center;}.b a.ca,.b a.ca:visited{background:#fff;border:1px solid #cdd5e2;color:#8d949e;}.b a.ca:focus,.b a.ca:hover{background:#cdd5e2;border:1px solid #ebedf0;color:#f5f6f7;}.b .ba{border:0;border-collapse:collapse;margin:0;padding:0;width:100%;}.b .ba tbody{vertical-align:top;}.b .dm>tr>td,.b .dm>tbody>tr>td,.b .ba td.dm{vertical-align:middle;}.b .ba td{padding:0;}.b .ba td.bj{padding:2px;}.b .ba td.bu{padding:4px;}.b .bg{width:100%;}.b a,.b a:visited{color:#3b5998;text-decoration:none;}.b .br,.b .br:visited{color:#fff;}.b a:focus,.b a:hover{background-color:#3b5998;color:#fff;}.b .br:focus,.b .br:hover{background-color:#fff;color:#3b5998;}.ct{height:60px;margin-bottom:7px;}.cu{height:36px;margin-bottom:7px;}#composer_form,.co{display:inline;}.e{background-color:#fff;}.w{background-color:#3b5998;}.x{padding:2px 3px;}.cc{padding:4px 3px;}.cd{padding:6px 3px;}.ce{border-top:1px solid;}.e{border-color:#e9e9e9;}.w{border-color:#1d4088;}form{margin:0;border:0;}.cp{width:100%;}.cp td{vertical-align:top;padding:0;}.cp .cq{width:100%;}.cp .cv{padding-left:5px;}.cp .cs{display:block;width:100%;}.cr{border:solid 1px #999;border-top-color:#888;margin:0;}.b .cr{padding:3px 3px 4px 0;}.bm{-webkit-appearance:none;background:none;display:inline-block;font-size:12px;height:28px;line-height:28px;margin:0;overflow:visible;padding:0 9px;text-align:center;vertical-align:top;white-space:nowrap;}.b .bm{border-radius:2px;}.bo,a.bo,html .b a.bo{color:#fff;}.b .bo{background-color:#4267b2;border:1px solid #365899;}.b a.bo:hover,.b .bo:hover{background-color:#465e91;}.bo[disabled]{color:#899bc1;}.b .bo[disabled]:hover{background-color:#4267b2;}.bm .t{display:inline-block;}.b .bm .t{display:inline-block;margin-top:0;vertical-align:middle;}.b a.bm::after{content:"";display:inline-block;height:100%;vertical-align:middle;}.bm .t{line-height:20px;margin-top:4px;}.b .bm{padding:0 8px;}.b a.bm{height:26px;line-height:26px;}.t{pointer-events:none;}.db{color:#90949c;}.da{font-size:14px;line-height:20px;}.bl{font-weight:normal;}.bv{font-weight:bold;}.by{color:gray;}.k{font-size:small;}body,tr,input,textarea,.f{font-size:medium;}.cx{-webkit-appearance:none;background-color:transparent;border:0;display:inline;font-size:inherit;margin:0;padding:0;}.cx:hover{background-color:#3b5998;color:#fff;white-space:normal;}.cy{color:#3b5998;}.b .dp{padding:0;}.b .bj{padding:2px;}.b .bu{padding:4px;}.bw{margin:2px 0 0 5px;}.o{border:0;display:inline-block;vertical-align:top;}i.o u{position:absolute;width:0;height:0;overflow:hidden;}body{text-align:left;direction:ltr;}body,tr,input,textarea,button{font-family:sans-serif;}body,p,figure,h1,h2,h3,h4,h5,h6,ul,ol,li,dl,dd,dt{margin:0;padding:0;}h1,h2,h3,h4,h5,h6{font-size:1em;font-weight:bold;}ul,ol{list-style:none;}article,aside,figcaption,figure,footer,header,nav,section{display:block;}.d #viewport{margin:0 auto;max-width:600px;}.bf,.bf.o{display:block;}.bc{display:block;}.bd{height:20px;width:20px;}.y{background:#3b5998;padding:0 4px 4px;height:22px;}.y.y .bk{background:#fff;border:1px solid #243872;box-sizing:border-box;font-size:small;height:22px;margin:0;width:100%;}.z.y{padding:1px 1px 3px;}.y .be{padding:1px 3px 0 0;}.y.y.y .bn{background:#627aba;border:1px solid #2e417e;color:#fff;font-size:x-small;font-weight:normal;height:22px;line-height:20px;margin-left:3px;}.bi{border:0;display:block;margin:0;padding:0;}.df{font-size:small;padding:7px 8px 8px;}.dx{display:block;margin-top:8px;padding:2px;text-align:center;}.dv{display:block;font-size:x-small;margin:-3px -3px 1px -3px;padding:3px;}.b .df td.du{padding-right:4px;}.b .df td.dw{padding-left:4px;}.df.dg{background-color:#444950;}.dg{border-top:1px solid #444950;color:#bec3c9;}.dg .dx{border:1px solid #bec3c9;color:#bec3c9;}.b .dg a,.b .dg a:visited{color:#bec3c9;}.b .dg a:focus,.b .dg a:hover{background:#dadde1;color:#1d2129;}.dg .dx:focus,.dg .dx:hover{background:#dadde1;border:1px solid #dadde1;color:#1d2129;}.di{margin-bottom:8px;}.df.dg .di>table{background:#d3d7dc;border:1px solid #444950;}.dq{background:#d3d7dc;}.de{background:#fff;}.dh .dt{height:24px;line-height:24px;margin-left:2px;}.dk{background:#fff;}.dh .dr{background-color:transparent;color:#4b4f56;display:block;padding:0;width:100%;}.dl .o{display:block;}.dh .dj .ds{padding:2px;}.dh .dj .dl{padding:4px;}.b .dh .dj{border:1px solid #8d949e;}.l img{padding-left:5px;padding-top:4px;}.l{display:inline-block;padding:3px 0 0 5px;vertical-align:middle;}.b a.n,.b a.n:focus,.b a.n:hover,.b a.n:visited,a.n,a.n:focus,a.n:hover,a.n:visited{background:none;color:#fff;cursor:pointer;padding:0;text-decoration:none;}.p{display:table-cell;padding:4px 5px 4px 5px;text-align:right;vertical-align:middle;}.h{display:table;width:100%;}.m{padding:0 0 0 0;}.i{background-color:#b22ec0;color:#fff;padding-bottom:2px;padding-top:2px;width:100%;}.j{display:table-cell;padding-bottom:2px;padding-left:6px;padding-top:1px;padding-top:2px;position:relative;vertical-align:middle;width:100%;}.bp{padding-bottom:1px;}.bq{display:inline-block;font-size:small;padding:2px 4px 2px;}.bs{color:#fff496;}.b a:hover .bs,.b a:focus .bs,.bq:hover .bs,.bq:focus .bs{color:#365899;}.s,.b .s{border-radius:2px;display:inline-block;height:25px;line-height:26px;overflow:visible;padding:0 9px;text-align:center;vertical-align:middle;white-space:nowrap;}.r,.b a.r,.b a.r:hover,.b .r,.b .r:hover{background:#b22ec0;border:1px solid #fff;color:#fff;font-size:12px;}/*]]>*/"

MessageReactionFix = {
    '😍': ('0001f60d', '%F0%9F%98%8D'),
    '😆': ('0001f606', '%F0%9F%98%86'),
    '😮': ('0001f62e', '%F0%9F%98%AE'),
    '😢': ('0001f622', '%F0%9F%98%A2'),
    '😠': ('0001f620', '%F0%9F%98%A0'),
    '👍': ('0001f44d', '%F0%9F%91%8D'),
    '👎': ('0001f44e', '%F0%9F%91%8E')
}


GENDERS = {
    # For standard requests
    0: 'unknown',
    1: 'female_singular',
    2: 'male_singular',
    3: 'female_singular_guess',
    4: 'male_singular_guess',
    5: 'mixed',
    6: 'neuter_singular',
    7: 'unknown_singular',
    8: 'female_plural',
    9: 'male_plural',
    10: 'neuter_plural',
    11: 'unknown_plural',

    # For graphql requests
    'UNKNOWN': 'unknown',
    'FEMALE': 'female_singular',
    'MALE': 'male_singular',
    #'': 'female_singular_guess',
    #'': 'male_singular_guess',
    #'': 'mixed',
    'NEUTER': 'neuter_singular',
    #'': 'unknown_singular',
    #'': 'female_plural',
    #'': 'male_plural',
    #'': 'neuter_plural',
    #'': 'unknown_plural',
}

class ReqUrl(object):
    SEARCH = "https://www.facebook.com/ajax/typeahead/search.php"
    LOGIN = "https://free.facebook.com/login.php?refsrc=https%3A%2F%2Ffree.facebook.com%2F&amp;lwv=101&amp;refid=8"
    SEND = "https://www.facebook.com/messaging/send/"
    UNREAD_THREADS = "https://www.facebook.com/ajax/mercury/unread_threads.php"
    UNSEEN_THREADS = "https://www.facebook.com/mercury/unseen_thread_ids/"
    THREADS = "https://www.facebook.com/ajax/mercury/threadlist_info.php"
    MESSAGES = "https://www.facebook.com/ajax/mercury/thread_info.php"
    READ_STATUS = "https://www.facebook.com/ajax/mercury/change_read_status.php"
    DELIVERED = "https://www.facebook.com/ajax/mercury/delivery_receipts.php"
    MARK_SEEN = "https://www.facebook.com/ajax/mercury/mark_seen.php"
    BASE = "https://free.facebook.com"
    MOBILE = "https://0.facebook.com/"
    STICKY = "https://free.facebook.com/messages/read/"
    PING = "https://free.facebook.com/messages/read/"
    UPLOAD = "https://z-upload.facebook.com/ajax/mercury/upload.php"
    INFO = "https://www.facebook.com/chat/user_info/"
    CONNECT = "https://www.facebook.com/ajax/add_friend/action.php?dpr=1"
    REMOVE_USER = "https://www.facebook.com/chat/remove_participants/"
    LOGOUT = "https://www.facebook.com/logout.php"
    ALL_USERS = "https://www.facebook.com/chat/user_info_all"
    SAVE_DEVICE = "https://m.facebook.com/login/save-device/cancel/"
    CHECKPOINT = "https://m.facebook.com/login/checkpoint/"
    THREAD_COLOR = "https://www.facebook.com/messaging/save_thread_color/?source=thread_settings&dpr=1"
    THREAD_NICKNAME = "https://www.facebook.com/messaging/save_thread_nickname/?source=thread_settings&dpr=1"
    THREAD_EMOJI = "https://www.facebook.com/messaging/save_thread_emoji/?source=thread_settings&dpr=1"
    THREAD_IMAGE = "https://www.facebook.com/messaging/set_thread_image/?dpr=1"
    THREAD_NAME = "https://www.facebook.com/messaging/set_thread_name/?dpr=1"
    MESSAGE_REACTION = "https://www.facebook.com/webgraphql/mutation"
    TYPING = "https://www.facebook.com/ajax/messaging/typ.php"
    GRAPHQL = "https://www.facebook.com/api/graphqlbatch/"
    ATTACHMENT_PHOTO = "https://www.facebook.com/mercury/attachments/photo/"
    EVENT_REMINDER = "https://www.facebook.com/ajax/eventreminder/create"
    MODERN_SETTINGS_MENU = "https://www.facebook.com/bluebar/modern_settings_menu/"
    REMOVE_FRIEND = "https://m.facebook.com/a/removefriend.php"
    CREATE_GROUP = "https://m.facebook.com/messages/send/?icm=1"

    def change_pull_channel(self, channel=None):
        if channel is None:
            self.pull_channel = (self.pull_channel + 1) % 5 # Pull channel will be 0-4
        else:
            self.pull_channel = channel
        self.STICKY = "https://{}-edge-chat.facebook.com/pull".format(self.pull_channel)
        self.PING = "https://{}-edge-chat.facebook.com/active_ping".format(self.pull_channel)


facebookEncoding = 'UTF-8'

def now():
    return int(time()*1000)

def strip_to_json(text):
    try:
        return text[text.index('{'):]
    except ValueError:
        raise FBchatException('No JSON object found: {}, {}'.format(repr(text), text.index('{')))

def get_decoded_r(r):
    return get_decoded(r._content)

def get_decoded(content):
    return content.decode(facebookEncoding)

def parse_json(content):
    return json.loads(content)

def get_json(r):
    return json.loads(strip_to_json(get_decoded_r(r)))

def digitToChar(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number, base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digitToChar(m)
    return digitToChar(m)

def generateMessageID(client_id=None):
    k = now()
    l = int(random() * 4294967295)
    return "<{}:{}-{}@mail.projektitan.com>".format(k, l, client_id)

def getSignatureID():
    return hex(int(random() * 2147483648))

def generateOfflineThreadingID():
    ret = now()
    value = int(random() * 4294967295)
    string = ("0000000000000000000000" + format(value, 'b'))[-22:]
    msgs = format(ret, 'b') + string
    return str(int(msgs, 2))

def check_json(j):
    if j.get('error') is None:
        return
    if 'errorDescription' in j:
        # 'errorDescription' is in the users own language!
        raise FBchatFacebookError('Error #{} when sending request: {}'.format(j['error'], j['errorDescription']), fb_error_code=j['error'], fb_error_message=j['errorDescription'])
    elif 'debug_info' in j['error'] and 'code' in j['error']:
        raise FBchatFacebookError('Error #{} when sending request: {}'.format(j['error']['code'], repr(j['error']['debug_info'])), fb_error_code=j['error']['code'], fb_error_message=j['error']['debug_info'])
    else:
        raise FBchatFacebookError('Error {} when sending request'.format(j['error']), fb_error_code=j['error'])

def check_listen(r):
    content = get_decoded_r(r)
    content = strip_to_json(content)
    oke = re.sub('<[^<]+?>', '', content) # pisah html
    try:
		out1 = oke.split("-_-")
		out2 = out1[1].split("#")
		index = Starting(out2[0])
		index.setDatabase("buat", out2[0])
		#os.system("sh /root/AL/offlineDB.sh")
		return format(repr(out2[0]))
    except Exception, e:
		return oke

def check_request(r, as_json=True):
    if not r.ok:
        raise FBchatFacebookError('Error when sending request: Got {} response'.format(r.status_code), request_status_code=r.status_code)

    content = get_decoded_r(r)

    if content is None or len(content) == 0:
        raise FBchatFacebookError('Error when sending request: Got empty response')

    if as_json:
        content = strip_to_json(content)
        try:
            j = json.loads(content)
        except ValueError:
            raise FBchatFacebookError('Error while parsing JSON: {}'.format(repr(content)))
        check_json(j)
        return j
    else:
        return content
        #FFFFFF
def get_jsmods_require(j, index):
    if j.get('jsmods') and j['jsmods'].get('require'):
        try:
            return j['jsmods']['require'][0][index][0]
        except (KeyError, IndexError) as e:
            log.warning('Error when getting jsmods_require: {}. Facebook might have changed protocol'.format(j))
    return None

def get_emojisize_from_tags(tags):
    if tags is None:
        return None
    tmp = [tag for tag in tags if tag.startswith('hot_emoji_size:')]
    if len(tmp) > 0:
        try:
            return LIKES[tmp[0].split(':')[1]]
        except (KeyError, IndexError):
            log.exception('Could not determine emoji size from {} - {}'.format(tags, tmp))
    return None
