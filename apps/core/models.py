# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from utils.choice import Choice
from workdays import workday, networkdays


@python_2_unicode_compatible
class Queue(models.Model):

    title = models.CharField(_("Título"), max_length=50)

    class Meta:
        db_table = "queue"
        verbose_name = _("Fila")
        verbose_name_plural = _("Filas")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Sla(models.Model):

    queue = models.ForeignKey(Queue, related_name="sla", verbose_name=_("Fila"))
    reference = models.CharField(
        _("Referência"),
        max_length=10,
        help_text=_("Informe a referência (se houver) do contrato para este SLA."),
        blank=True
    )
    service = models.CharField(_("Serviço"), max_length=50)
    description = models.TextField(_("Descrição"), blank=True)
    days_budget = models.PositiveSmallIntegerField(
        _("Estimativa"),
        help_text=_("Informe o prazo máximo em dias para elaboração de estimativa."),
        default=0
    )
    days_start_attendance = models.PositiveSmallIntegerField(
        _("Início do atendimento"),
        help_text=_("Informe o prazo máximo em dias para início do atendimento."),
        default=0
    )
    days_delivery = models.PositiveSmallIntegerField(
        _("Execução do serviço"),
        help_text=_("Informe o prazo máximo em dias para execução do serviço."),
        default=2
    )
    value = models.PositiveIntegerField(
        _("Valor"),
        help_text=_("Informe o valor unitário deste SLA."),
        blank=True,
        null=True
    )

    class Meta:
        db_table = "sla"
        verbose_name = _("SLA")
        verbose_name_plural = _("SLAs")

    def __str__(self):
        return self.service


@python_2_unicode_compatible
class Ticket(models.Model):

    identifier = models.CharField(
        _("Identificador"),
        help_text=_("Informe o ID ou outro identificador do ticket."),
        max_length=10
    )
    title = models.CharField(
        _("Título"),
        max_length=150
    )
    start_date = models.DateField(
        _("Data de abertura"),
    )
    end_date = models.DateField(
        _("Data de encerramento"),
        blank=True,
        null=True
    )
    sla = models.ForeignKey(Sla, related_name="tickets", verbose_name=_("SLA"))

    class Meta:
        db_table = "ticket"
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        ordering = ["-start_date", "-end_date"]

    def __str__(self):
        return self.title

    def _get_interruption_days(self):
        count = 0
        interruptions = self.history.filter(interruption=True)
        for interrupt in interruptions:
            if interrupt.end_date:
                calc = interrupt.end_date - interrupt.start_date
                if calc.days >= 1:
                    work_days = networkdays(interrupt.start_date, interrupt.end_date)
                    count += work_days
        return count

    def latest_status(self):
        status = Status.objects.select_related("ticket").filter(ticket=self).first()
        return status

    def due_date(self):
        max = self.sla.days_budget + self.sla.days_start_attendance + self.sla.days_delivery
        break_days = self._get_interruption_days()
        max += break_days
        due_date = workday(self.start_date, max)
        return due_date


class StatusChoice(Choice):
    OPEN = u"open", _("Aberto")
    WORKING = u"working", _("Em andamento")
    CLOSED = u"closed", _("Fechado")
    W_USER = u"waiting_user", _("Aguardando usuário")
    W_CLIENT = u"waiting_client", _("Aguardando cliente")
    W_RESOURCES = u"waiting_resources", _("Aguardando recursos")
    W_SUPPLIER = u"waiting_supplier", _("Aguardando fornecedor")


@python_2_unicode_compatible
class Status(models.Model):

    ticket = models.ForeignKey(Ticket, related_name="history")
    state = models.CharField(_("Status"), max_length=20, default="open", choices=StatusChoice)
    note = models.TextField(_("Observações"), blank=True)
    start_date = models.DateField(_("Data"))
    end_date = models.DateField(_("Finalizado"), blank=True, null=True)
    modified = models.DateTimeField(_("Modificado"), auto_now=True)
    interruption = models.BooleanField(_("Interrupção"), default=False)

    class Meta:
        db_table = "status"
        verbose_name = _("Status")
        verbose_name_plural = _("Status")
        ordering = ["-modified", ]

    def __str__(self):
        return self.get_state_display()
