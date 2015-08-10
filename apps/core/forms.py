# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Ticket, Sla, Status


class TicketForm(forms.ModelForm):

    sla = forms.ModelChoiceField(
        queryset=Sla.objects.all(),
        empty_label=_("-- Escolha um SLA --"),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': _("SLA"),
            },
        ),
    )

    class Meta:
        model = Ticket
        fields = ("identifier", "title", "start_date", "sla")
        exclude = ("end_date", )
        widgets = {
            'identifier': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _("10203040")
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _("Título"),
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _("DD/MM/AAAA")
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _("DD/MM/AAAA")
                }
            ),
        }

    def save(self, commit=True):
        obj = super(TicketForm, self).save(commit=False)
        if commit:
            if not obj.pk:
                obj.save()
                status = Status(
                    type="open",
                    ticket=obj
                )
                status.save()
                return obj
            obj.save()
        return obj