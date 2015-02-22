from django.db import models
from django_fsm import FSMField, transition
from uuidfield import UUIDField
# Create your models here.

class Staff(models.Model):
    name = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.name

PRIORITY_CHOICES = ( 
  (1, 'Low'), 
  (2, 'Normal'), 
  (3, 'High'), 
)
 
class Task(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    taskid = UUIDField(auto=True)
    slug = models.CharField(max_length=200,unique=True,blank=True,help_text='auto generate slug field')
    state = FSMField(default='new')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    assign_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    staff = models.ForeignKey(Staff,blank=True)
    due_date = models.DateTimeField(default=None)
    
    
    @transition(field=state, source='new', target='approve')  
    def approve(self):
        pass
    
    @transition(field=state, source='approve', target='new')  
    def unapprove(self):
        pass
    
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.assign_date = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        
        # self.slug = slugify(self.title)
        self.slug = "%s-%s" % (self.assign_date.strftime('%d-%b-%Y'),self.title.replace(" ", "-"))
        #self.slug = "%s" % (self.title.replace(" ", "-"))
        
        super(Task, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-assign_date"]
        