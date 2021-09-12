from django.db import models
import re, bcrypt, calendar

class UserManager (models.Manager):
    def registration_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email = User.objects.filter(email=postData['email'])
        if len(postData['first_name'])<2:
            errors['first_name']='First name should be at least 2 characters long'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name should be at least 2 characters long'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = 'Invalid email address'
        if len(postData['email'])==None:
            errors['email_len']='Email address required'
        if email:
            errors['email_unique']='Email is already in system'
        if len(postData['password'])<5:
            errors['password']='Password should be at least 5 characters long'
        if not postData['password']==postData['c_password']:
            errors['password_c']='Passwords should match'
        return errors
  
    def login_validator(self,postData):
        errors={}
        email = User.objects.filter(email=postData['email'])
        if not email:
            errors['creds']='Invalid Credentials'
        else:
            if email:
                logged_user = email[0]
                if not bcrypt.checkpw(postData['password'].encode(),logged_user.password.encode()):
                    errors['creds']='Invalid Credentials'
        return errors

class HomeManager (models.Manager):
    def basic_validator(self,postData,user):
        errors={}
        home = Home.objects.filter(user=user).filter(name=postData['name'])
        if home:
            errors['home_unique']='A home with this name has already been created. Please choose a different home.'
        if len(postData['name'])<2:
            errors['name']='Name should be at least 2 characters long'
        return errors

class ReportYManager (models.Manager):
    def basic_validator(self,postData,home,create):
        errors={}
        if create == True:
            year = ReportY.objects.filter(home=home).filter(year=postData['year'])
            if year:
                errors['year_unique']='A report for this year has already been created. Try editing the report instead.'
        if len(postData['jan_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['feb_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['mar_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['apr_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['may_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['jun_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['jul_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['aug_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['sep_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['oct_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['nov_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        if len(postData['dec_energy'])<1:
            errors['energy']='Energy use should be at least 1 kWh'
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    
    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} ({self.id})>"

# Homes . . . User:Homes . . . 1:M
# Yearly . . . Homes:Yearly . . . 1:M
# Monthly . . . Homes:Monthly . . . 1:M
# Weekly . . . Homes:Weekly . . . 1:M
# Daily . . . Homes:Daily . . . 1:M

class Home(models.Model):
    name=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="user_home", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=HomeManager()
    
    def __repr__(self):
        return f"<Home: {self.name} ({self.location})>"

class ReportY(models.Model):
    year=models.IntegerField()
    jan_energy=models.IntegerField()
    feb_energy=models.IntegerField()
    mar_energy=models.IntegerField()
    apr_energy=models.IntegerField()
    may_energy=models.IntegerField()
    jun_energy=models.IntegerField()
    jul_energy=models.IntegerField()
    aug_energy=models.IntegerField()
    sep_energy=models.IntegerField()
    oct_energy=models.IntegerField()
    nov_energy=models.IntegerField()
    dec_energy=models.IntegerField()
    home = models.ForeignKey(Home, related_name="home_year", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ReportYManager()
    
    def __repr__(self):
        return f"<Year: {self.home.user} ({self.home}) ({self.year})>"

