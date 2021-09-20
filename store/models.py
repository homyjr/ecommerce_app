from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import EmailField
from django.db.models.fields.related import OneToOneField
from django.core.validators import MinLengthValidator


# Create your models here.

MYCHOICES = (('YES', 'yes'), 
           ('NO',"no"))

STATUSCHOICES = (('COMPLETED', 'completed'), 
           ('ACTIVE',"active"))


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length=100, blank= True, null = True)
    email = models.CharField(max_length=100, blank = True, null=True)
    
    def __str__(self) -> str:
        return str(self.user)

  

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default = 0)
    image = models.ImageField(upload_to = 'images', default = 'products/no_image.jpg')
    features = models.TextField(max_length=500, default='no features')
    is_active = models.CharField(max_length=3, choices=MYCHOICES, default='YES')

    def __str__(self) -> str:
        return str(self.name)



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_complete = models.CharField(max_length=3, choices=MYCHOICES, default='NO')
    date_created = models.DateTimeField(auto_now_add=True)
    transaction_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return str(self.transaction_id)
    
    @property
    def get_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0 ,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        return self.product.price * self.quantity



class Shippingaddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)   
    name = models.CharField(max_length=200, null=True)
    address = models.TextField(max_length=100, null=True)
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    email = models.EmailField(max_length = 254)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=6, null=True)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)    
    cardnumber = models.CharField(max_length=16,validators=[MinLengthValidator(16)])
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4,validators=[MinLengthValidator(4)])
    cvv = models.CharField(max_length=3,validators=[MinLengthValidator(3)])


class Myorder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shippingaddress = models.ForeignKey(Shippingaddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSCHOICES, default='ACTIVE')
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.order.transaction_id)


class Categories(models.Model):
    name = models.CharField(max_length=100, default='no category')
    product = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return str(self.name)

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-date_created'] 

    
    def as_dict(self):

        return {
            "id": str(self.id),
            "customer": str(self.customer),
            "subject": self.subject,
            'content': self.content
        } 

    def __str__(self):
        return str(self.subject)


    

    

