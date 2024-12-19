from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#  Class -->Product model is defined
class Product(models.Model):
    # name = string field is created with max_lenghth of 20 cahracters
    name=models.CharField(max_length=200)
    # a text field is created for description
    description=models.TextField()
    # integer filed for stroing stock qty
    stock_quantity=models.IntegerField()
    # decimal field is created for price of the pdt
    price=models.DecimalField(max_digits=10,decimal_places=2)
    # user model is created with Foreign key
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # date time field is created / auto_now_add =True means it is added automatically
    date_created=models.DateTimeField(auto_now_add=True)
    # automatic data is set for the modification of the product
    date_modified=models.DateTimeField(auto_now=True)

# string representation method--> product model
    def __str__(self):
        # returns the product name after the pdt objct is created
        return self.name

#  class audit trail is created
class AuditTrail(models.Model):
    # foreign key is used for linkinng to the pdt model
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    # positive inetger field for storing the version number
    version=models.PositiveIntegerField()
    # string fiedl to store the pdt name
    name=models.CharField(max_length=255)
    # positive integer field for stock qty
    stock_quantity=models.PositiveIntegerField()
    # decimal field for price
    price=models.DecimalField(max_digits=10, decimal_places=2)
    # cascade is used for the user who made the chnage
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    # auto_now-->automatically recorsd the change time
    timestamp=models.DateTimeField(auto_now_add=True)
    description=models.TextField()

# unique-->ensures the each pdt and version are unique
    class Meta:
        unique_together=('product','version')  