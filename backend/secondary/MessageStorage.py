class MessageStorage:

    def __init__(self):
        self.messages = dict()

    def append(self, key, message):
        self.messages[key] =  message
        self.messages = dict(sorted(self.messages.items()))

    def length(self):
        return len(self.messages.keys())

    def get_all(self):
        res = dict()
        for key, val in self.messages.items():
            if key not in res.keys():
                res[key] = val

        return res




