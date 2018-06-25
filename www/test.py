# -*- coding: UTF-8 -*-
'''
Created on 2018锟斤拷6锟斤拷21锟斤拷

@author: taihao
'''
import asyncio
from www.models import User
from www import orm
from aiomysql import pool
async def test(loop):
    await orm.create_pool(loop,user='root',password='123456',db='awesome')
    u=User(name='Test',email='test1@example.com',passwd='12343333',image='about:blank',id="101")
    await u.save()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()    