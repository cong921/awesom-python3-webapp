#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lnb
# @Date:   2018-04-21 12:26:58
# @Last Modified by:   Lnb
# @Last Modified time: 2018-04-21 21:32:05
from orm import Model,StringField,IntegerField


class User(Model):
    __table__='users'

    id=IntegerField(primary_key=True)
    name=StringField()
    __init__():
        #创建实例
        user=User(id=123,name='Michael')
        #存入数据库:
        user.insert()
        #查询所有User对象
        users=User.findAll()
        user=yield from User.find('123')
        user=User(id=123,name='Michael')
        yield from user.save()
