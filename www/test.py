# -*- coding: UTF-8 -*-
'''
Created on 2018��6��21��

@author: taihao
'''
import orm
from models import User, Blog, Comment
import asyncio

def test():
    yield from orm.create_pool(user='root',password='123456',database='awesome')
    u=User(name='Test',email='test@example.com',passwd='12343333',image='about:blank')
    yield from u.save()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(test()))
loop.close()