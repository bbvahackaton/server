"""
Se basó de la siguiente fuente
https://docs.djangoproject.com/en/1.11/_modules/django/utils/log/
"""
import logging

from django.conf import settings
from django.core.management.color import color_style
from django.utils.translation import override as ov


class RequireEnvTrue(logging.Filter):
    """
    """

    def filter(self, record):
        return settings.ENV


class ServerFormatter(logging.Formatter):
    """
    Formateador
    """

    def __init__(self, *args, **kwargs):
        self.style = color_style()
        super(ServerFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        msg = record.msg
        status_code = getattr(record, 'status_code', None)

        if status_code:
            if 200 <= status_code < 300:
                # Put 2XX first, since it should be the common case
                msg = self.style.HTTP_SUCCESS(msg)
            elif 100 <= status_code < 200:
                msg = self.style.HTTP_INFO(msg)
            elif status_code == 304:
                msg = self.style.HTTP_NOT_MODIFIED(msg)
            elif 300 <= status_code < 400:
                msg = self.style.HTTP_REDIRECT(msg)
            elif status_code == 404:
                msg = self.style.HTTP_NOT_FOUND(msg)
            elif 400 <= status_code < 500:
                msg = self.style.HTTP_BAD_REQUEST(msg)
            else:
                # Any 5XX, or any other status code
                msg = self.style.HTTP_SERVER_ERROR(msg)

        if self.uses_server_time() and not hasattr(record, 'server_time'):
            record.server_time = self.formatTime(record, self.datefmt)

        record.msg = msg
        return super(ServerFormatter, self).format(record)

    def uses_server_time(self):
        """
        Obtiene el tiempo del servidor.
        """
        return self._fmt.find('%(server_time)') >= 0


class RequireSocketTrue(logging.Filter):
    """
    Valida si se enviará el log al usuario a través de sockets.
    """

    def filter(self, record):
        return getattr(record, 'socket', False)


class RequiereLogTrue(logging.Filter):
    """
    Filtro que se usa para saber si se guarda el log en los archivos logs
    """

    def filter(self, record):
        if not record.msg:
            return False
        return True


class FileFormatter(logging.Formatter):
    """
    Para traducir el idioma en ingles
    """

    def __init__(self, *args, **kwargs):
        self.style = '%'
        super(FileFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        msg = record.msg
        with ov('en'):
            record.msg = msg
        return super(FileFormatter, self).format(record)
