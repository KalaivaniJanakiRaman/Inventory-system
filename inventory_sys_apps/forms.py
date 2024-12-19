from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product

# for user registration
class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField(max_length=30,required=True)
    last_name=forms.CharField(max_length=30,required=True)
    # for user details
    class Meta:
        model=User
        # fields required for user creation
        fields=['username','first_name','last_name','password1','password2']

# for product form to get details like name,description,stock qty,price
class ProductForm(forms.ModelForm):
    # fields required for pdt creation
    class Meta:
        model=Product
        fields=['name','description','stock_quantity','price']

# kwargs--> keyword arguments--> it is passed to __int__
    def __init__(self,*args,**kwargs):
        # user--> assigned to user atribute through kwargs
        # defaulr is set to none --> if not provided
        self.user=kwargs.pop('user', None)
        # superclass--> it calls the __int__method of the parent class
        # super function-->ensures parent class logic runs while going customisation
        super(ProductForm,self).__init__(*args,**kwargs)

# for saving contents
# custom save method
    def save(self,commit=True):
        # calls the parent class save method
        # commit=false/ without committing to the database
        instance=super(ProductForm, self).save(commit=False)
        # if commit =true , save instance to the database
        if self.user:
            instance.user=self.user
        if commit:
            instance.save()
        return instance

# commit=false==used if additinal modificaations are required
# return instance-->it returns the saved or modified instance