from django.db import models
from category.models import category
from django.urls import reverse

# Create your models here.
class products(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField(default=0)
    images = models.ImageField(upload_to="photos/products", default="")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('category.category', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self):
        return self.product_name

class Variation(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=(('color', 'color'), ('size', 'size')))
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product
