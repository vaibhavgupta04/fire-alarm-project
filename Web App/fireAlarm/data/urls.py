from django.urls import path
from . import views
urlpatterns = [
    #path('', views.home),
    path("",views.index,name='home'),
    path("index/",views.index,name='index'),
    path("show_request/",views.show_request,name='show_request'),
    path("send/",views.send,name="send"),
    path("loginpage/",views.loginpage,name='loginpage'),
    path("registerPage/",views.registerPage,name='registerPage'),
    path("dashboard/",views.dashboard,name='dashboard'),
    path("logoutuser/",views.logoutuser,name="logoutuser"),
    path("history/",views.history,name="history"),
    path("graph/",views.graph,name="graph"),
    path("userpage/",views.userpage,name="userpage"),
    path("fire_history/",views.fire_history,name='fire_history'),
    path("detail/<str:pk>",views.detail,name="detail"),
    path("request_access/",views.request_access,name="request_access"),
    path("add_to_grp/<str:pk>",views.add_to_grp,name="add_to_grp"),
    path("given_access/",views.given_access,name="given_access"),
    path("remove_from_grp/<str:pk>",views.remove_from_grp,name="remove_from_grp")
]