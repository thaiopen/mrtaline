from django.conf import settings
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail
from forms import SignUpForm

# Create your views here.

def index(request):
    language = 'en-US'
    session_language = 'en-US'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']
    
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        #send mail
        #send_mail(subject, message, from_mail, to_list, fail_silently=True )
        subject = 'Thank you for your Submit to MRTAGIS'
        message = 'Welcome to MRATGIS, We very appreciate your join .\n'
        from_email = settings.EMAIL_HOST_USER
        to_list = [save_it.email,settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True )
        messages.success(request,'Thank you for joining')
        return HttpResponseRedirect('/thank-you/')
    #return render(request,'signups/index.html',{'form': form})
    return render(request,'signups/index.html',locals())

def thankyou(request):
    
    return render(request,'signups/thankyou.html',locals())
