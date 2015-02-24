from __future__ import absolute_import
import json

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
#user with auth django
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from braces import views
from django.contrib.gis.geos import fromstr

from reports.models import Place, Portal
# Create your views here.
#def index(request):
#    return render(request,'home/index.html',locals())
#
def save_marker(request):
    if request.method == 'POST' and request.is_ajax:
        response_data = {}
        #name = request.POST['name']
        #address = request.POST['address']
        #latlng = request.POST['latlng']
        #report_type = request.POST['report_type']
        name = request.POST.get('name',None)
        address = request.POST.get('address',None)
        latlng = request.POST.get('latlng',None)
        report_type = request.POST.get('report_type',None)
        user = request.POST.get('user',None)
        token = request.POST.get('csrfmiddlewaretoken',None)
        
        response_data['name'] = name
        response_data['address'] = address
        response_data['latlng'] = latlng
        response_data['report_type'] = report_type
        response_data['user'] = user
        response_data['token'] = token
        #current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
        #split string with with delimeters
        #str.split(', ')
        p = latlng.split(',')
        point = fromstr("POINT(%s %s)" % (p[1],p[0]) )
        print response_data
        #print p
        #print point
        p = Portal.objects.get(title=user)
        u = User.objects.get(username=user)
        #print p
        point_obj = Place(title=name, description=address,location=point, portal=p, user=u)
        #print point_obj
        point_obj.save()
        #print point_obj.created
        response_data['created'] = point_obj.created
        #request.POST
        #{"latlng": "13.733382,100.521061", "csrfmiddlewaretoken": "F11cng7GGhHqmAsnHhrCQAIg5nVOijMT", "name": "aaaaa", "report_type": "asset", "address": "aaaaaa"}
       #return render(request,json.dumps(request.POST),content_type='application/json')
        #django 1.7 use JsonResponse
        #return  render(request,'home/index.html',JsonResponse(response_data))
        return HttpResponse(JsonResponse(response_data), content_type="application/json")
    else:
        msg = {"nothing to see": "this isn't happening"}
        return HttpResponse(JsonResponse(msg), content_type="application/json")

def remove_marker(request):
    if request.method == 'POST' and request.is_ajax:
        latlng = request.POST.get('latlng',None)
        p = latlng.split(',')
        point = fromstr("POINT(%s %s)" % (p[1],p[0]) )
        Place.objects.get(location=point).delete()
        response_data = {"progress": "it works!"}
        return HttpResponse(JsonResponse(response_data), content_type="application/json")
    else:
        msg = {"progress": "it fails"}
        return HttpResponse(JsonResponse(msg), content_type="application/json")       


class HomePageView(generic.TemplateView):
    template_name = 'home/index.html'

class PortalView(generic.TemplateView):
    template_name = 'home/portal.html'

class SignUpView(views.AnonymousRequiredMixin,views.FormValidMessageMixin, generic.CreateView):
#    form_class = UserCreationForm
    form_class = RegistrationForm
    form_valid_message = "Thank you for signup"
    model = User
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
    #after signup will bring to profile   accouts/username
    #after signup create default portal for each user
    def form_valid(self, form):
        resp = super(SignUpView, self).form_valid(form)
        Portal.objects.create(user=self.object,title=self.object.username)
        return resp

class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('portal')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)
#assign form_class create template  'accounts/login.html'


class LogOutView(views.LoginRequiredMixin,views.MessageMixin, generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        self.messages.success("You've been logged out. Come back soon!")
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)