from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('registration', views.registration),
    path('login', views.login),
    path('logout', views.logout),


    path('homes', views.homes),
    path('new_home', views.home),
    path('home_create', views.home_create),
    path('home/<int:id>', views.home_edit),
    path('home/edit/<int:id>', views.home_edited),
    path('home/<int:id>/destroy', views.homedestroy),

    path('noreport', views.noreport),
    path('<int:id>/reports', views.reports),
    path('<int:id>/reports/<int:year>', views.reports_year),
    path('<int:id>/new_report', views.new_report),
    path('<int:id>/report_create', views.report_create),
    path('<int:id>/edit_report/<int:year>', views.edit_report),
    path('<int:id>/report_edited/<int:year>', views.report_edited),
    path('<int:id>/report/<int:year>/destroy', views.reportdestroy),



    path('transition', views.transition),
    path('community', views.community),
    

    path('view', views.users_view),
]