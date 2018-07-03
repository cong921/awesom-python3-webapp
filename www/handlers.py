# -*- coding: UTF-8 -*-
'''
Created on 2018年6月26日

@author: taihao
'''
from www.models import User, Blog, next_id
from www.coroweb import get, post
import asyncio
import time
from www.apis import APIValueError, APIError
import hashlib
import re
from aiohttp import web
import json
from www.config import configs
import logging
from www.user import user
' urlhandlers '

@get('/')
async def index(request):
    summary='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tepor incididunt ut labore et dolore magna aliqua.'
    blogs=[
        Blog(id='1',name='Test Blog',summary=summary,created_at=time.time()-120),
        Blog(id='2',name='Something New',summary=summary,created_at=time.time()-3600),
        Blog(id='3',name='Learn Swift',summary=summary,created_at=time.time()-7200)
        ]
    return {
        '__template__':'blogs.html',
        'blogs':blogs
        }

_RE_EMAIL=re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1=re.compile(r'^[0-9a-f]{40}$')
    
@get('/api/users')
async def api_get_users():
    users=await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passw='******'
    return dict(users=users)
 
COOKIE_NAME = 'AwEsOmE' 
_COOKIE_KEY = configs.session.secret

def user2cookie(user,max_age):
    '''
    Generate cookie str by user.
    '''
    #build cookie string by : id-expires-sha1
    expires = str(int(time.time()+max_age))
    s='%s-%s-%s-%s' % (user.id,user.passwd,expires,_COOKIE_KEY)
    L=[user.id,expires,hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L=cookie_str.split('-')
        if len(L)!=3:
            return None
        uid,expires,sha1=L
        if int(expires)<time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s='%s-%s-%s-%s' % (uid,user.passwd,expires,_COOKIE_KEY)
        if sha1!=hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd='******'
        return user
    except Exception as e:
        logging.info(e)
        return None
    
    
@post('/api/users')   
async def api_register_user(*,email,name,passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users=await User.findAll('email=?', [email])
    if len(users)>0:
        raise APIError('register:failed','email','Email is already in use.')
    uid=next_id()
    sha1_passwd='%s:%s' % (uid,passwd)
    user=User(id=uid,name=name.strip(),email=email,passwd=hashlib.sha1(sha1_passwd.encode('utf-8'))).hexdigest(),image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest()
    await user.save()
    #make session cookie:
    r=web.Response()
    r.set_cookie(COOKIE_NAME,user2cookie(user,86400), max_age=86400,httponly=True)
    user.passwd='******'
    r.content_type='application/json'
    r.body=json.dumps(user,ensure_ascii=False).encode('utf-8')
    return r
@post('/api/authenticate')    
async def authenticate(*,email,passwd):
    if not email:
        raise APIValueError('email','Invalid email.')
    if not passwd:
        raise APIValueError('passwd','Invalid passwd.')
    users=await User.findAll('email=?',[email])
    if len(users)==0:
        raise APIValueError('email','Email not exist.')
    user=users[0]
    #check passwd:
    sha1=hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd!=sha1.hexdigest():
        raise APIValueError('passwd','Invalid password.')
    #authenticate ok, set cookie:
    r=web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400),max_age=86400,httponly=True)
    user.passwd='******'
    r.content_type='application/json'
    r.body=json.dump(user, ensure_ascii=False).encode('utf-8')
    return r

async def auth_factory(app,handler):
    async def auth(request):
        logging.info('check user: %s %s' % (request.method,request.path))
        request.__user__=None
        cookie_str=request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user=await cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__=user
        return (await handler(request))
    return auth

