from django.urls import path
from . import views

app_name = 'weatherapp'


urlpatterns = [
    path('', views.IndexView.as_view(), name="index_url"),
    path('<int:pk>/forecast', views.ForecastDetailView.as_view(), name='forecast_url'),
    path('add/', views.add, name='add_url'),
    path('delete/<int:pk>', views.delete, name="delete_url"),

]
