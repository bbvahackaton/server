from django.views.generic import View

from basecore.models import BaseView, ManagerView
from inegi.action import Action

class InegiView(BaseView, View):

    @staticmethod
    def get_data_from_inegi(request, **kwargs):
        manager = ManagerView()
        try:
            action = Action()
            id_pyme = kwargs.get('id_pyme')
            data = action.get_data_from_inegi(id_pyme)
            response = manager.response(data)
        except Exception as error:
            response = manager.response_error(error)
        return response
