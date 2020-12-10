from django.contrib import admin
from .models import Bucket, Item, IdentifierType, Identifier


class IdentiferInline(admin.TabularInline):
    model = Identifier
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'bucket']}),
        ('Additional Info', {'fields': ['desc'], 'classes': ['collapse']})
    ]
    inlines = [IdentiferInline]


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


# Register your models here.
admin.site.register(Bucket)
admin.site.register(Item, ItemAdmin)
admin.site.register(IdentifierType)
