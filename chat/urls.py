from django.conf.urls import patterns, url

from chat.views import RoomView, UserView, MessageView, MemberView

urlpatterns = patterns('',
    (r'^rooms/$', RoomView.as_view()),
    (r'^rooms/(?P<item_id>\d+)/$', RoomView.as_view()),
    (r'^users/$', UserView.as_view()),
    (r'^users/(?P<item_id>\d+)/$', UserView.as_view()),
    (r'^rooms/(?P<room_id>\d+)/messages/$', MessageView.as_view()),
    (r'^rooms/(?P<room_id>\d+)/messages/(?P<item_id>\d+)/$', MessageView.as_view()),
    (r'^rooms/(?P<room_id>\d+)/members/$', MemberView.as_view()),
    (r'^rooms/(?P<room_id>\d+)/members/(?P<user_id>\d+)/$', MemberView.as_view()),
)