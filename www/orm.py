#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lnb
# @Date:   2018-04-21 12:26:58
# @Last Modified by:   Lnb
# @Last Modified time: 2018-04-21 22:09:00
# 
import asyncio,logging
import aiomysql
@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool=yield from aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf-8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
        )

@asyncio.coroutine
def select(sql,args,size=None):
    log(sql,args)
    global __pool
    with (yield from __pool) as conn:
        cur=yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs=yield from cur.fetchmany(size)
        else:
            rs=yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned:%s'%len(rs))
        return rs

@asyncio.coroutine
def execute(sql,args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur=yield from conn.cursor()
            yield from cur.execute(sql.replace('?','%s'),args)
            affected=cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected

class Model(dict,metaclass=ModelMetaclass):

    def __init__(self,**kw):
        super(Model,self).__init__(**kw)

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'"%key)

    def __setattr__(self,key,value):
        self[key]=value

    def getValue(self,key):
        return getattr(self,key,None)

    def getValueOrDefault(self,key):
        value=getattr(self,key,None)
        if value is None:
            field=self.__mappings__[key]
            if field.default is not None:
                value=field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s:%s'%(key,str(value)))
        return value
    @classmethod
    @asyncio.coroutine
    def find(cls,pk):
        ' find object by primary key.'
        rs=yield from select ('%s where `%s`=?'%(cls.__select__,clas.__primary_key__),[pk],1)
        if(len(rs)==0):
            return None
        return cls(**rs[0])

    @asyncio.coroutine
    def save(self):
        args=list(map(self.getValueOrDefault,self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows=yield from execute(self.__insert__,args)
        if rows!=1:
            logging.warn('failed to insert record:affected rows:%s'% rows)

    @asyncio.coroutine
    def findAll(cls,where=None,args=None,**kw):
        ' find objects by where clause.'
        sql=[cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args=[]
        orderBy=kw.get('orderBy',None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit=kw.get('limit',None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit,int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit,tuple) and len(limit)==2:
                sql.append('?,?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value:%s'%str(limit))
        rs=await select(''.join(sql),args)
        return [cls(**r) for r in rs]

    @asyncio.coroutine
    def findNumber(cls,selectField,where=None,args=None):
        ' find number by select and where.'
        sql=['select %s _num_ from `%s`'%(selectField,cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs=await select(''.join(sql),args,1)
        if len(rs)==0:
            return None
            return rs[0]['_num_']

    @asyncio.coroutine
    def update(self):
        args=list(map(self.getValue,self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows=await execute(self.__update__,args)
        if rows!=1:
            logging.warn('failed to update by primary key:affected rows:%s'%rows)
    @asyncio.coroutine
    def remove(self):
        args=[self.getValue(self.__primary_key__)]
        rows=await execute(self__delete__,args)
        if rows!=1:
            logging.warn('failed to remove by primary key: affected rows:%s'%rows)

class Field(object):

    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default

    def __str__(self):
        return '<%s,%s:%s>'%(self.__class__.__name__,self.column_type,self.name)

class StringField(Field):

    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100'):
        super().__init__(name,ddl,primary_key,default)
