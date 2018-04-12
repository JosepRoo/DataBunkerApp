class Response(object):
    def __init__(self, success, records=0, data=None, msgResponse=None):
        self.success = success
        self.records = records
        self.data = data
        self.msgResponse = msgResponse

    def json(self):
        return {'success': self.success,
                'records': self.records,
                'data': self.data,
                'msgResponse': self.msgResponse
                }
