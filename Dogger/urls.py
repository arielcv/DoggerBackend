from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as token
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    url(r'^users/(?P<name>[a-zA-Z0-9_.-]+)/$', views.getUser, name='user'),
    url(r'^owners/$', views.dogOwnerList ,name = 'dogOwnerList'),
    url(r'^owners/signup/$', views.dogOwnerSignUp ,name = 'dogOwnerSignUp'),
    url(r'^owners/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogOwnerDetails, name= 'dogOwnerDetail'),
    url(r'^owners/(?P<name>[a-zA-Z0-9_.-]+)/reservation/$', views.dogOwnerReservation, name= 'dogOwnerDetail'),
    url(r'^dogs/$', views.dogList ,name = 'dogOwnerList'),
    url(r'^dogs/owner/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogListByOwner, name= 'dogOwnerDetail'),
    url(r'^dogs/(?P<id>[0-9]+)/$', views.dogDetails, name= 'dogOwnerDetail'),
    url(r'^reservation/(?P<id>[0-9]+)/$', views.acceptReservation, name= 'dogOwnerDetail'),
    url(r'^walkers/$', views.dogWalkerList ,name = 'dogOwnerList'),
    url(r'^walkers/signup/$', views.dogWalkerSignUp ,name = 'dogOwnerList'),
    url(r'^walkers/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogWalkerDetails, name= 'dogOwnerDetail'),
    url(r'^walkers/(?P<name>[a-zA-Z0-9_.-]+)/reservation/$', views.dogWalkerReservation, name= 'dogOwnerDetail'),
    url(r'^walkers/(?P<name>[a-zA-Z0-9_.-]+)/constraints/$', views.dogWalkerConstraintsList, name='dogOwnerDetail'),
    url(r'^walkers/constraints/(?P<id>[0-9]+)$', views.dogWalkerConstraintsDetails, name='dogOwnerDetail'),
    url(r'^login/$', token.obtain_auth_token),
]