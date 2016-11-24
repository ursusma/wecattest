from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^lnr$',views.lnr),
    url(r'^test$',views.test),
    url(r'',views.index),
]
