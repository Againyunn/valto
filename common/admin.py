from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from .models import *

# Register your models here.
class UserinfoAdmin(ImportExportMixin, admin.ModelAdmin):
    pass
admin.site.register(Userinfo, UserinfoAdmin)