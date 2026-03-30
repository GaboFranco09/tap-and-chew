from django.db import models

class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url   = models.URLField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category    = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name        = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    image_url   = models.URLField(blank=True)
    is_active   = models.BooleanField(default=True)
    is_available= models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.category.name} — {self.name}'


class Combo(models.Model):
    name        = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    products    = models.ManyToManyField(Product, related_name='combos')
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    image_url   = models.URLField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name