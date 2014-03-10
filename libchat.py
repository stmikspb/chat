from google.appengine.ext import db
import re
from urlparse import urlparse
from google.appengine.ext.webapp import template
from django.utils import simplejson
from google.appengine.api import channel



arr_emo = []
arr_emo_secret = []
def addEmo(c, i, ext = '.gif', secret = False):
    if secret == False:
        arr_emo.append({'c':c, 'i':i + ext})
    else:
        arr_emo_secret.append({'c':c, 'i':i + ext})
addEmo(':confused:', 'icon_confused')
addEmo(':demit:', 'skeleton')
addEmo(':D', 'icon_biggrin')
addEmo(':GPI:', 'icon_gpitm')
addEmo(':twisted:', 'icon_twisted')
addEmo(':thumb-up:', 'new_thumbup')
addEmo(':-D', 'icon_biggrin')
addEmo(':clap:', 'eusa_clap')
addEmo(':mrgreen:', 'icon_mrgreen')
addEmo('8)', 'icon_cool')
addEmo(':mario:', 'mario')
addEmo(':o', 'icon_surprised')
addEmo('](*,)', 'eusa_wall')
addEmo(':roll:', 'icon_rolleyes')
addEmo(':thumb-down:', 'new_thumbdn')
addEmo(':grin:', 'icon_biggrin')
addEmo('=D>', 'eusa_clap')
addEmo(':=D)', 'eusa_clap')
addEmo('8-)', 'icon_cool')
addEmo(':-E', 'gigi')
addEmo(':)', 'icon_smile')
addEmo(':siul:', 'eusa_whistle')
addEmo(':wink:', 'icon_wink')
addEmo(':blow-up:', 'new_blowingup')
addEmo(':-)', 'icon_smile')
addEmo(':(', 'icon_sad')
addEmo('#-o', 'eusa_doh')
addEmo(':lol:', 'icon_lol')
addEmo(':-p', 'y_10')
addEmo(':angel:', 'eusa_angel')
addEmo(';-)', 'icon_wink')
addEmo(':bad-words:', 'new_cussing')
addEmo(':smile:', 'icon_smile')
addEmo(':nangis:', 'nangis')
addEmo('=P~', 'eusa_drool')
addEmo(':x', 'icon_mad')
addEmo(':-p', 'y_10')
addEmo('=;', 'eusa_hand')
addEmo(':!:', 'icon_exclaim')
addEmo(':-\"', 'siul')
addEmo(':crazyeyes:', 'new_Eyecrazy')
addEmo(':-(', 'icon_sad')
addEmo(':^o', 'eusa_liar')
addEmo(':-x', 'icon_mad')
addEmo(':udut:', 'udut')
addEmo(':-&', 'eusa_sick')
addEmo(':question', 'icon_question')
addEmo(':n00b:', 'new_newbie')
addEmo(':sad:', 'icon_sad')
addEmo(':mad:', 'icon_mad')
addEmo(':---)', 'eusa_liar')
addEmo(':udud:', 'smoke', '.png')
addEmo(':boohoo', 'eusa_boohoo')
addEmo(':idea:', 'icon_idea')
addEmo(':flower:', 'bloem12')
addEmo(':rofl:', 'new_rofl')
addEmo(':-o', 'icon_surprised')
addEmo(':kabur:', 'penguinkabur')
addEmo('[-X', 'eusa_naughty')
addEmo(':menyan:', 'menyan')
addEmo(':-$', 'eusa_shhh')
addEmo(':arrow:', 'icon_arrow')
addEmo(':scatter:', 'new_scatter')
addEmo(':shock:', 'icon_eek')
addEmo(':fy:', 'fyou')
addEmo('[-o<', 'eusa_pray')
addEmo(':kopi:', 'kopi')
addEmo(':banana:', 'banana')
addEmo(':-s', 'eusa_eh')
addEmo(':|', 'icon_neutral')
addEmo(':scrambleup:', 'new_scrambles')
addEmo(':?', 'icon_confused')
addEmo('!peb', 'alienpeb')
addEmo('=))', 'muahaha')
addEmo('8-[', 'eusa_shifty')
addEmo(':cry:', 'icon_cry')
addEmo(':swt:', 'sweat')
addEmo('\\:D/', 'eusa_dance')
addEmo(':-|', 'icon_neutral')
addEmo(':hugs:', 'hugs')
addEmo(':sleeping:', 'new_sleeping')
addEmo(':-?', 'icon_confused')
addEmo('$2c', '2cents')
addEmo(';)', 'icon_wink')
addEmo('[-(', 'eusa_snooty')
addEmo(':evil:', 'icon_evil')
addEmo(':sweat:', 'sweat')
addEmo(':-#', 'eusa_silenced')
addEmo(':sembah:', 'nyembah')
addEmo(':fire:', 'new_ukliam2')
addEmo(':neutral:', 'icon_neutral')
addEmo(':rolleyes:', 'rolleyes')
addEmo(':cool:', 'icon_cool')
addEmo(':eek:', 'icon_surprised')
addEmo(':ace:', 'ace_ani')
addEmo(':aceheart:', 'aceheart_ani')
addEmo(':cizcuz:', 'sapi')
addEmo(':exa:', 'monyet')
addEmo(':heap:', 'stealth')
addEmo(':youfan:', 'pinguin')
addEmo(':eins:', 'puffy')
addEmo(':yinyang:', 'yinyang_ani')
addEmo(':soy:', 'soybean')
addEmo(':pompom:', 'pom-pom-girl')
addEmo(':semangat:', 'pom-pom-girl2')


