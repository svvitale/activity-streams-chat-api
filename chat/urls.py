from django.conf.urls import patterns, url

from chat.views import RoomView, UserView, MessageView

urlpatterns = patterns('',
    (r'^rooms/$', RoomView.as_view()),
    (r'^rooms/(?P<item_id>\d+)/$', RoomView.as_view()),
    (r'^users/$', UserView.as_view()),
    (r'^users/(?P<item_id>\d+)/$', UserView.as_view()),
    (r'^rooms/(?P<room_id>)/messages/$', MessageView.as_view()),
    (r'^rooms/(?P<room_id>)/messages/(?P<item_id>)$', MessageView.as_view()),
    #(r'^rooms/(?P<room_id>)/members/$', MemberView.as_view()),
    #(r'^rooms/(?P<room_id>)/members/(?P<item_id>)$', MemberView.as_view()),
)