from django.conf.urls import url

from .views import TicketCreateView, TicketListView, TicketUpdateView


urlpatterns = [
    url(r'^add/$', TicketCreateView.as_view(), name="add"),
    url(r'^list/$', TicketListView.as_view(), name="list"),
    url(r'^update/(?P<pk>\d+)/$', TicketUpdateView.as_view(), name="update"),
]
