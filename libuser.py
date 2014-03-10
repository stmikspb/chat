from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import channel
from google.appengine.api import memcache
from django.utils import simplejson
import re
import datetime
import string
import oauth
import urllib
from urlparse import urlparse

import libchat

def getAliveUsers(username = "", token = ""): #optional params to get specific data
    data = memcache.get("aliveusers")
    if data is not None:
        ndata = data
    else:
        #Memcache for this set is empty, create a new one
        ndata = []
    
    sdata = [] #specific data
    if username != "":
        for user in ndata:
            if user['username'] == username:
                sdata.append(user)
    if token != "":
        for user in ndata:
            if user['token'] == token:
                sdata.append(user)
    if len(sdata) > 0:
        return sdata
    
    return ndata
def getAliveUsersSpecific(data, username = "", token = ""):
    sdata = [] #specific data
    if username != "":
        for user in data:
            if user['username'] == username:
                sdata.append(user)
    if token != "":
        for user in data:
            if user['token'] == token:
                sdata.append(user)

    return sdata
def writeAliveUsers(ndata):
    memcache.set(key="aliveusers",value=ndata)
    return
def appendAliveUsers(username):
    created = datetime.datetime.now()
    last_updated = created
    client_id = username + str(created)
    token = channel.create_channel(client_id)
    nuser = {
        'username':username,
        'token':token,
        'created':created,
        'last_updated' :last_updated,
        'client_id':client_id
        }
    
    data = getAliveUsers()
    data.append(nuser)
    writeAliveUsers(data)
    return token

def pingUser(user_token):
    users = getAliveUsers()
    for user in users:
        if user['token'] == user_token:
            user['last_updated'] = datetime.datetime.now()
    writeAliveUsers(users)
    return
    
def listAliveUsers(users = None):
    if users is None:
        users = getAliveUsers()
    arr_users = []
    for user in users:
        found = False
        tmp_username = user['username']
        if tmp_username == "__anonymous":
            tmp_username = "(Anonymous)"
        for a in arr_users:
            if a['usr'] == tmp_username:
                a['ch'] += 1
                found = True
        if found == False:
            arr_users.append({'usr':tmp_username, 'ch':1})
            
    output = template.render('userlist.html', {'users' : arr_users})        
    output_users = {
                    'return_type' : 'userlist',
                    'data' : output
                    }
    users_json = simplejson.dumps(output_users)
    for user in users:        
        client_id = user['client_id']# later change this to client id                    
        try:
            channel.send_message(client_id, users_json)
        except channel.InvalidChannelClientIdError:
            pass

def cronUpdateAliveUsers():
    #delete zombie channel, update non zombie channel
    changes = False
    users = getAliveUsers()
    for user in users:
        diff_sec = (datetime.datetime.now() - user['last_updated']).seconds
        if diff_sec > 60 * 1:
            changes = True
            usr_ch_count = len(getAliveUsersSpecific(users,username=user['username']))
            if user['username'] != "__anonymous":
                if usr_ch_count == 1:
                    
                    chat = libchat.ChatData()
                    chat.usr = ''
                    chat.msg = user['username'] + " left the chat (request timed out)"
                    chat.date = user['last_updated']
                    chat.put()                    
            users.remove(user)
    if changes == True:
        writeAliveUsers(users) # later, if no changes, don't perform this task
        listAliveUsers(users)
    return

def logout(username):
    users = getAliveUsers()
    for user in users:
        if user['username'] == username:
            users.remove(user)
    writeAliveUsers(users)
    return

def join(nickname):
    token = appendAliveUsers(nickname)
    return token