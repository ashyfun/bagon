class BotTokenNotSet(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = 'Bot token not set. Check .env file and try again.'

    def __str__(self):
        return self.message
