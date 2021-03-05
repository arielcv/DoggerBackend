from django.conf.urls import url
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    url(r'^owners/$', views.dogOwnerList ,name = 'dogOwnerList'),
    url(r'^owners/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogOwnerDetails, name= 'dogOwnerDetail'),
    url(r'^dogs/$', views.dogList ,name = 'dogOwnerList'),
    url(r'^dogs/owner/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogListByOwner, name= 'dogOwnerDetail'),
    url(r'^dogs/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogDetails, name= 'dogOwnerDetail'),
    url(r'^walkers/$', views.dogWalkerList ,name = 'dogOwnerList'),
    url(r'^walkers/(?P<name>[a-zA-Z0-9_.-]+)/$', views.dogWalkerDetails, name= 'dogOwnerDetail'),
    url(r'^api/token/$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]