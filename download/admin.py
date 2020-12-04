from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.BCCEmail)
class BCCEmailAdmin(admin.ModelAdmin):
    pass

@admin.register(models.CCEmail)
class CCEmailAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ['address', 'upload_date']