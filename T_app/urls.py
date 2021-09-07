from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('registration', views.registration),
    path('login', views.login),

    path('homes', views.homes),
    path('new_home', views.new_home),
    path('home_create', views.home_create),

    path('energy_use', views.energy_use),
    path('new_report', views.new_report),
    path('report_create', views.report_create),

    path('edit_report/<int:id>', views.edit_report),
    path('report_edited/<int:id>', views.report_edited),

    path('logout', views.logout),




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