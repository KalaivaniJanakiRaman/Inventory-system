from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, ProductForm
from .models import Product, AuditTrail
from django.contrib import messages

# te,plate view
# template_name-->specifies teh template file to be used for this view
class Index(TemplateView):
    template_name = 'index.html'

#dashboard
# view ->requires login part 
# LoginRequiredMixin-->ensures only authenticated users can access this view
# user not logged out--redirects to login pg
class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        # def get--handles get request
        # pdts=pdt.objects.all()-->retrieves all pdt object from database by id
        products=Product.objects.all().order_by('id') 
        # renders dashboard.html
        # passes= pdt.queryset
        # so that the tempalte will show the list of pdts
        return render(request,'dashboard.html',{'products':products})
# view class that handles sign up for new usres
class SignUpView(View):
    # def get --request HTTP
    def get(self,request):
        # UserRegisterForm--Django form 
        # contains field slike usre name, email, password
        form=UserRegisterForm()
        # render signup template
        # it will access the template to display form to the user
        return render(request,'signup.html',{'form':form})
# def post--handles post hhtp request
    def post(self,request):
        # UserRegisterForm passes the submiited data
        # allows the form to validate the user input
        form=UserRegisterForm(request.POST)
        # checks for validity
        if form.is_valid():
            # creates a new user if the form is valid
            user=form.save()
            # login --user is loggedin 
            login(request,user)
            # a success messafe is shown
            messages.success(request,"Account created successfully!")
            return redirect('dashboard')
        # redirect to the dashboard-- url
        # if form is not valid, returns to sign up page
        # form will be displayed 
        return render(request,'signup.html',{'form':form})
# class aadd pdt
# CreateView-->generic class based view
# 
class AddProduct(LoginRequiredMixin,CreateView):
    # model=pdt instances
    model=Product
    # for pdt creation
    form_class=ProductForm
    # specifying the template for pdt creation
    template_name='item_form.html'
    # reverse_lazy-->used for resolving the run time delay
    # after successful pdt creation, it is redirected to dashbord
    success_url=reverse_lazy('dashboard')
# def form_valid -->loggedin user-->associated with newly created pdt
    def form_valid(self, form):
        # 
        form.instance.user=self.request.user  
        # calls--parent class-form_valid -->to save pdt instance
        response=super().form_valid(form)
        # audittrail->creates new pdt
        # it stores the follwing fields
        AuditTrail.objects.create(
            # name, pdt, stock_qty, price and user
            product=self.object,
            version=1,
            name=self.object.name,
            stock_quantity=self.object.stock_quantity,
            description=self.object.description,
            price=self.object.price,
            user=self.request.user
        )
        # returns the response after the audit trail
        return response
# LoginRequiredMixin--used only authenticatwd user can access this view
# 
class EditProduct(LoginRequiredMixin,UpdateView):
    model=Product
    # used a custom form-pdt form, for adding additional fields
    form_class=ProductForm
    # template-item_form
    template_name='item_form.html'
    # reverse_lazy for avoiding time delay
    success_url=reverse_lazy('dashboard')
# form_valid function
    def form_valid(self,form):
        # called the parent form_valid -->handles HTTP response
        response=super().form_valid(form)
        # retrives latest version of the audit trail
        latest_version=AuditTrail.objects.filter(product=self.object).order_by('-version').first()
        # cretaes a new version for the audit trail
        new_version=latest_version.version + 1 if latest_version else 1
        # stores the details like pdt,version, name,stock_qty, price
        AuditTrail.objects.create(
            product=self.object,
            version=new_version,
            name=self.object.name,
            stock_quantity=self.object.stock_quantity,
             description=self.object.description,
            price=self.object.price,
            user=self.request.user
        )
        # returns the response
        return response
# class delete pdt
# 
class DeleteProduct(LoginRequiredMixin,DeleteView):
    # model-->
    # template->refers to delete-item 
    model=Product
    template_name='delete_item.html'
    success_url=reverse_lazy('dashboard')
    # helpful for easy access-->template-->context
    context_object_name='product'
# custom delete function
# arguments , keyword argumnets
    def delete(self,request,*args,**kwargs):
        # get_object()--> method to get or retrieve object
        product=self.get_object()
        # retruves the latestverions
        latest_version=AuditTrail.objects.filter(product=product).order_by('-version').first()
        # retruves the new version
        new_version=latest_version.version + 1 if latest_version else 1
# audit trail object with details/ fields like pdt, version, name, stock_qty
        AuditTrail.objects.create(
            product=product,
            version=new_version,
            name=product.name,
            stock_quantity=0,  
            price=product.price,
            description=self.object.description,
            user=self.request.user
        )
        # delete method is called
        return super().delete(request,*args,**kwargs)

class AuditView(LoginRequiredMixin, View):
    # get method
    # pk-primary key--values with id for a pdt
    def get(self,request,pk):
        # retirves pdt with their pk
        product=Product.objects.get(pk=pk)
        # this is used to filter the pdt with recent audit trail
        audit_trail=AuditTrail.objects.filter(product=product).order_by('-version')
        return render(request,'audit.html',{'product':product,'audit_trail':audit_trail})
# logout view, with message after successfully logged out.
def logout_view(request):
    logout(request)
    messages.info(request,"You have been logged out.")
    # redirects to login page
    return redirect('login')