from django.db import models
from uuslug import slugify
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User
from uuidfield import UUIDField

# Create your models here.

class Author(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    birth_date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)


class Contractor(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    logo = models.ImageField(upload_to='media', blank=True)
    
    def logo_tag(self):
        if self.logo:
            return u'<img src="%s" style="width:60px;height:60px />' % (self.logo.url)
        else:
            return u'No logo file'
    logo_tag.short_description = 'Thumbnail'
    logo_tag.allow_tags = True 
    
    def __unicode__(self):
        return self.name
    
    
STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('u', 'UnPublished'),
)

class Entry(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    slug = models.CharField(max_length=200,unique=True,blank=True,help_text='auto generate slug field')
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(Author, blank=True)
    contractor = models.ForeignKey(Contractor, blank=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    
    objects = EntryQuerySet.as_manager()
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        
        # self.slug = slugify(self.title)
        self.slug = "%s-%s" % (self.created.strftime('%d-%b-%Y'),self.title.replace(" ", "-"))
        #self.slug = "%s" % (self.title.replace(" ", "-"))
        
        super(Entry, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = "Report Entry"
        verbose_name_plural = "Report Entries"
        ordering = ["-created"]
        
class ReportArea(gismodels.Model):
    title = models.CharField(max_length=256)
    uuid = UUIDField(auto=True)
    geom = gismodels.MultiPolygonField()

    objects = gismodels.GeoManager()

    def __unicode__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
class Report(gismodels.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    uuid = UUIDField(auto=True)
    #type point
    geom = gismodels.PointField()
    picture = models.ImageField(upload_to='reports/%Y/%m/%d',blank=True)
    address =  models.CharField(max_length=200,blank=True)
    published = models.BooleanField(default=False,blank=True)
    created = models.DateTimeField(auto_now_add=True,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True,blank=True)
    categories = models.ManyToManyField(Category,blank=True)

    objects = gismodels.GeoManager()

    def latitude(self):
        return self.geom.y

    def longitude(self):
        return self.geom.x

    @property
    def popupContent(self):
        return '<img src="{}" /><p><{}</p>'.format(
          self.picture.url,
          self.description
          )

    def __unicode__(self):
        return self.title
    
class Place(gismodels.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    location = gismodels.PointField()
    picture = models.ImageField()
    type = models.CharField(
            max_length=8,
            choices=(('t','traffic'),('c','contruction'),('b','block'),)
    )

    def latitude(self):
        return self.location.y

    def longitude(self):
        return self.location.x

    @property
    def popupContent(self):
        return '<img src="{}" /><p><{}</p>'.format(
          self.picture.url,
          self.description
          )


    def __unicode__(self):
        return self.title


class Checkin(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(User)
    place = models.ForeignKey(Place)

    objects = gismodels.GeoManager()
