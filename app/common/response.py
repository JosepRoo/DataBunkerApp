class Response(object):
    def __init__(self, success, records=0, data=None, msg_response=None):
        self.success = success
        self.records = records
        self.data = data
        self.msg_response = msg_response

    def json(self):
        return {'success': self.success,
                'records': self.records,
                'data': self.data,
                'msg_response': self.msg_response
                }
