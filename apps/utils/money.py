# -*- coding: utf-8 -*-

import locale


def normalize_money(data):
    data = data.replace(".", "")
    data = data.replace(",", ".")
    return data


def money_format(value):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    value = locale.currency(value, grouping=True, symbol=False)
    return "R$ {0}".format(value)
