# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


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
class Status(models.Model):

    title = models.CharField(_("Título"), max_length=30)

    class Meta:
        db_table = "status"
        verbose_name = _("Estado")
        verbose_name_plural = _("Estados")

    def __str__(self):
        return self.title


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
        auto_now_add=True
    )
    end_date = models.DateField(
        _("Data de encerramento"),
        blank=True,
        null=True
    )
    sla = models.ForeignKey(Sla, related_name="tickets", verbose_name=_("SLA"))
    status = models.ForeignKey(Status, related_name="tickets", verbose_name=_("Estado"))

    class Meta:
        db_table = "ticket"
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Break(models.Model):

    ticket = models.ForeignKey(Ticket, related_name="breaks")
    date = models.DateField(_("Data"), auto_now_add=True)
    reason = models.CharField(
        _("Motivo"),
        help_text=_("Informe o motivo da interrupção no SLA."),
        max_length=100
    )
    status = models.ForeignKey(
        Status,
        related_name="breaks",
        verbose_name=_("Estado"),
        help_text=_("Informe o novo estado do ticket após a interrupção.")
    )

    class Meta:
        db_table = "break"
        verbose_name = _("Interrupção")
        verbose_name_plural = _("Interrupções")

    def __str__(self):
        return self.date
