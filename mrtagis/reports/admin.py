from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from leaflet.admin import LeafletGeoAdmin
from models import ReportArea, Report
from django.contrib.gis.maps.google import GoogleMap
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal.srs import SpatialReference


from models import Entry, Contractor, Author, Place, Portal
# Register your models here.

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    fields = ('name','address','phone','website','logo',)
    list_display = ('name','address','phone','website','logo','logo_tag')
    readonly_fields = ('logo_tag',)

#admin.site.register(Contractor,ContractorAdmin)

def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "1 story was"
    else:
        message_bit = "%s stories were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)

def all_tasks(modeladmin,request, queryset):
    for qs in queryset:
        print qs.title

def publish_report(modeladmin, request, queryset):
    queryset.update(publish=True)
    queryset.update(status='p')
    publish_report.short_description = "Mask as published"

def unpublish_report(modeladmin, request, queryset):
    queryset.update(publish=False)
    queryset.update(status='u')
    unpublish_report.short_description = "Mask as unpublished"

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status','publish','created',)
    ordering = ['title']
    actions = [publish_report,unpublish_report]
    
#admin.site.register(Entry, EntryAdmin)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = (('username','email'),('first_name','last_name'))
    
#class ReportAreaAdmin(gisadmin.OSMGeoAdmin):
class ReportAreaAdmin(LeafletGeoAdmin):
    search_fields = ['title','uuid']
    list_display = ['title','uuid']
    readonly_fields = ['uuid']
    map_height = '500px'

class ReportAdmin(LeafletGeoAdmin):
    list_display = ('title',)
    #map_width = '90%'
    map_height = '500px'
    
class GoogleAdmin(gisadmin.OSMGeoAdmin):
    map_template = 'reports/gis/admin/gmgdav3.html'
    g = GEOSGeometry('POINT (9.191884 45.464254)',srid=4326) # Set map center
    g.set_srid(4326)
    #g.transform(900913)
    default_lon = int(g.x)
    default_lat = int(g.y)
    default_zoom = 7
    extra_js = ["http://maps.google.com/maps/api/js?v=3.2&sensor=false"] 
    
#admin.site.register(ReportArea, ReportAreaAdmin)
admin.site.register(ReportArea, LeafletGeoAdmin)
#admin.site.register(ReportArea, GoogleAdmin)
admin.site.register(Report, ReportAdmin )
admin.site.register(Place, ReportAdmin)
admin.site.register(Portal)
#admin.site.register(Report, GoogleAdmin )
