from .client import Client


class Action(object):

    def __init__(self):
        self.client = Client()

    def get_data_from_inegi(self, id_pyme):
        return self.client.get_data_from_inegi(id_pyme)