#SS Emos
addEmo(':ss_UB', 'UB', '.gif', True)
addEmo(':ss_badut', 'badut', '.gif', True)
addEmo(':ss_bantai', 'bantai', '.gif', True)
addEmo(':ss_bego', 'bego', '.gif', True)
addEmo(':ss_bikingambar', 'bikingambar', '.gif', True)
addEmo(':ss_bropeace', 'bropeace', '.gif', True)
addEmo(':ss_cowcake', 'cowcake', '.gif', True)
addEmo(':ss_dansamesir', 'dansamesir', '.gif', True)
addEmo(':ss_dansa', 'dansa', '.gif', True)
addEmo(':ss_gebukin', 'gebukin', '.gif', True)
addEmo(':ss_hajar', 'hajar', '.gif', True)
addEmo(':ss_jagungletup', 'jagungletup', '.gif', True)
addEmo(':ss_kecebong', 'kecebong', '.gif', True)
addEmo(':ss_kempes', 'kempes', '.gif', True)
addEmo(':ss_kepalapecah', 'kepalapecah', '.gif', True)
addEmo(':ss_ketawagila', 'ketawagila', '.gif', True)
addEmo(':ss_ketawaserem', 'ketawaserem', '.gif', True)
addEmo(':ss_kudabeol', 'kudabeol', '.gif', True)
addEmo(':ss_mandi', 'mandi', '.gif', True)
addEmo(':ss_mules', 'mules', '.gif', True)
addEmo(':ss_ngacay', 'ngacay', '.gif', True)
addEmo(':ss_nguantuk', 'nguantuk', '.gif', True)
addEmo(':ss_sniper', 'sniper', '.gif', True)

