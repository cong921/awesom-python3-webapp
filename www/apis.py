# -*- coding: UTF-8 -*-
'''
Created on 2018年6月26日

@author: taihao
'''
'''
JSON API definition.
'''

class APIError(Exception):
    '''
    the base APIError which contains error(required),data(optional) and message(optional).
    '''
    def __init__(self,error,data='',message=''):
        super(APIError,self).__init__(message)
        self.error=error
        self.data=data
        self.message=message
        
class APIValueError(APIError):
    
    '''
    Indicate the input value has error or invalid.The data specifies the error field of input form.
    '''
    def __init__(self,field,message=''):
        super(APIValueError,self).__init__('value:invalid',field,message)
        
class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found.The data specifies the resource name.
    '''
    def __init__(self,field,message=''):
        super(APIResourceNotFoundError,self).__init('value:notfound',field,message)
class APIPermissionError(APIError):
    '''
    Indicate the api has no permisssion.
    '''
    def __init__(self,message=''):
        super(APIPermissionError,self).__init__('permission:forbidden', 'permission', message)
    