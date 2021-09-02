from django.urls import path
from . import views

urlpatterns = [
    path('', views.register),
    path('register', views.register),
    path('login', views.login),

    path('dashboard', views.jobs),
    path('jobs', views.jobs),
    path('newjob', views.newjob),
    path('jobcreate', views.jobcreate),

    path('job/<int:id>', views.edit_job),
    path('job/edit/<int:id>', views.job_edited),

    path('viewjob/<int:id>', views.job),

    path('logout', views.logout),

    #Black Belt
    path('jobhelper/<int:id>', views.jobhelpercreate),
    path('destory_jobhelper/<int:id>', views.destroyjobhelper),
    path('job/<int:id>/destroy', views.jobdestroy),

    path('view', views.users_view),
]