##PLEMO emos
addEmo(':plemo_annoyed', 'pl_icons/annoyed', '.gif', True)
addEmo(':plemo_big_eyed', 'pl_icons/big_eyed', '.gif', True)
addEmo(':plemo_brokenheart', 'pl_icons/brokenheart', '.gif', True)
addEmo(':plemo_cool', 'pl_icons/cool', '.gif', True)
addEmo(':plemo_dance', 'pl_icons/dance', '.gif', True)
addEmo(':plemo_defaultsmall', 'pl_icons/defaultsmall', '.gif', True)
addEmo(':plemo_drinking', 'pl_icons/drinking', '.gif', True)
addEmo(':plemo_girlkiss', 'pl_icons/girlkiss', '.gif', True)
addEmo(':plemo_gril_toungue', 'pl_icons/gril_toungue', '.png', True)
addEmo(':plemo_hassle', 'pl_icons/hassle', '.gif', True)
addEmo(':plemo_idiot', 'pl_icons/idiot', '.gif', True)
addEmo(':plemo_laugh', 'pl_icons/laugh', '.gif', True)
addEmo(':plemo_listening_music', 'pl_icons/listening_music', '.gif', True)
addEmo(':plemo_money', 'pl_icons/money', '.gif', True)
addEmo(':plemo_nottalking', 'pl_icons/nottalking', '.gif', True)
addEmo(':plemo_private-lock', 'pl_icons/private-lock', '.png', True)
addEmo(':plemo_sad', 'pl_icons/sad', '.gif', True)
addEmo(':plemo_sick', 'pl_icons/sick', '.gif', True)
addEmo(':plemo_smile', 'pl_icons/smile', '.gif', True)
addEmo(':plemo_tears', 'pl_icons/tears', '.gif', True)
addEmo(':plemo_tongue', 'pl_icons/tongue', '.gif', True)
addEmo(':plemo_wave', 'pl_icons/wave', '.gif', True)
addEmo(':plemo_yupi', 'pl_icons/yupi', '.gif', True)
addEmo(':plemo_applause', 'pl_icons/applause', '.gif', True)
addEmo(':plemo_bringiton', 'pl_icons/bringiton', '.gif', True)
addEmo(':plemo_broken_heart', 'pl_icons/broken_heart', '.gif', True)
addEmo(':plemo_cozy', 'pl_icons/cozy', '.gif', True)
addEmo(':plemo_dancingmoves', 'pl_icons/dancemoves', '.gif', True)
addEmo(':plemo_devil', 'pl_icons/devil', '.gif', True)
addEmo(':plemo_fever', 'pl_icons/fever', '.gif', True)
addEmo(':plemo_girl_kiss', 'pl_icons/girl_kiss', '.gif', True)
addEmo(':plemo_grin', 'pl_icons/grin', '.gif', True)
addEmo(':plemo_heart', 'pl_icons/heart', '.gif', True)
addEmo(':plemo_joyful', 'pl_icons/joyful', '.gif', True)
addEmo(':plemo_likefood', 'pl_icons/likefood', '.gif', True)
addEmo(':plemo_lol', 'pl_icons/lol', '.gif', True)
addEmo(':plemo_not_talking', 'pl_icons/not_talking', '.gif', True)
addEmo(':plemo_music', 'pl_icons/music', '.gif', True)
addEmo(':plemo_rock', 'pl_icons/rock', '.gif', True)
addEmo(':plemo_scenic', 'pl_icons/scenic', '.gif', True)
addEmo(':plemo_silly_couple', 'pl_icons/silly_couple', '.gif', True)
addEmo(':plemo_startled', 'pl_icons/startled', '.gif', True)
addEmo(':plemo_thinking', 'pl_icons/thinking', '.gif', True)
addEmo(':plemo_unsure', 'pl_icons/unsure', '.gif', True)
addEmo(':plemo_wink', 'pl_icons/wink', '.gif', True)
addEmo(':plemo_angry', 'pl_icons/angry', '.gif', True)
addEmo(':plemo_bigeyed', 'pl_icons/bigeyed', '.gif', True)
addEmo(':plemo_bring_it_on', 'pl_icons/bring_it_on', '.gif', True)
addEmo(':plemo_bye', 'pl_icons/bye', '.gif', True)
addEmo(':plemo_crying', 'pl_icons/crying', '.gif', True)
addEmo(':plemo_dancing_moves', 'pl_icons/dance_moves', '.gif', True)
addEmo(':plemo_doh', 'pl_icons/doh', '.gif', True)
addEmo(':plemo_fingerscrossed', 'pl_icons/fingerscrossed', '.gif', True)
addEmo(':plemo_griltoungue', 'pl_icons/griltoungue', '.png', True)
addEmo(':plemo_gym', 'pl_icons/gym', '.gif', True)
addEmo(':plemo_hungry', 'pl_icons/hungry', '.gif', True)
addEmo(':plemo_kiss', 'pl_icons/kiss', '.gif', True)
addEmo(':plemo_like_food', 'pl_icons/like_food', '.gif', True)
addEmo(':plemo_lonely', 'pl_icons/lonely', '.gif', True)
addEmo(':plemo_nerd', 'pl_icons/nerd', '.gif', True)
addEmo(':plemo_party', 'pl_icons/party', '.gif', True)
addEmo(':plemo_metal', 'pl_icons/rock_n_roll', '.gif', True)
addEmo(':plemo_scouple', 'pl_icons/scouple', '.gif', True)
addEmo(':plemo_sleeping', 'pl_icons/sleeping', '.gif', True)
addEmo(':plemo_surprised', 'pl_icons/surprised', '.gif', True)
addEmo(':plemo_tired', 'pl_icons/tired', '.gif', True)
addEmo(':plemo_w00t', 'pl_icons/w00t', '.gif', True)
addEmo(':plemo_worship', 'pl_icons/worship', '.gif', True)

class ChatData(db.Model):
    usr = db.TextProperty()
    msg = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)

def postSystemChat(message):
    chat = ChatData()
    chat.usr = ''
    chat.msg = message
    chat.put()
    chatlist()
    return
