from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    emoji = models.CharField(max_length=10, default='🐠')
    sort_order = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order','name']
    def __str__(self): return self.name

class Product(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name       = models.CharField(max_length=200)
    slug       = models.SlugField(unique=True)
    description= models.TextField(blank=True)
    care_tips  = models.TextField(blank=True)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight_kg  = models.DecimalField(max_digits=6, decimal_places=3, default=0.200)
    stock      = models.PositiveIntegerField(default=50)
    image      = models.ImageField(upload_to='products/', blank=True, null=True)
    image2     = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured   = models.BooleanField(default=False)
    is_new_arrival= models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self): return self.name
    @property
    def final_price(self): return self.offer_price if self.offer_price else self.price
    @property
    def savings(self):
        if self.offer_price: return round(float(self.price)-float(self.offer_price),2)
        return 0
    @property
    def discount_pct(self):
        if self.offer_price and self.price>0:
            return int(((self.price-self.offer_price)/self.price)*100)
        return 0
    @property
    def in_stock(self): return self.stock > 0

class Review(models.Model):
    name      = models.CharField(max_length=100)
    location  = models.CharField(max_length=80, blank=True)
    rating    = models.IntegerField(default=5)
    title     = models.CharField(max_length=150, blank=True)
    body      = models.TextField()
    verified  = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f"{self.name} – {self.rating}★"
