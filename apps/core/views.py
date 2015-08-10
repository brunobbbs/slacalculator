from __future__ import unicode_literals

from datetime import datetime

from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DetailView
)

from django.core.urlresolvers import reverse

from .forms import TicketForm, StatusForm
from .models import Ticket, Status, StatusChoice


class HomePageView(TemplateView):

    template_name = 'core/index.html'


class TicketDetailView(DetailView):

    model = Ticket


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


class ChangeStatusView(CreateView):

    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse("tickets:list")

    def get_ticket(self):
        ticket = Ticket.objects.get(pk=self.request.GET.get("ticket"))
        return ticket

    def get_status(self, status):
        result = dict()
        for choice, value in StatusChoice:
            result[choice] = value
        return result[status]

    def get_context_data(self, **kwargs):
        kwargs = super(ChangeStatusView, self).get_context_data(**kwargs)
        state = self.request.GET.get("status")
        kwargs.update({
            'ticket': self.get_ticket(),
            'status': self.get_status(state)
        })
        return kwargs

    def form_valid(self, form):
        current_status = self.get_object()
        form_kwargs = self.get_form_kwargs()['data']
        date = map(int, form_kwargs['start_date'].split("/"))
        current_status.end_date = datetime(date[2], date[1], date[0])
        current_status.save()

        state = self.request.GET.get("status")
        ticket = self.get_ticket()
        if state == "closed":
            ticket.end_date = datetime.now()
            ticket.save()
        else:
            ticket.end_date = None
            ticket.save()
        return super(ChangeStatusView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ChangeStatusView, self).get_form_kwargs()
        state = self.request.GET.get("status")
        kwargs['initial'] = {
            'ticket': self.get_ticket().pk,
            'state': state
        }
        return kwargs
