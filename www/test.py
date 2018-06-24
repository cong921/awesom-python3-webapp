# -*- coding: UTF-8 -*-
'''
Created on 2018��6��21��

@author: taihao
'''
import asyncio
from www.models import User
from www import orm
async def test():
    await orm.create_pool(user='root',password='123456',database='awesome')
    u=User(name='Test',email='test@example.com',passwd='12343333',image='about:blank',id="100")
    await u.save()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(test()))
loop.close()    