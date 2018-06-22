# -*- coding: UTF-8 -*-
'''
Created on 2018��6��21��

@author: taihao
'''
from www import orm
import asyncio
from www.models import User

def test():
    yield from orm.create_pool(user='root',password='123456',database='awesome', host='127.0.0.1',)
    u=User(name='Test',email='test@example.com',passwd='12343333',image='about:blank',id="100")
    yield from u.save()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(test()))
loop.close()