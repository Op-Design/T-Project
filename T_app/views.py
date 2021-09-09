from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import User, Home, Year
import bcrypt

def registration(request):
    if request.method == "GET":
        return render (request, 'registration.html')
    elif request.method == "POST":
        # Validates input data meets standards in models
        errors = User.objects.registration_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/registration')
        # Sends data and creates objects is everything is verified
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
            # Saves data in sessions for future use.
            request.session['user_id'] = new_user.id
            request.session['first_name']=new_user.first_name
            return redirect('/homes')
    else:
        return redirect ('/')

def login(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            return redirect ('/homes')
        return render (request, 'login.html')
    elif request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        elif len(errors)==0:
            logged_user=User.objects.get(email=request.POST['email'])
            request.session['user_id']=logged_user.id
            request.session['first_name']=logged_user.first_name
            return redirect('/homes')
    else:
        return redirect ('/')

def homes(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            logged_user = User.objects.get(id=request.session['user_id'])
            context = {
            "homes" : Home.objects.filter(user=logged_user),
            }
            return render(request, 'homes.html', context)
    return redirect ('/')

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    return redirect('/')
    
def home_create(request):
    if request.method == 'POST':
        errors = Home.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home')
        else:
            Home.objects.create(
                name= request.POST['name'],
                location=request.POST['location'],
                description=request.POST['description'],
                user=User.objects.get(id=request.session['user_id']),
            )
            return redirect('/homes')
    return redirect('/homes')

def home_edit (request, id):
    if request.method == 'GET':
        logged_user = User.objects.get(id=request.session['user_id']):
        if Home.objects.filter(user=logged_user):

        context = {
            "id" : id,
            "job" : Job.objects.get(id=id),
        }
        return render(request,'job_edit.html',context)
    return redirect(request, '/homes')

def home_edited (request, id):
    if request.method == 'POST':
        errors = Job.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/home/{id}')
        else:
            update = Job.objects.get(id=id)
            update.title = request.POST['title']
            update.description=request.POST['description']
            update.location=request.POST['location']
            update.save()
            return redirect('/homes')
    return redirect('/homes')

def energy_use(request):
    pass
def new_report(request):
    pass
def report_create(request):
    pass

# Old stuff below

def jobs(request):
    logged_user = User.objects.get(id=request.session['user_id'])
    if request.method == "GET":
        if 'user_id' in request.session:
            context = {
            "user" : request.session,
            "all_the_jobs" : Job.objects.exclude(job_helper=logged_user).order_by("-created_at"),
            "jobs_helping" : Job.objects.filter(job_helper=logged_user),
            }
            return render(request, 'jobs.html', context)
    return redirect ('/')

def newjob(request):
    if request.method == 'GET':
        return render(request, 'new_job.html')
    return redirect('/')

def jobcreate(request):
    if request.method == 'POST':
        errors = Job.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/newjob')
        else:
            Job.objects.create(
                title= request.POST['title'],
                description=request.POST['description'],
                location=request.POST['location'],
                user=User.objects.get(id=request.session['user_id']),
            )
            return redirect('/homes')
    return redirect('/newjob')

def edit_job (request, id):
    if request.method == 'GET':
        context = {
            "id" : id,
            "job" : Job.objects.get(id=id),
        }
        return render(request,'job_edit.html',context)
    return redirect(request, '/homes')

def job_edited (request, id):
    if request.method == 'POST':
        errors = Job.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/job/{id}')
        else:
            update = Job.objects.get(id=id)
            update.title = request.POST['title']
            update.description=request.POST['description']
            update.location=request.POST['location']
            update.save()
            return redirect('/homes')
    return redirect('/homes')

def job(request, id):
    if request.method == "GET":
        context = {
            "job" : Job.objects.get(id=id),
        }
    return render(request, 'job.html', context)

def jobdestroy(request, id):
    delete = Job.objects.get(id=id)
    delete.delete()
    return redirect('/homes')

def logout(request):
    request.session.flush()
    return redirect('/')


# Black Belt
def jobhelpercreate(request,id):
    logged_user = User.objects.get(id=request.session["user_id"])
    job = Job.objects.get(id=id)
    logged_user.job_helping.add(job)
    return redirect('/homes')

def destroyjobhelper(request, id):
    logged_user = User.objects.get(id=request.session["user_id"])
    job = Job.objects.get(id=id)
    logged_user.job_helping.remove(job)
    return redirect('/homes')

def users_view(request):
    context = {
    "users" : User.objects.all(),
    }
    return render(request, 'users_view.html', context)





def edit_report(request):
    pass
def report_edited(request):
    pass