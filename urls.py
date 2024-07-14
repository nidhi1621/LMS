"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Library import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('facultyview/', views.facultyview, name='facultyview'),

    path('signupage/',views.signupage,name = 'signupage'),
    path('ViewRegister/',views.ViewRegister,name ='ViewRegister'),
    path('TC/',views.TC,name ='TC'),

    path('Contactus/',views.Contactus,name='Contactus'),
    path('aboutus/',views.aboutus,name='aboutus'),

    # path('accounts/login/', auth_views.LoginView.as_view(template_name='/home/ta-user1/Documents/LMSform/LMS/LMS/Templates/Login.html')),

    path('Userlogin/',views.Userlogin,name = 'Userlogin'),
    path('adminlogin/',views.adminlogin,name = 'adminlogin'),


    path('add/',views.add,name='add'),
    path('view/',views.view,name='view'),
     path('view_csv/',views.view_csv,name='view_csv'),

    path('viewuser/',views.viewuser,name='viewuser'),
    path('viewuser_csv/',views.viewuser_csv,name='viewuser_csv'),
    
    
    path('search/', views.search, name='search'),
    
    path('forget-password/',views.ForgetPassword,name='forget-password'),
    path('change-password/<token>/',views.ChangePassword,name='change-password'),

    path('issuebooks/', views.issuebooks, name='issuebooks'),
    path('issuebookview/', views.issuebookview, name='issuebookview'),
    path('issuebookview_csv/', views.issuebookview_csv, name='issuebookview_csv'),


    path('returnbookForm/<int:book_id>/', views.returnbookForm, name='returnbookForm'),
    path('returnbookview/',views.returnbookview,name='returnbookview'),


    path('facultydetail/',views.facultydetail,name='facultydetail'),
    path('facultydetail_csv/',views.facultydetail_csv,name='facultydetail_csv'),
    
    
    path('facultyissuebook/', views.facultyissuebook, name='facultyissuebook'),
    path('facultyissuebookview/', views.facultyissuebookview, name='facultyissuebookview'),
    path('facultyissuebookview_csv/', views.facultyissuebookview_csv, name='facultyissuebookview_csv'),


    path('facultyreturnbookForm/<int:book_id>/', views.facultyreturnbookForm, name='facultyreturnbookForm'),
    path('facultyreturnbookview/',views.facultyreturnbookview,name='facultyreturnbookview'),

    path('Update/<int:book_id>/',views.Update,name='Update'),
    # path('Updatebookview/',views.Updatebookview,name='Updatebookview'),

    path("delete_book/", views.delete_book, name="delete_book"),
    path("logout_view/", views.logout_view, name='logout_view'),
    
]
