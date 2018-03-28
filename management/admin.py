from django.contrib import admin
from management.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'flavor', 'size', 'price','thumbnail_html',)
    search_fields = ('category__name', 'flavor__name', 'size__name', 'description',)
    list_filter = (('category',admin.RelatedOnlyFieldListFilter),)

    def thumbnail_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_thumbnail_url())
    thumbnail_html.allow_tags = True
    thumbnail_html.short_description = "Imagen"

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'order_time','retire_time','order_source','status','total',)
    search_fields = ('id', 'name',)
    inlines = (ProductInOrderInline,)
    list_filter = ('order_time', 'retire_time', 'order_source', 'status',)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'image_html',)
    search_fields = ('email','first_name', 'last_name',)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"

    def full_name(self,obj):
        return obj.get_full_name()
    full_name.short_description = "Full Name"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'image_html',)
    search_fields = ('name','short_name',)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"


class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'image_html',)
    search_fields = ('name','short_name',)
    list_filter = (('category',admin.RelatedOnlyFieldListFilter),)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'image_html',)
    search_fields = ('name','short_name',)
    list_filter = (('category',admin.RelatedOnlyFieldListFilter),)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"


class BackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_html', 'available',)
    search_fields = ('name',)
    list_filter = ('available',)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"


class GlobalValuesAdmin(admin.ModelAdmin):
    list_display = ('key', 'int_value', 'char_value',)
    search_fields = ('key',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Flavor, FlavorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInOrder)
admin.site.register(GlobalValues, GlobalValuesAdmin)
admin.site.register(Background, BackgroundAdmin)
