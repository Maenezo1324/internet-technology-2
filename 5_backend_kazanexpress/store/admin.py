from django.contrib import admin
from django.utils.html import format_html
from .models import Shop, Category, Product, ProductImage
from django.utils.safestring import mark_safe

class PriceRangeFilter(admin.SimpleListFilter):
    title = 'диапазон цен'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('low', 'До 1000'),
            ('mid', 'От 1000 до 5000'),
            ('high', 'Выше 5000'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=1000)
        if self.value() == 'mid':
            return queryset.filter(price__gte=1000, price__lte=5000)
        if self.value() == 'high':
            return queryset.filter(price__gt=5000)
        return queryset

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_image')
    search_fields = ('title',)
    readonly_fields = ('id',)

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"
    get_image.short_description = 'Картинка'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_main_image', 'price', 'orders_count', 'is_active')
    list_filter = ('is_active', PriceRangeFilter)
    search_fields = ('id', 'title')
    readonly_fields = ('id',)
    inlines = [ProductImageInline]
    filter_horizontal = ('categories',)

    def get_main_image(self, obj):
        main_img = obj.images.filter(is_main=True).first() or obj.images.first()
        if main_img:
            return format_html('<img src="{}" style="max-height: 50px;"/>', main_img.image.url)
        return "-"
    get_main_image.short_description = 'Главное фото'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_paths')
    search_fields = ('title', 'parents__title', 'products__id')
    filter_horizontal = ('parents',)

    def display_paths(self, obj):
        paths = obj.get_all_paths()
        return mark_safe("<br>".join(paths))
    display_paths.short_description = 'Пути к категории'