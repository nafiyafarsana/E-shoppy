from django.db import models
from django.urls import reverse
from PIL import Image
from accounts.serializer import User

# Create your models here.


   
    
class Category(models.Model):
    category_name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255)
    cat_image=models.ImageField(upload_to='pictures/%Y/%m,/%d/',blank=True)
    
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
        
    def get_url(self):
        return f'/{self.slug}/'
    
    def __str__(self):
        return self.category_name



class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=200,blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='uploads/',blank=True,null=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ('-created_date',)
    
    def get_url(self):
        return f'/{self.slug}/'
    
    def __str__(self):
        return self.product_name
    def get_image(self):
        if self.images:
            return 'http://127.0.0.1:8000/' + self.image.url
        return ''
 
     
     
class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)
    
variation_category_choice = (
        ('color','color'),
        ('size','size'),
)
            
class Variations(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)   
    variation_category = models.CharField(max_length=100 , choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):  
        return self.variation_value
    
    

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True, null=True, default=None)
    date_added=models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    
def __str__(self):
    return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    variations = models.ManyToManyField(Variations,blank=True) 
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE, null=True,blank=True, default=None)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.price * self.quantity


    def __unicode__(self):
        return self.product
     