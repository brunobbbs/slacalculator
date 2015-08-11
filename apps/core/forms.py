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
        exclude = ("end_date", "state")
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
                    state="open",
                    ticket=obj,
                    start_date=obj.start_date
                )
                status.save()
                return obj
            obj.save()
        return obj


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ("ticket", "state", "note", "start_date")
        exclude = ("end_date", "interruption", "modified")
        widgets = {
            'ticket': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        obj = super(StatusForm, self).save(commit=False)
        if commit:
            interruptions = ["waiting_user", "waiting_supplier",
                             "waiting_client", "waiting_resources"]
            if obj.state in interruptions:
                obj.interruption = True
            obj.save()
        return obj
