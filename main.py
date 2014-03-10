from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import channel
from django.utils import simplejson
import re
import datetime
import string
import oauth
import urllib
from urlparse import urlparse

import libchat
import libuser

application_key = "WLdDqBExrTh7QRrbRNSBvA"
application_secret = "mjcpGlsArr1oqd0GxNeh1kQuzyBn3I7GwPmHIME"
user_token = "FILL_IN"
user_secret = "FILL_IN"
#host = "http://localhost:9005"
host = "http://stmikspbchat.appspot.com"
callback = "%s/verify" % host


#pindah ke latest oauth
#support login via yahoo, (fb?)
#di db ActiveUsers tambah field "acc_type" (twitter, yahoo, etc)
#di tiap msg chatlist, kasih icon disebelah username, icon acc_type (twitter,yahoo, etc)
#di daftar online user, kasih icon acc_type jg
#kasih command untuk ngepost status ke twit/yahoo/etc
#commandnya satu aja, /post "text here", yg nanti bakal detect acc_type dan ngepost ke service yg tersedia

#dropdown buat pengganti msg textfield, jadi past chat bisa dipilih lagi

#public todo:
#bisa login pake yahoo,fb(?), tiap ngechat bisa keliatan loginnya pakai apa (ada icon service, kecil disebelah kiri/kanan username)
#bisa ngepost ke status (yahoo,twitter,fb(?)) pake command /post


class ClientPing(webapp.RequestHandler):
    def post(self):
        user_token = self.request.get('token');
        libuser.pingUser(user_token)
        return

class CronActiveUsersUpdate(webapp.RequestHandler):
    def get(self):
        libuser.cronUpdateAliveUsers()
class ListAliveUsers(webapp.RequestHandler):
    def get(self):
        libuser.listAliveUsers()

class ChatPost(webapp.RequestHandler):
    def post(self):
        client = oauth.GDIClient(application_key, application_secret, callback, self)
        if client.get_cookie():
            if self.request.get('message') != "":
                username = client.get_cookie_username()
                libchat.postChat(username, self.request.get('message'))
        libchat.chatlist()
class ChatArchive(webapp.RequestHandler):
    def get(self):        
        self.response.out.write(libchat.chatlist(True))

class ChatExit(webapp.RequestHandler):
    def get(self):
        client = oauth.GDIClient(application_key, application_secret, callback, self)
        username = client.get_cookie_username()
        libuser.logout(username)
        libchat.postSystemChat(username + " left the chat (log out via GDI Account)")
        client.expire_cookie()
        return self.redirect("/")
        
class IFrameSample(webapp.RequestHandler):
    def get(self):
        output = template.render('iframesample.html', {'host':host})
        self.response.out.write(output)
        
class MainPage(webapp.RequestHandler):
    def get(self, mode = ""):

        #client = pythontwitter.OAuthClient('twitter', self)       
        client = oauth.GDIClient(application_key, application_secret, callback, self)
        if mode == "login":
            return self.redirect(client.get_authorization_url())
        if mode == "verify":
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier = auth_verifier)
            return self.redirect("/")

        nickname = ""
        new_token = ""
        if client.get_cookie():
            #info = client.get('/account/verify_credentials')
            #nickname = info['screen_name']
            nickname = client.get_cookie_username()
        else:
            nickname = "__anonymous"
        
        new_token = libuser.join(nickname)

        

        #case: gw close tab, 3 menit lalu RTO, trus buka lagi, nggak ada message " has joined the chat"
        #harusnya ada message "gw has left the chat (last_updated)"
        #trus dibawahnya ada message "gw has joined the chat (waktu sekarang)"
        #penyebab: karna region dibawah ini dipanggil duluan sebelum ping
        #jadi sementara channel gw yg harusnya RTO masih ada di db, MainPage jg nambah 1 row
        #baru yaitu channel baru gw. dengan total lebih dari 1 channel, conditional statetement dibawah
        #gak bakal dieksekusi

        #gimana caranya mekanisme ping dibagian ngedelete zombie channel bisa di eksekusi lebih dulu
        #sebelum region dibawah ini jalan. solusi: pisahkan fungsi delete zombie channel di kelas ping
        #lalu panggil disini
        
        if nickname != "__anonymous":
            usr_ch_count = len(libuser.getAliveUsers(username=nickname))
            if usr_ch_count == 1:
                libchat.postSystemChat(nickname + " has joined the chat")


        

        output = template.render('index.html', {'new_nickname' : nickname, 'new_token' : new_token, 'arr_emo' : libchat.arr_emo})

        self.response.out.write(output)

application = webapp.WSGIApplication(
                                     [
                                      ('/_activeusersupdate',CronActiveUsersUpdate),
                                      ('/_listaliveusers',ListAliveUsers),                                      
                                      ('/ping', ClientPing),
                                      ('/archive', ChatArchive),
                                      ('/logout', ChatExit),
                                      ('/chatpost', ChatPost),
                                      ('/iframesample', IFrameSample),
                                      ('/(.*)', MainPage)],
                                     debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
