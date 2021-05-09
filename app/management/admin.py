from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from management.models import *
from django.db.models import Q


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
    list_display = ('id', 'description', 'retire_time','order_source','status','total', 'user')
    search_fields = ('id', 'total')
    inlines = (ProductInOrderInline,)
    list_filter = (
        ('retire_time', DateRangeFilter),
        'status',
    )

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', )
    search_fields = ('email','full_name',)

    labels = {
        'email': 'Correo',
    }

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(CustomUserAdmin, self).get_search_results(request, queryset, search_term)
        queryset = self.model.objects.filter(Q(full_name__unaccent__icontains=search_term) | Q(email=search_term))
        return queryset, use_distinct


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'image_html',)
    search_fields = ('name', 'name',)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"


class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'image_html',)
    search_fields = ('name','name',)
    list_filter = (('category',admin.RelatedOnlyFieldListFilter),)

    def image_html(self,obj):
        return u'<img height="100" src="%s/" />' % (obj.get_image_url())
    image_html.allow_tags = True
    image_html.short_description = "Image"


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'image_html',)
    search_fields = ('name','name',)
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

class CostItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit',)
    search_fields = ('name','unit',)

class CostAdmin(admin.ModelAdmin):
    list_display = ('cost_item', 'quantity', 'total_display', 'date',)
    search_fields = ('cost_item',)
    date_hierarchy = 'date'
    ordering = ('cost_item','-date',)
    list_filter = ('date',('cost_item',admin.RelatedOnlyFieldListFilter),)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CostItem, CostItemAdmin)
admin.site.register(Cost, CostAdmin)
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Flavor, FlavorAdmin)
#admin.site.register(Size, SizeAdmin)

#admin.site.register(ProductInOrder)
#admin.site.register(GlobalValues, GlobalValuesAdmin)
#admin.site.register(Background, BackgroundAdmin)
