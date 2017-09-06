from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegisterView.as_view()),
    url(r'^login/$', views.UserLoginView.as_view()),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
