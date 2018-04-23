class Response(object):
    def __init__(self, success=False, msg_response=None):
        self.success = success
        self.msg_response = msg_response

    def json(self):
        return {'success': self.success,
                'msg_response': self.msg_response
                }
