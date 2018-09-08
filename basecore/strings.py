from django.utils.translation import ugettext_lazy as _
from dataclean.settings import get_element_settings


class ConsStr(object):
    message = 'message'
    status = 'status'
    http_created = 201
    http_not_implemented = 501
    none = None
    int_cero = 0
    off_cero = 0
    utf8 = 'utf-8'
    str_void = ''
    str_space = ''
    meth_get = 'GET'
    bool_true = True
    bool_false = False
    meth_post = 'POST'
    dispatch = 'dispatch'
    domain_front = get_element_settings('DNS', 'DNS_FRONTEND')


class Strings(object):
    type_error = _('ERROR')
