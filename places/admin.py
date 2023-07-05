from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableTabularInline

from places.models import Place
from places.models import Image


class ImageInline(SortableTabularInline):
    model = Image
    extra = 0
    ordering = ['position']
    list_display = ['image_field', 'get_preview']
    readonly_fields = ['get_preview']

    def get_preview(self, image: Image):
        picture_height = 200
        return format_html(
            '<img src="{url}" height="{height}" />',
            url=image.picture.url,
            height=picture_height,
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
