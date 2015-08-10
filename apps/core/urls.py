from django.conf.urls import url

from .views import (
    TicketCreateView,
    TicketListView,
    TicketUpdateView,
    ChangeStatusView
)


urlpatterns = [
    url(r'^add/$', TicketCreateView.as_view(), name="add"),
    url(r'^list/$', TicketListView.as_view(), name="list"),
    url(r'^update/(?P<pk>\d+)/$', TicketUpdateView.as_view(), name="update"),
    url(r'^status/update/(?P<pk>\d+)/', ChangeStatusView.as_view(), name="status_update"),
]
