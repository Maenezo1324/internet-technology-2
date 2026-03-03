from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    parents = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')

    def __str__(self):
        return self.title

    def get_all_paths(self):
        """Возвращает все пути к категории через родителей"""
        if not self.parents.exists():
            return [self.title]
        paths = []
        for parent in self.parents.all():
            for parent_path in parent.get_all_paths():
                paths.append(f"{parent_path} -> {self.title}")
        return paths

class Shop(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='shops/', blank=True, null=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orders_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)