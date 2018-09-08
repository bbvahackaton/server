import logging
import re
import json
import sys
from builtins import object

from django.db import connection
from django.http import JsonResponse

status = 200

logger = logging.getLogger('server')


class Store(object):
    def execute(self):
        statement = self.convert_to_statement()
        cursor = connection.cursor()
        try:
            cursor.execute("BEGIN")
            cursor.execute(statement)
            results_sql = cursor.fetchall()
            if len(results_sql) == 0:
                results_sql = []
            else:
                results_sql = results_sql[0][0]
                if results_sql is None:
                    results_sql = []
            cursor.execute("COMMIT")
        finally:
            cursor.close()
        return results_sql

    def convert_to_statement(self):
        var_names = self.get_variables_names()
        atributes = self.__dict__
        body = ""
        for var in var_names:
            body = body + "'" + str(atributes[var]).replace("'", "''") + "',"
        body = "SELECT " + self.__class__.__name__.lower() + "(" \
               + body[:-1] + ")"
        print(body)
        # logger.info(body)
        return body

    def get_variables_names(self):
        attributes = self.__dict__
        var_names = []
        for var_name in attributes:
            if not (
                    var_name[0].startswith('__') and var_name[0].endswith(
                '__')):
                var_names.append(var_name)
        var_namex = []
        r = re.compile('^[a-z]{3}_[a-z]{6}')
        for var_name in var_names:
            if r.match(var_name):
                var_namex.append(var_name)
        return var_namex

    def notificate(self, data, room):
        import sys
        event = sys._getframe(1).f_code.co_name
        mensaje = self.get_element(data, 'mensaje')
        data = self.del_element(data, 'mensaje')
        type = self.get_type(data)
        data = self.del_element(data, 'type')
        logger.info(mensaje, extra={'socket': event, 'room': room,
                                    'data': data, 'type': type})

    @staticmethod
    def get_element(data, element):
        if element in data:
            element = data[element]
        else:
            element = ''
        return element

    @staticmethod
    def del_element(data, element):
        if element in data:
            del data[element]
        return data

    @staticmethod
    def get_type(data):
        if 'type' in data:
            type = data['type']
            if type == '1':
                type = 'SUCCESS'
            if type == '2':
                type = 'INFO'
        else:
            type = ''
        return type

    @staticmethod
    def notificate_error(message, room):
        import sys
        event = sys._getframe(1).f_code.co_name
        logger.error(message)
        data = "Ha ocurrido un error."
        logger.error(data, extra={'socket': event, 'room': room})


class BaseView(object):
    from django.contrib.auth.decorators import login_required
    logger = logging.getLogger('dataclean')
    decorators = [login_required]

    @staticmethod
    def response(data, statux=status):
        return JsonResponse(data, safe=False, status=statux)

    class Meta:
        abstract = True


class Constantes:
    logger = logging.getLogger('server')
    str_vacio = ""

    array_vacio = []


class ManagerView(Constantes, object):
    @staticmethod
    def response_client(type_, message):
        response = JsonResponse({
            'message': message,
            'type': type_
        })
        if type_ == 'ERROR':
            response.status_code = 400
        return response

    @staticmethod
    def response(data, statux=status):
        if data is None:
            data = []
        return JsonResponse(data, safe=False)

    def response_error(self, error):
        import traceback
        error_list = []
        for error_ in error.args:
            error_list.append(error_)
            logger.error(error_)
        data = {'error_msg': error_list, 'trace': self.clear_traceback(traceback.format_exc())}
        return JsonResponse(data, safe=False)

    @staticmethod
    def clear_traceback(traceback):
        new_traceback = []
        for trace in traceback.split('\n'):
            trace = trace.strip()
            if trace != '':
                new_traceback.append(trace)
        return new_traceback

    @staticmethod
    def get_content_query(query, objeto, offset=None):
        if len(query.getlist(objeto)) > 0:
            if offset is not None:
                return query.getlist(objeto)[offset]
            else:
                return json.dumps(query.getlist(objeto))
        else:
            return ""
