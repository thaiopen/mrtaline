from django.conf.urls import patterns, include, url
from reports import views

urlpatterns = patterns('',
    # /reports/
    url(r'^$',views.index, name='index'),
    url(r'^report_list$',views.report_list, name='report_list'),
    # /report_json
    url(r'^report.json$', views.report_json, name='report_json'),
    # /reports/1
    url(r'^(?P<report_id>\d+)/$',views.detail, name='detail'),
)
