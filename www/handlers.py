# -*- coding: UTF-8 -*-
'''
Created on 2018年6月26日

@author: taihao
'''
from www.user import User
from www.coroweb import get
' urlhandlers '

@get('/')       
def index(request):
    users=yield from User.findAll()
    return {
        '__template__':'test.html',
        'users':users
        }