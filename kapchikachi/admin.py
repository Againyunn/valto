from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from .models import *

# Register your models here.


class CommentAdmin(ImportExportMixin, admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)

class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)


# admin.site.register(OrderTransaction)