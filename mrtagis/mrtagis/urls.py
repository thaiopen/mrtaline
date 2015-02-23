from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from djgeojson.views import GeoJSONLayerView
from reports.models import Entry, Report
from home.views import HomePageView, SignUpView, LoginView, LogOutView, PortalView
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mrtagis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^p/$', login_required(PortalView.as_view()),name='portal'),
    #url(r'^p/$', PortalView.as_view(),name='portal'),
    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogOutView.as_view(), name='logout'),
    #url(r'p/?P<portal>/$', HomePageView.as_view(), name ='portal'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signups/', include('signups.urls')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^language/(?P<language>[a-zA-Z\-]+)/$', 'reports.views.language'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Report), name='data'),
    url(r'^p/save_marker/$','home.views.save_marker', name='save_marker'),
    url(r'^p/remove_marker/$','home.views.remove_marker', name='remove_marker'),
)