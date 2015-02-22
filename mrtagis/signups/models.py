from django.db import models
from django.utils.encoding import smart_unicode

# Create your models here.
class SignUp(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __unicode__(self):
        return "%s , %s" % (self.first_name, smart_unicode(self.email))