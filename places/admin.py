from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableTabularInline

from .models import Place
from .models import Image


class ImageInline(SortableTabularInline):
    model = Image
    extra = 0
    ordering = ['position']
    list_display = ['image_field', 'get_preview']
    readonly_fields = ['get_preview']

    def get_preview(self, image: Image):
        return format_html(
            '<img src="{url}" height="{height}" />',
            url=image.picture.url,
            height=200,
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    search_fields = ['title']
    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    ordering = ['position']
