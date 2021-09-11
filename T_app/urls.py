from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('registration', views.registration),
    path('login', views.login),

    path('homes', views.homes),
    path('new_home', views.home),
    path('home_create', views.home_create),
    path('home/<int:id>', views.home_edit),
    path('home/edit/<int:id>', views.home_edited),

    path('<str:name>/reports', views.reports),
    path('<str:name>/reports/<string:year>', views.reports_year),
    path('new_report', views.new_report),
    path('report_create', views.report_create),

    path('<str:name>/edit_report/<int:year>', views.edit_report),
    path('<str:name>/report_edited/<int:year>', views.report_edited),

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