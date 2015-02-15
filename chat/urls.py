from django.conf.urls import patterns, url

from chat.views import RoomView

urlpatterns = patterns('',
    (r'^rooms/$', RoomView.as_view()),
    (r'^rooms/(?P<room_id>\d+)/$', RoomView.as_view()),
)