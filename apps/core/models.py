# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from utils.choice import Choice
from workdays import workday


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

    def latest_status(self):
        status = Status.objects.select_related("ticket").filter(ticket=self).last()
        return status

    def due_date(self):
        max = self.sla.days_budget + self.sla.days_start_attendance + self.sla.days_delivery
        due_date = workday(self.start_date, max)
        return due_date


class StatusChoice(Choice):
    OPEN = "open", _("Aberto")
    WORKING = "working", _("Em andamento")
    CLOSED = "closed", _("Fechado")
    W_CLIENT = "waiting_client", _("Aguardando cliente")
    W_RESOURCES = "waiting_resources", _("Aguardando recursos")
    W_SUPPLIER = "waiting_supplier", _("Aguardando fornecedor")
    W_USER = "waiting_user", _("Aguardando usuário")


@python_2_unicode_compatible
class Status(models.Model):

    type = models.CharField(_("Tipo"), max_length=20, choices=StatusChoice, default=StatusChoice.OPEN)
    note = models.TextField(_("Observações"), blank=True)
    added = models.DateTimeField(_("Adicionado"), auto_now_add=True)
    ticket = models.ForeignKey(Ticket, related_name="history")

    class Meta:
        db_table = "status"
        verbose_name = _("Estado")
        verbose_name_plural = _("Estados")
        ordering = ["-added", ]

    def __str__(self):
        return self.get_type_display()


@python_2_unicode_compatible
class Break(models.Model):

    ticket = models.ForeignKey(Ticket, related_name="breaks")
    date = models.DateField(_("Data"))
    reason = models.CharField(
        _("Motivo"),
        help_text=_("Informe o motivo da interrupção no SLA."),
        max_length=100
    )
    status = models.CharField(
        _("Estado"),
        max_length=20,
        choices=StatusChoice,
        default=StatusChoice.W_USER,
        help_text=_("Informe o novo estado do ticket após a interrupção.")
    )

    class Meta:
        db_table = "break"
        verbose_name = _("Interrupção")
        verbose_name_plural = _("Interrupções")

    def __str__(self):
        return self.date
