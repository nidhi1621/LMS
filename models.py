from django.db import models
from django.contrib.auth.models import User
#from django.db.models.fields import CharField

# Create your models here.

class signupdetail(models.Model):
    FirstName = models.CharField(max_length=50,null=True)
    LastName = models.CharField(max_length=50,null=True)
    Email = models.EmailField(max_length=20, null=True)
    Password = models.CharField(max_length=50,default='')
    confirmpassword = models.CharField(max_length=50,default='')
    forget_password_token = models.CharField(max_length=100, blank=True)
    role_choice = (
        ('S' , 'Student'),
        ('F','Faculty')
    )
    Role = models.CharField(max_length=1, choices=role_choice, default='')
    checkbox = models.BooleanField(default=False)

class viewsignup(models.Model):
    username = models.CharField(max_length=50)
    role_choice = (
        ('Student' , 'Student'),
        ('Faculty','Faculty')
        )
    Role = models.CharField(max_length=20, choices=role_choice, default='')

class userlogin(models.Model):
    Email = models.EmailField(max_length=20, null=True)
    password = models.CharField(max_length=30)

class Viewlogin(models.Model):
    username = models.CharField(max_length=50)
    # Email = models.EmailField(max_length=70,blank=True,unique=True)

class addbook(models.Model):
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=50)
    Author_Name = models.CharField(max_length=50)
    isbn = models.PositiveIntegerField(null=True)
    CATEGORY_CHOICES = [
        ('IT & Technology', 'IT & Technology'),
        ('Management', 'Management'),
        ('Arts', 'Arts'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='')
    total_copies = models.IntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=0)
    Book_Status = (
        ('Available','Available'),
        ('Issued','Issued')
    )
    book_status = models.CharField(max_length=20, choices=Book_Status, default='')
   
    def __str__(self):
        return f"{self.book_id} {self.book_name}"


class view(models.Model):
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=50)
    Author_Name = models.CharField(max_length=50)
    isbn = models.PositiveIntegerField(null=True)
    CATEGORY_CHOICES = [
        ('IT & Technology', 'IT & Technology'),
        ('Management', 'Management'),
        ('Arts', 'Arts'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='')
    Book_Status = (
        ('Avaliable' , 'Avaliable'),
        ('Issued','Issued')
        )
    book_Status = models.CharField(max_length=20, choices=Book_Status, default='')                                                                                                                                                                          

def __str__(self):
    return f"{self.book_id} {self.book_name}"


class IssueBooks(models.Model):
    book = models.ForeignKey(addbook, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    issue_date = models.DateField()
    course = models.CharField(max_length=50)
    
    def __str__(self):
        return self.student_name


class returnbooks(models.Model):
    book = models.ForeignKey(IssueBooks, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=50)
    issue_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return self.student_name


class FacultyIssueBooks(models.Model):
    book = models.ForeignKey(addbook, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=50)
    Faculty_id = models.CharField(max_length=20)
    Faculty_name = models.CharField(max_length=100)
    Department = [
        ('IT & Technology', 'IT & Technology'),
        ('Management', 'Management'),
        ('Arts', 'Arts'),
    ]
    department = models.CharField(max_length=50, choices=Department, default='')
    issue_date = models.DateField()
    returned = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.Faculty_name


class Facultyreturnbooks(models.Model):
    book = models.ForeignKey(FacultyIssueBooks, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=50)
    Faculty_id = models.CharField(max_length=20)
    Faculty_name = models.CharField(max_length=50)
    Department = [
        ('IT & Technology', 'IT & Technology'),
        ('Management', 'Management'),
        ('Arts', 'Arts'),
    ]
    department = models.CharField(max_length=50, choices=Department, default='')
    issue_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return self.Faculty_name

class Updatebook(models.Model):
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=50)
    

    

