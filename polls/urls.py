from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_page_with_button, name='page_with_button'),
    path('current-datetime', views.get_current_datetime, name='current_datetime'),
    path('save-client-log', views.save_client_log, name='save_client_log'),
]
