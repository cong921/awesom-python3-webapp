# -*- coding: UTF-8 -*-
'''
Created on 2018年6月26日

@author: taihao
'''
from www.user import User
from www.coroweb import get
import asyncio
' urlhandlers '

@get('/')
async def index(request):
    users=await User.findAll()
    return {
        '__template__':'test.html',
        'users':users
        }