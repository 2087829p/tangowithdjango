from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
		list_display = ('title', 'category', 'url')
		def __unicode__(self):
			return self.list_display


admin.site.register(Category)
admin.site.register(Page,PageAdmin)
