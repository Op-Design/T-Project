from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import User, Home, ReportY
import bcrypt
from datetime import date

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

def logout(request):
    request.session.flush()
    return redirect('/')

# Home functions

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
        logged_user = User.objects.get(id=request.session['user_id'])
        errors = Home.objects.basic_validator(request.POST, logged_user)
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
        logged_user = User.objects.get(id=request.session['user_id'])
        logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
        context = {
            "id" : id,
            "home" : logged_user_home,
        }
        return render(request,'home_edit.html',context)
    return redirect(request, '/')

def home_edited (request, id):
    if request.method == 'POST':
        logged_user = User.objects.get(id=request.session['user_id'])
        errors = Home.objects.basic_validator(request.POST, logged_user)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/home/{id}')
        else:
            update = Home.objects.get(id=id)
            update.name= request.POST['name']
            update.location=request.POST['location']
            update.description=request.POST['description']
            update.save()
            return redirect('/homes')
    return redirect('/homes')

def homedestroy(request, id):
    logged_user = User.objects.get(id=request.session['user_id'])
    logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
    logged_user_home.delete()
    return redirect('/homes')

# Report functions

def noreport(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            return render(request, 'noreport.html')
        return redirect ('/')
    return redirect ('/')

def reports(request, id):
    if request.method == "GET":
        if 'user_id' in request.session:
            current_year=date.today().year
            home = id
            return redirect(f'/{home}/reports/{current_year}')
        return redirect ('/')
    return redirect ('/')

def reports_year(request, id, year):
    if request.method == "GET":
        if 'user_id' in request.session:
            logged_user = User.objects.get(id=request.session['user_id'])
            logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
            report = ReportY.objects.filter(home=logged_user_home).filter(year=year).first()
            all_reports = ReportY.objects.filter(home=logged_user_home)
            # Retreives the currently selccted year report of the current home
            context = {
            "home":logged_user_home,
            "report" : report,
            "all_reports": all_reports,
            }
            return render(request, 'report.html', context)
    return redirect ('/')

def new_report(request,id):
    # I have to create a verification here to make sure current user is home owner
    # So you don't create a report under someone else's home
    # Something like 'if Home.user == current user'
    if request.method == 'GET':
        if 'user_id' in request.session:
            logged_user = User.objects.get(id=request.session['user_id'])
            logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
            context = {
            "home":logged_user_home,
            }
            return render(request, 'input_report.html', context)
    return redirect('/')

def report_create(request,id):
    if request.method == 'POST':
        logged_user = User.objects.get(id=request.session['user_id'])
        logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
        errors = ReportY.objects.basic_validator(request.POST, logged_user_home, True)
        home = id
        year=request.POST['year']
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/{home}/new_report')
        else:
            ReportY.objects.create(
                year=year,
                jan_energy=request.POST['jan_energy'],
                feb_energy=request.POST['feb_energy'],
                mar_energy=request.POST['mar_energy'],
                apr_energy=request.POST['apr_energy'],
                may_energy=request.POST['may_energy'],
                jun_energy=request.POST['jun_energy'],
                jul_energy=request.POST['jul_energy'],
                aug_energy=request.POST['aug_energy'],
                sep_energy=request.POST['sep_energy'],
                oct_energy=request.POST['oct_energy'],
                nov_energy=request.POST['nov_energy'],
                dec_energy=request.POST['dec_energy'],
                home=logged_user_home,
            )
            return redirect(f'/{home}/reports/{year}')
    return redirect('/homes')

def edit_report(request,id,year):
    if request.method == 'GET':
        logged_user = User.objects.get(id=request.session['user_id'])
        logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
        report = ReportY.objects.filter(home=logged_user_home).filter(year=year).first()
        # Retreives the currently selccted year report of the current home
        context = {
        "home":logged_user_home,
        "report" : report,
        }
        return render(request,'report_edit.html',context)
    return redirect(request, '/')

def report_edited(request,id,year):
    if request.method == 'POST':
        logged_user = User.objects.get(id=request.session['user_id'])
        logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
        errors = ReportY.objects.basic_validator(request.POST, logged_user_home, False)
        home = id
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/{home}/edit_report/{year}')
        else:
            update = ReportY.objects.filter(home=logged_user_home).filter(year=year).first()
            update.jan_energy=request.POST['jan_energy']
            update.feb_energy=request.POST['feb_energy']
            update.mar_energy=request.POST['mar_energy']
            update.apr_energy=request.POST['apr_energy']
            update.may_energy=request.POST['may_energy']
            update.jun_energy=request.POST['jun_energy']
            update.jul_energy=request.POST['jul_energy']
            update.aug_energy=request.POST['aug_energy']
            update.sep_energy=request.POST['sep_energy']
            update.oct_energy=request.POST['oct_energy']
            update.nov_energy=request.POST['nov_energy']
            update.dec_energy=request.POST['dec_energy']
            update.save()
            # return redirect(f'{name}/reorts')
            return redirect(f'/{home}/reports/{year}')
    return redirect('/homes')
    
def reportdestroy(request, id, year):
    logged_user = User.objects.get(id=request.session['user_id'])
    logged_user_home = Home.objects.filter(user=logged_user).filter(id=id).first()
    report = ReportY.objects.filter(home=logged_user_home).filter(year=year).first()
    report.delete()
    return redirect(f'/{id}/reports')

# Transition functions

def transition(request):
    if request.method == 'GET':
        if 'user_id' in request.session:
            return render(request, 'coming_soon.html')
    return redirect('/')

# Community functions

def community(request):
    if request.method == 'GET':
        if 'user_id' in request.session:
            return render(request, 'coming_soon.html')
    return redirect('/')








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
