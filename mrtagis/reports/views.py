from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Polygon
import json
from models  import Report
from forms import ReportForm
from django.views.generic import UpdateView,  View, CreateView, ListView, DetailView

def index(request):
    language = 'en-US'
    session_language = 'en-US'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    return render(request,'reports/index.html',{'language': language})

def language(request,language='en-US'):
    #generate response from HttpResponse objects
    response = HttpResponse("setting language to %s" % language)
    #set variable inside cookies
    response.set_cookie('lang', language)
    return response

def report_list(request):
    report_lists = Report.objects.order_by('-pub_date')[:5]
    context = {'report_lists': report_lists}
    return render(request,'reports/report_list.html',context)

def detail(request):
    return render(request,'reports/detail.html',{})

def report_json(request):
    # figure out what the bounding box is for the request
    # /report.json?bbox=x1,y1,x2,y2
    # need polygon from geodjango
    bbox  = request.GET['bbox'].split(',')
    # polygon object to make query
    poly = Polygon.from_bbox(bbox)

    # fetch those crimes
    reports = Report.objects.filter(geom__within=poly)
    # convert to geojson
    geojson_dict = {
        "type": "FeatureCollection",
        # array of dict of report json
        "features": [report_to_json(report) for report in reports],
    }
    # return the response
    # encapsulate content type
    return HttpResponse(json.dumps(geojson_dict),content_type='application/json')

# basemap.html use leafjson add geojson on map function report_refresh()
def report_to_json(report):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [report.geom.x, report.geom.y],
        },
        "properties": {
            "description": report.title,
        }
    }


