from django.contrib import admin
from django.urls import path
        
# ]
from django.contrib.auth import views as auth_views 
from .views import Index, SignUpView, Dashboard, AddProduct, EditProduct, DeleteProduct, AuditView, logout_view
urlpatterns = [
    path('',Index.as_view(),name='index'),
    # for dashboard
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
    # for sign up
    path('signup/',SignUpView.as_view(),name='signup'),
    # for adding pdt
    path('add-product/',AddProduct.as_view(),name='add-product'),
    # for editing pdt
    path('edit-product/<int:pk>/',EditProduct.as_view(),name='edit-product'),
    # for deleting pdt
    path('delete-product/<int:pk>/',DeleteProduct.as_view(),name='delete-product'),
    # for aduir trail--audting
    path('audit/<int:pk>/',AuditView.as_view(),name='audit'),
    
    #adding login and logout url links
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),  
    path('logout/',logout_view, name='logout'),  
]