def processMsg( usr, msg, fdate):
    msg += " "

    #html escape
    msg = msg.replace("<", "&lt;")
    msg = msg.replace("<", "&gt;")


    arr_msg = msg.split(' ', 1)

    #all first command action (/me, /tweet, etc)
    if arr_msg[0] == "/me":
        msg = "<b><span class='me'>*" + usr + " " + arr_msg[1] + "*</span></b>"
        usr = " "
    elif arr_msg[0] == "/fake": # ~username: msg (real username) (pdate style)
        if len(msg.split(' ', 2)) >= 3:
            arr_fake = msg.split(' ', 2)
            fake_usr = arr_fake[1]
            fake_msg = arr_fake[2]
            real_usr = usr

            usr = fake_usr
            msg = fake_msg + "<span class='pdate'>(" + real_usr + ")</span>"


    if usr != "" and usr != " ": #if this is not chat sys message
        msg = " : " + msg

    #all middle command (:imgbin_xxx:)
    arr_msg = msg.split(' ')
    msg = ""
    for m in arr_msg:
        raw_cmd = m.split(':')
        if len(raw_cmd) == 3: # this is a valid command, having no spaces and 2 ":"
            cmd = raw_cmd[1]
            raw_cmd2 = cmd.split('_')
            if len(raw_cmd2) == 2: # this is a valid command, having 1 "_"
                cmd_name = raw_cmd2[0]
                cmd_param = raw_cmd2[1]
                if cmd_name == "imgbin":
                    if cmd_param != "":
                        msg += " " + "<a href='http://imgbin.gamedevid.org/view/" + cmd_param + "/'><img src='http://imgbin.gamedevid.org/i/" + cmd_param + "_tn' border='0' align='none' alt='" + cmd_param + "' title='" + cmd_param + "'/></a>"
                    else:
                        msg += " " + m
            else: # this is not a valid command, treat it as normal message
                msg += " " + m
        else: # this is not a valid command, treat it as normal message
            msg += " " + m
    #emoticons (:penguin:), dan hidden (:kabur:)
    #cuman yg hidden nggak ditampilin di emo list, dan di db tagnya harus beda sama nama filenya
    #contoh untuk tag kabur, nama filenya penguinlari.gif

    for emo in arr_emo:
        msg = msg.replace(emo['c'], "<img src='/res/" + emo['i'] + "' title='" + emo['c'] + "' alt='" + emo['c'] + "'>")
    for emo in arr_emo_secret:
        msg = msg.replace(emo['c'], "<img src='/res/" + emo['i'] + "' title='Emoticon rahasia' alt='Emoticon rahasia'>")

    mention = re.compile(r"""\B@([0-9a-zA-Z_]+)""")
    hash = re.compile(r"""\B#([0-9a-zA-Z_]+)""")
    msg = mention.sub(r'@<a href="http://twitter.com/#!/\1"><b>\1</b></a>', msg)
    msg = hash.sub(r'<a href="http://twitter.com/#!/search?q=%23\1"><b>#\1</b></a>', msg)

    #parse url
    arr_msg = msg.split(' ')
    msg = ""
    for m in arr_msg:
        #if only www., then automatically add http://
        if m[:4] == "www.":
            m = "http://" + m
        word = urlparse(m)
    	scheme = word.__getattribute__('scheme');
    	if scheme == "http" or scheme == "https":
	            url_caption = word.geturl()
	            url_caption = url_caption.replace("http://", " ", 1)
	            url_caption = url_caption.replace("https://", " ", 1)
	            msg += " " + "<a href='" + word.geturl() + "'>" + url_caption + "</a>"
        else:
            msg += " " + m

    return {'usr':usr, 'msg':msg, 'date':fdate}
def chatlist(archive = False):
    limit = 30
    if archive == True:
        limit = 9999
    chats_data = db.GqlQuery("SELECT * FROM ChatData ORDER BY date DESC LIMIT 0," + str(limit)).fetch(limit, 0)
    chats = [];
    for c in chats_data:
        fdate = c.date.strftime("%m %d,%Y %H:%M:%S")
        chats.append(processMsg(c.usr, c.msg, fdate))

    output = template.render('chatlist.html', {'chats' : chats})
    if archive == True:
        return output
    chatUpdate = {
                  'return_type' : 'chatlist',
                  'data' : output
                  }
    chats_json = simplejson.dumps(chatUpdate)

    import libuser
    users = libuser.getAliveUsers()
    for user in users:        
        client_id = user['client_id']# later change this to client id                    
        try:
            channel.send_message(client_id, chats_json)
        except channel.InvalidChannelClientIdError:
            pass
    return

    

def postChat(username, message):
    chat = ChatData()
    chat.usr = username
    chat.msg = message
    chat.put()    
    
    return 0