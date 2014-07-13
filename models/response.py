class Response:
    def __init__(self):
        self.error = True
        self.message = ''
        self.data = False

    def add_data(self, data):
        self.error = False
        self.data = data

    def add_error_message(self, message):
        self.error = True
        self.data = False
        self.message = message

    def as_dict(self):
        return {
            'error': self.error,
            'message': self.message,
            'data': self.data
        }