#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lnb
# @Date:   2018-04-21 16:59:18
# @Last Modified by:   Lnb
# @Last Modified time: 2018-04-21 17:34:14
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        # 排除Model类本身:
        if name='Model':
            return type.__new__(cls,name,bases,attrs)

        tableName=attrs.get('__table__',None) or name
        logging.info('found model:%s (table:%s'%(name,tableName))

        mappings=dict()
        fields=[]
        primary_key=None
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info(' found mapping:%s==>%s'%(k,v))
                mappings[k]=value
                if v.primary_key:

                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field:%s'%k)
                    primaryKey=key
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields=list(map(lambda f:'`%s`'%f, fields))
        attrs['__mappings__']=mappings #保存属性和列的映射关系
        attrs['__table__']=tableName
        attrs['__primary_key']=primaryKey
        attrs['__fields__']=fields
        attrs['__select__']='select `%s`,%s from `%s`'%(primaryKey,','.join(escaped_fields),tableName)
        attrs['__insert__']='insert into `%s` (%s,`%s`) values (%s)'%(tableName,','.join(escaped_fields),primaryKey,create_args_string(len(escaped_fields)+1))
        attrs['__update__']='update `%s` set %s where `%s`=?'%(tableName,','.join(map(lambda f:'`%s`=?'%(mappings.get(f).name or f),fields)),primaryKey)
        attrs['__delete__']='delete from `%s` where `%s`=?'%(tableName,primaryKey)
        return type.__new__(cls,name,bases,attrs)
