# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.filter(name="icon_label")
def icon_label(value):
    icons = {
        "open": "icon-circle-blank",
        "working": "icon-play",
        "closed": "icon-lock",
        "waiting_user": "icon-user",
        "waiting_client": "icon-shield",
        "waiting_resources": "icon-tasks",
        "waiting_supplier": "icon-group"
    }
    return icons.get(value)


@register.filter(name="badge_color")
def badge_color(value):
    colors = {
        "open": "info",
        "working": "success",
        "closed": "primary",
        "waiting_user": "warning",
        "waiting_client": "warning",
        "waiting_resources": "warning",
        "waiting_supplier": "warning"
    }
    return colors.get(value, "default")
