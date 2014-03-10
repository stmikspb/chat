#!/usr/bin/env python
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users

import libchat
import libuser

import facebook
import os.path





application_key = "WLdDqBExrTh7QRrbRNSBvA"
application_secret = "mjcpGlsArr1oqd0GxNeh1kQuzyBn3I7GwPmHIME"
user_token = "FILL_IN"
user_secret = "FILL_IN"
#host = "http://localhost:8080"
host = "http://stmikspbchat.appspot.com"
callback = "%s/verify" % host

#todo: setiap ping, atau buat ping baru dengan interval yg lebih besar (tiap 5 menit misalnya)
#di tiap ping tsb, cek new thread/reply di stmikspbchat, dari rss mungkin, klo ada yg baru, broadcast

#pindah ke latest oauth
#support login via yahoo, stmikspbchat-acc, (fb?)
#di db ActiveUsers tambah field "acc_type" (twitter, yahoo, etc)
#di tiap msg chatlist, kasih icon disebelah username, icon acc_type (twitter,yahoo, etc)
#di daftar online user, kasih icon acc_type jg
#kasih command untuk ngepost status ke twit/yahoo/etc
#commandnya satu aja, /post "text here", yg nanti bakal detect acc_type dan ngepost ke service yg tersedia

#dropdown buat pengganti msg textfield, jadi past chat bisa dipilih lagi

#public todo:
#tiap ada reply/post baru di stmikspbchat, broadcast linknya ke chat (kayak fb newsfeed)
#bisa login pake yahoo,fb(?), dan stmikspbchat-account.appspot.com,tiap ngechat bisa keliatan loginnya pakai apa (ada icon service, kecil disebelah kiri/kanan username)
#bisa ngepost ke status (yahoo,twitter,fb(?)) pake command /post
FACEBOOK_APP_ID = "295375653836119"
FACEBOOK_APP_SECRET = "c7825cfedfeba3b48c5672d7c8bee5b8"

class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
class BaseHandler(webapp.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(
                    self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                            id=str(profile["id"]),
                            name=profile["name"],
                            profile_url=profile["link"],
                            access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        return self._current_user


class HomeHandler(BaseHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "example.html")
        args = dict(current_user=self.current_user,
                facebook_app_id=FACEBOOK_APP_ID)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.out.write(template.render(path, args))

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

class ChatPost(BaseHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if self.request.get('message') != "":
                username = user.nickname()
                libchat.postChat(username, self.request.get('message'))
        libchat.chatlist()
class ChatArchive(webapp.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'        
        self.response.out.write(libchat.chatlist(True))

class ChatExit(BaseHandler):
    def get(self):
        args = dict(current_user=self.current_user,
                facebook_app_id=FACEBOOK_APP_ID)
        #client = oauth.GDIClient(application_key, application_secret, callback, self)
        #username = client.get_cookie_username()
        username = args['current_user'].name
        libuser.logout(username)
        libchat.postSystemChat(username + " left the chat")
        #client.expire_cookie()
        return self.redirect("/")

class IFrameSample(webapp.RequestHandler):
    def get(self):
        output = template.render('iframesample.html', {'host':host})
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.out.write(output)

class MainPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = None
        if user:
            nickname = user.nickname()
        else:
            nickname = "__anonymous"
            login_url = users.create_login_url()
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




        output = template.render('index.html', {'login_url': login_url, 'new_nickname' : nickname, 'new_token' : new_token, 'arr_emo' : libchat.arr_emo, 'facebook_app_id' : FACEBOOK_APP_ID})
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        self.response.out.write(output)

application = webapp.WSGIApplication(
        [
            (r'/_activeusersupdate',CronActiveUsersUpdate),
            (r'/_listaliveusers',ListAliveUsers),                                      
            (r'/ping', ClientPing),
            (r'/archive', ChatArchive),
            (r'/logout', ChatExit),
            (r'/chatpost', ChatPost),
            (r'/iframesample', IFrameSample),
            (r'/', MainPage)],

        debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
