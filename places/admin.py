from django.contrib import admin
from django.utils.html import format_html

from .models import Place
from .models import Image


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('image_field', 'get_preview', 'name')
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return format_html(
            '<img src="{url}" width="{width}" />'.format(
                url=obj.image_field.url,
                width=200,
            )
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    ordering = ['id']
