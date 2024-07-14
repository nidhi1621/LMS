from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date,datetime,timedelta
from django.core.exceptions import ValidationError
from .forms import *
from .models import *
import csv
from django.db.models import Sum,Count,F,Q
import re
import uuid
from django.core.mail import send_mail

from django.conf import settings 

# Create your views here.

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def TC(request):
    return render(request, "T&C.html")

def Contactus(request):
    return render(request,'Contact us.html')

def aboutus(request):
    return render(request,'about-us.html')

def adminlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add")
            else:
                return HttpResponse("You are not an admin.")
        else:
            if username == 'superuser':
                User.objects.create_superuser(username=username, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("/add")
            else:
                alert = True
                return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

    
def signupage(request):
    if request.method == "POST":
        FirstName = request.POST.get('FirstName')
        LastName = request.POST.get('LastName')
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        confirmpassword = request.POST.get('confirmpassword')
        Role = request.POST.get('Role')
        checkbox = request.POST.get('cb1')== 'on'

        if not FirstName or not Email or not Role:
            messages.error(request, '*Please fill in all required fields.')
            return render(request, "Register.html")

        if signupdetail.objects.filter(FirstName=FirstName).exists():
            messages.error(request,'Username is already taken.')
            return render(request, "Register.html")
        
        if Password != confirmpassword:
            messages.error(request,'Password and confirm password do not match.')
            return render(request, "Register.html")
    
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{1,8}$', Password):
            messages.error(request, '*Password should be alphanumeric with a special character,*Password must contain at least 1 capital letter,*Password should not be longer than 8 characters.')
            alert_message = list(messages.get_messages(request))[-1]
            alert_type = 'alert-danger' 
            return render(request, "Register.html", {'alert_message': alert_message, 'alert_type': alert_type})
        
        sign = signupdetail(FirstName=FirstName, LastName=LastName, Email=Email, Password=Password, confirmpassword=confirmpassword, Role=Role,checkbox=checkbox)
        sign.save()
        return redirect('Userlogin')

    return render(request, 'Register.html')

def ViewRegister(request):
    data = signupdetail.objects.all()
    return render(request, "Viewregister.html", {'data': data})

def users(Email, password):
    try:
        user = signupdetail.objects.get(Email=Email)
        if user.Password == password:
            return user
    except signupdetail.DoesNotExist:
        pass
    return None

def Userlogin(request):
    if request.method == "POST":
        Email = request.POST.get('Email')
        password = request.POST.get('password')
        user = users(Email, password)

        if user is not None:
            if user.Role == 'Student': 
                login(request, user)
                request.session['user_id'] = user.id  
                return redirect("home") 
            elif user.Role == 'Faculty': 
                login(request, user)
                request.session['user_id'] = user.id  
                return redirect("facultyview") 
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect("Userlogin")
    return render(request, "Login.html")


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            Email = request.POST.get('Email')
            
            if not signupdetail.objects.filter(Email=Email).exists():
                messages.success(request, 'No user found with this email.')
                return render(request, "Login.html")

            token = str(uuid.uuid4())

            user = signupdetail.objects.get(Email=Email)
            user.forget_password_token = token
            user.save()

            send_forget_password_mail(user.Email, token)

            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
        
    except Exception as e:
        print(e)
    return render(request, "forget_password.html")

def send_forget_password_mail(Email , token ):
    subject = 'Your forget password link'
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def ChangePassword(request, token):
    context = {}
    try:
        user = signupdetail.objects.get(forget_password_token=token)
        if user:
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('reconfirm_password')

                if new_password != confirm_password:
                    messages.success(request, 'Both passwords should be equal.')
                    return redirect(f'/change-password/{token}/')
                
                if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{1,8}$',new_password):
                    messages.error(request, '*Password should be alphanumeric with a special character,*Password must contain at least 1 capital letter,*Password should not be longer than 8 characters.')
                    alert_message = list(messages.get_messages(request))[-1]
                    alert_type = 'alert-danger' 
                    return render(request, f'/change-password/{token}/', {'alert_message': alert_message, 'alert_type': alert_type})

                user.Password = new_password
                user.confirmpassword= new_password
                user.save()

                return redirect('/Userlogin/')

            context = {'user': user}
            print(context)

    except Exception as e:
        print(e)

    return render(request, "password_reset_confirm.html", context)


def add(request):
    if request.method == "POST":
        add = addbook()
        add.book_id = request.POST.get("book_id")
        add.book_name = request.POST.get('book_name')
        add.Author_Name = request.POST.get('Author_Name')
        add.isbn = request.POST.get('isbn')
        add.category = request.POST.get('category')
        add.total_copies = request.POST.get('total_copies')
        add.available_copies = request.POST.get('available_copies', add.total_copies)
        add.book_status = request.POST.get('book_status', 'Available') 

        if addbook.objects.filter(book_id=add.book_id).exists():
            messages.error(request,'Book ID is already taken.')
            return render(request, "Addpage.html")
        
        add.save()
        add = addbook.objects.all()
        messages.success(request, 'Book added successfully!')
        return render(request,"Addpage.html",{'add':add})
    else:
        return render(request, 'Addpage.html')
    
def view(request):
    data = addbook.objects.all()
    num_issued_books = IssueBooks.objects.count()
    num_available_books = addbook.objects.filter(book_status='Available').aggregate(Sum('total_copies'))['total_copies__sum']
    context = {'data':data,'num_issued_books':num_issued_books,'num_available_books':num_available_books}
    return render(request,'Viewpage.html',context)

def view_csv(request):
    data = addbook.objects.all()
    num_issued_books = IssueBooks.objects.count()
    num_available_books = addbook.objects.filter(book_status='Available').aggregate(Sum('total_copies'))['total_copies__sum']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="available_books.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book ID', 'Book Name', 'Author', 'Total Copies', 'Available Copies'])

    for book in data:
        writer.writerow([book.book_id, book.book_name, book.Author_Name, book.total_copies, book.available_copies])

    return response
       
       
def viewuser(request):
    data = addbook.objects.all()
    book_issues = IssueBooks.objects.values('book__book_id', 'book__book_name', 'book__Author_Name', 'student_name', 'issue_date').annotate(total_issued=Count('book'), total_available=F('book__total_copies') - Count('book'))
    query = request.GET.get('q', '').strip()
    if query:
        data = data.filter(Q(book_name__icontains=query) | Q(Author_Name__icontains=query))
    return render(request,'userview.html',{'data':data,'book_issues':book_issues})

def viewuser_csv(request):
    data = addbook.objects.all()
    book_issues = IssueBooks.objects.values('book__book_id', 'book__book_name', 'book__Author_Name', 'student_name', 'issue_date').annotate(total_issued=Count('book'), total_available=F('book__total_copies') - Count('book'))
    query = request.GET.get('q', '').strip()
    if query:
        data = data.filter(Q(book_name__icontains=query) | Q(Author_Name__icontains=query))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="issued_books_to_users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Book ID', 'Book Name', 'Author', 'Issue Date'])

    for issue in book_issues:
        writer.writerow([issue['student_name'], issue['book__book_id'], issue['book__book_name'], issue['book__Author_Name'], issue['issue_date']])

    return response

def search(request):
    query = request.GET.get('q', '').strip()
    results = addbook.objects.filter(Q(book_name__icontains=query) | Q(Author_Name__icontains=query)| Q(book_status__icontains=query))
    return render(request, 'searchresult.html', {'results': results, 'query': query})

def issuebooks(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        add_book = get_object_or_404(addbook, book_id=book_id)
        if add_book.available_copies <= 0:
            messages.error(request, 'Sorry, all copies of this book have already been issued.')
            return redirect('issuebookview')
        issue_date_str = request.POST.get('issue_date')
        issue_date = datetime.strptime(issue_date_str, '%d/%m/%Y').date()
        book = IssueBooks.objects.create(
            student_id=request.POST.get('student_id'),
            student_name=request.POST.get('student_name'),
            book=add_book,
            issue_date=issue_date,
            course=request.POST.get('course')
        )
        add_book.available_copies -= 1
        add_book.save()
        messages.success(request, 'Book issued successfully!')
        return redirect('issuebookview')
    else:
        context = {'add_books': addbook.objects.filter(available_copies__gt=0)}
        return render(request, 'Issuedbook.html', context)

def issuebookview(request):
    book = IssueBooks.objects.all()
    return render(request, "IssueBookdetails.html", {'book': book})

def issuebookview_csv(request):
    books = IssueBooks.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="issued_books.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book ID','Book Name','Student ID', 'Student Name', 'Course', 'Issue Date'])

    for book in books:
        writer.writerow([book.book.book_id,book.book.book_name,book.student_id,book.student_name,book.course,book.issue_date])

    return response


def returnbookForm(request, book_id):
    book = IssueBooks.objects.get(book__id=book_id)
    if request.method == "POST":
        rb = returnbooks()
        rb.book = book
        rb.book_name = book.book_name
        rb.student_id = book.student_id
        rb.student_name = book.student_name
        issue_date_str = request.POST.get('issue_date')
        return_date_str = request.POST.get('return_date')
        if issue_date_str and return_date_str:
            issue_date = datetime.strptime(issue_date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            return_date = datetime.strptime(return_date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            rb.issue_date = issue_date
            rb.return_date = return_date
            max_days = 7
            days_diff = (datetime.strptime(return_date, '%Y-%m-%d') - datetime.strptime(issue_date, '%Y-%m-%d')).days
            if days_diff > max_days:
                messages.warning(request, f'*Book should be returned within {max_days} days of the issue date.')
            else:
                rb.save()
                messages.success(request, 'Book returned successfully.')
                book.delete()
                return redirect('returnbookview') 
        else:
            messages.error(request, 'Please enter both issue date and return date.')
    context = {'book': book}
    return render(request, 'return.html', context)


def returnbookview(request):
    rb = returnbooks.objects.all()
    return render(request,'returnbookdetails.html',{'rb': rb})


def Update(request,book_id):
    data = addbook.objects.get(book_id=book_id)
    if request.method == "POST":
        data.book_id = request.POST.get("book_id")
        data.book_name = request.POST.get('book_name')
        data.save()
        messages.success(request, 'Book details updated successfully!')
        return redirect('view')
    else:
        return render(request, 'Update.html', {'data': data})

def delete_book(request):
    book_id = request.POST['book_id']
    addbook.objects.filter(book_id=book_id).delete()
    return render(request, 'book_delete.html')

def logout_view(request):
    del request.session['user_id']  
    logout(request)
    return redirect('home')

def facultyview(request):
    return render(request, "facultyview.html")

def facultydetail(request):
    data = addbook.objects.all()
    book_issues = FacultyIssueBooks.objects.values('book__book_id', 'book__book_name', 'book__Author_Name', 'book__total_copies', 'Faculty_name','department').annotate(total_issued=Count('book'), total_available=F('book__total_copies') - Count('book'))

    query = request.GET.get('q', '').strip()
    if query:
        data = data.filter(Q(book_name__icontains=query) | Q(Author_Name__icontains=query))
    return render(request,'facultydetail.html',{'data':data,'book_issues':book_issues})


def facultydetail_csv(request):
    data = addbook.objects.all()
    book_issues = FacultyIssueBooks.objects.values('book__book_id', 'book__book_name', 'book__Author_Name', 'book__total_copies', 'Faculty_name','department').annotate(total_issued=Count('book'), total_available=F('book__total_copies') - Count('book'))

    query = request.GET.get('q', '').strip()
    if query:
        data = data.filter(Q(book_name__icontains=query) | Q(Author_Name__icontains=query))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="faculty_book_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book ID', 'Book Name', 'Author', 'Total Copies', 'Total Issued', 'Total Available', 'Faculty Name', 'Department'])

    for issue in book_issues:
        writer.writerow([issue['book__book_id'], issue['book__book_name'], issue['book__Author_Name'], issue['book__total_copies'], issue['total_issued'], issue['total_available'], issue['Faculty_name'], issue['department']])

    return response

def facultyissuebook(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        add_book = get_object_or_404(addbook, book_id=book_id)
        if add_book.available_copies <= 0:
            messages.error(request, 'Sorry, all copies of this book have already been issued.')
            return redirect('issuebookview')
        issue_date_str = request.POST.get('issue_date')
        issue_date = datetime.strptime(issue_date_str, '%d/%m/%Y').date()
        book = FacultyIssueBooks.objects.create(
            Faculty_id=request.POST.get('Faculty_id'),
            Faculty_name=request.POST.get('Faculty_name'),
            book=add_book,
            issue_date=issue_date,
            department=request.POST.get('department')
        )
        add_book.available_copies -= 1
        add_book.save()
        messages.success(request, 'Book issued successfully!')
        return redirect('facultyissuebookview')
    else:
        context = {'add_books': addbook.objects.filter(available_copies__gt=0)}
        return render(request, 'facultyissuebook.html', context)
    
def facultyissuebookview(request):
    book = FacultyIssueBooks.objects.all()
    return render(request, "facultyissuebookview.html", {'book': book})

def facultyissuebookview_csv(request):
    book = FacultyIssueBooks.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="faculty_issued_books.csv"'

    writer = csv.writer(response)
    writer.writerow(['Faculty Name', 'Book ID', 'Book Name', 'Author', 'Issue Date'])

    for issue in book:
        writer.writerow([issue.Faculty_name, issue.book.book_id, issue.book.book_name, issue.book.Author_Name, issue.issue_date])

    return response

def facultyreturnbookForm(request, book_id):
    book = FacultyIssueBooks.objects.get(book__id=book_id)
    if request.method == "POST":
        rb = Facultyreturnbooks()
        rb.book = book
        rb.book_name = book.book_name
        rb.Faculty_id = book.Faculty_id
        rb.Faculty_name = book.Faculty_name
        issue_date_str = request.POST.get('issue_date')
        return_date_str = request.POST.get('return_date')
        if issue_date_str and return_date_str:
            issue_date = datetime.strptime(issue_date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            return_date = datetime.strptime(return_date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            rb.issue_date = issue_date
            rb.return_date = return_date
            max_days = 7
            days_diff = (datetime.strptime(return_date, '%Y-%m-%d') - datetime.strptime(issue_date, '%Y-%m-%d')).days
            if days_diff > max_days:
                messages.warning(request, f'*Book should be returned within {max_days} days of the issue date.')
            else:
                rb.save()
                messages.success(request, 'Book returned successfully.')
                book.delete()
                return redirect('facultyreturnbookview') 
        else:
            messages.error(request, 'Please enter both issue date and return date.')
    context = {'book': book}
    return render(request, 'facultyreturnbookForm.html', context)


def facultyreturnbookview(request):
    rb = Facultyreturnbooks.objects.all()
    return render(request,'facultyreturnbookview.html',{'rb': rb})




