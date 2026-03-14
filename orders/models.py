from django.db import models
from store.models import Product

class Order(models.Model):
    STATUS  = [('pending','Pending'),('confirmed','Confirmed'),('processing','Processing'),
               ('dispatched','Dispatched'),('delivered','Delivered'),('cancelled','Cancelled')]
    COURIER = [('professional','Professional Courier'),('st_courier','ST Courier'),('dtdc','DTDC'),('other','Other')]

    order_id    = models.CharField(max_length=20,unique=True,blank=True)
    full_name   = models.CharField(max_length=120)
    mobile      = models.CharField(max_length=15)
    email       = models.EmailField(blank=True)
    address     = models.TextField()
    landmark    = models.CharField(max_length=120,blank=True)
    city        = models.CharField(max_length=60)
    state       = models.CharField(max_length=60)
    pincode     = models.CharField(max_length=10)
    subtotal    = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    shipping    = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total       = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status      = models.CharField(max_length=20,choices=STATUS,default='pending')
    courier     = models.CharField(max_length=20,choices=COURIER,blank=True)
    tracking_no = models.CharField(max_length=100,blank=True)
    dispatch_date=models.DateField(null=True,blank=True)
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']

    def save(self,*args,**kwargs):
        if not self.order_id:
            last=Order.objects.order_by('-id').first()
            num=int(last.order_id[3:])+1 if last and last.order_id.startswith('MVS') else 10001
            self.order_id=f'MVS{num:05d}'
        super().save(*args,**kwargs)
    def __str__(self): return f"{self.order_id} – {self.full_name}"

    @property
    def tracking_url(self):
        return {'professional':'https://www.tpcindia.com/','st_courier':'https://www.stcourier.com/',
                'dtdc':'https://www.dtdc.in/'}.get(self.courier,'')

class OrderItem(models.Model):
    order       = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product     = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    product_name= models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=10,decimal_places=2)
    qty         = models.PositiveIntegerField()
    weight_kg   = models.DecimalField(max_digits=6,decimal_places=3)
    @property
    def line_total(self): return round(float(self.price)*self.qty,2)
