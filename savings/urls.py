from django.urls import re_path, include
from savings import views as savings_views

app_name = 'savings'

urlpatterns = [
	re_path(r'^savings/$', savings_views.savings_view, name='savings'),
	re_path(r'^withdraw/$', savings_views.withdraw_view, name='withdraw'),
	re_path(r'^deposit/$', savings_views.deposit_view, name='deposit'),
]