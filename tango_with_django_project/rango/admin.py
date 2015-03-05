from django.contrib import admin
from rango.models import Category, Page,UserProfile



class PageAdmin(admin.ModelAdmin):
		list_display = ('title', 'category', 'url')
		def __unicode__(self):
			return self.list_display
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)