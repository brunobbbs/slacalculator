from __future__ import unicode_literals

from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView
)

from django.core.urlresolvers import reverse

from core.forms import TicketForm
from .models import Ticket, Status


class HomePageView(TemplateView):

    template_name = 'core/index.html'


class TicketCreateView(CreateView):

    model = Ticket
    form_class = TicketForm

    def get_success_url(self):
        return reverse("tickets:list")


class TicketListView(ListView):

    model = Ticket


class TicketUpdateView(UpdateView):

    model = Ticket
    form_class = TicketForm

    def get_success_url(self):
        return reverse("tickets:list")


class StatusCreateView(CreateView):

    model = Status
    form_class = None  # TODO: Add form_class

    def get_success_url(self):
        return reverse("tickets:list")