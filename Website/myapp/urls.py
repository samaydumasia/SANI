from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('chat', views.chat, name = "chat"),
    path('login', views.login, name = "login"),
    # path('signup', views.signup, name = "signup"),
    path('profile', views.profile, name = "profile"),
    path('send', views.send, name='send'),
    # path('getMessages/<str:user_id>/', views.getMessages, name='getMessages'), 
    path('getMessages', views.getMessages, name='getMessages'),
    path('analysis',views.analysis,name='analysis')   
]