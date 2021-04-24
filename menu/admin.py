from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Categori,Urun,Images,Comment
from django import forms

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model=Images
    extra=5

class CategoriAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields={'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Categori.objects.add_related_count(
                qs,
                Urun,
                'Categori',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Categori.objects.add_related_count(
                qs,
                 Urun,
                 'Categori',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'



class UrunAdmin(admin.ModelAdmin):
    list_display = ['title','description','tip','Categori','keywords', 'status','image_tag']
    list_filter = ['status','Categori']
    inlines=[ProductImageInline]
    prepopulated_fields={'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','urun','user','rate','status']
    list_filter = ['status']
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'urun','image_tag']

admin.site.register(Categori,CategoriAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Urun,UrunAdmin)

admin.site.register(Comment,CommentAdmin)