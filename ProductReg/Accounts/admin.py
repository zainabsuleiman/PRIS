from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Industry)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Application)
admin.site.register(ApplicationFeedback)
admin.site.register(Plan)