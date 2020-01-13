'''
    return Json models
'''
import json

class ReCode(object):

    def error_func(self,status,error,message,timetamp: str):
        
        data = {
            "status":status,  # 状态
            "error":error,  # 错误提示
            "message":message,  # 信息
            "timetamp":timetamp,  # 时间
        }
        return data

    def success_func(self,message: str,data: dict,timetamp: str):

        re_data = {
            "status":1,
            "message":"操作成功",
            "data":data,
            "timetamp":timetamp
        }
        return re_data