from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.encoding import force_unicode


def decimal_to_real(value, precision=2):
    '''
    Receives a Decimal instance and returns a string formatted as brazilian Real currency:
    12,234.00. Without the "R$".
    '''
    value = floatformat(value, precision)
    value, decimal = force_unicode(value).split('.')
    value = intcomma(value)
    value = value.replace(',', '.') + ',' + decimal
    return value
