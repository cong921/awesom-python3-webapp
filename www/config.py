# -*- coding: UTF-8 -*-
'''
Created on 2018年6月28日

@author: taihao
'''
import config_default
configs=config_default.configs

class Dict(dict):
    
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self,name=(),values=(),**kw):
        super(Dict,self).__init__(self,**kw)
        for k,v in zip(name,values):
            self[k]=v
        
    def __getattr__(self,key):    
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    
    def __setattr__(self,key,value):
        self[key]=value
def merge(default,override):    
    r={}
    for k,v in default.items():
        if k in override:
            if isinstance(v, dict):
                r[k]=merge(v,override[k])
            else:
                r[k]=v
        else:
            r[k]=v
    return r  
def toDict(d):
    D=Dict()
    for k, v in d.items():
        D[k]=toDict(v) if isinstance(v,dict) else v
    return D
try:
    import config_override
    configs=merge(configs,config_override.configs)
except ImportError:
    pass
configs=toDict(configs)