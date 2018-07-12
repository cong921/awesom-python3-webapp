# -*- coding: UTF-8 -*-
'''
Created on 2018锟斤拷6锟斤拷21锟斤拷

@author: taihao
'''

import asyncio
from www.models import Blog
import orm
async def test(loop):
    __pool=await orm.create_pool(loop,user='root',password='123456',db='awesome')
    blog=await Blog.find('0015308596041480350c664940b4db49d672cf97094abd8000')
    print(blog.name)
    await blog.remove()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()    