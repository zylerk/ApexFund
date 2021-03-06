

class BaseClass():
    """description of class"""
    STATE_OK = 1
    STATE_ERROR = -1    

    def __init__(self, **kwargs):
        self.state = 'ok'                        
        return super().__init__(**kwargs)

    def ok(self):
        self.state = 'ok'
        return BaseClass.STATE_OK

    def error(self, err_msg=None):
        if err_msg:
            self.state = err_msg
        return BaseClass.STATE_ERROR