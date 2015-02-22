from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin
from models import Task, Staff
# Register your models here.


class TaskAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = ['state',]
    list_display = ('title','assign_date',)

    
class StaffAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)

admin.site.register(Task,TaskAdmin)

admin.site.register(Staff, StaffAdmin)