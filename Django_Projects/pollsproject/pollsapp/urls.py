from django.urls import path
from . import views

app_name = 'pollsapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_url'),
    path('signup/', views.SignUp.as_view(), name='signup_url'),
    path('newpoll/', views.create_question, name='newpoll_url'),
    path('<int:pk>/', views.PollView.as_view(), name='poll_url'),
    path('<int:pk>/vote/', views.vote, name='vote_url'),    
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results_url'),
]
