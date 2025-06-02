# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("", login_view, name="login"),
    path("logout/", user_logout, name="logout"),
    # path("dashboard/", dashboard, name="dashboard"),
    path('employee_report/<int:user_id>/', employee_report, name='employee_report'),  # New URL pattern
    path('activity/<int:activity_id>/confirm-delete/', confirm_delete_activity, name='confirm_delete_activity'),
    path('activity/<int:activity_id>/confirm-delete_dpcr/', confirm_delete_activity_dpcr, name='confirm_delete_activity_dpcr'),
    path('activity/<int:activity_id>/delete/', delete_activity, name='delete_activity'),
    path('activity/<int:activity_id>/delete_dpcr/', delete_activity_dpcr, name='delete_activity_dpcr'),
    path('activities/<int:user_id>/', ActivitiesView.as_view(), name='activities'),    
    
    path('opcr-smart-kpi/<int:pk>/', update_opcr_smart_kpi, name='update_opcr_smart_kpi'),
    path('opcr-smart-kpi/list/', opcr_smart_kpi_list, name='opcr_smart_kpi_list'),
    path('opcr-smart-kpi/list/all', opcr_smart_kpi_list_all, name='opcr_smart_kpi_list_all'),
    path('opcr-smart-kpi/add/', opcr_smart_kpi_page, name='add_opcr_smart_kpi'),  # Add view


    
    path('landing/', landing_page, name='landing_page'),  
    path('add-ipcr-opcr/', add_ipcr_opcr, name='add_ipcr_opcr'),
    path('add-ipcr-dpcr/', add_ipcr_dpcr, name='add_ipcr_dpcr'),
    path('add/', add_ipcr_opcr, name='add_ipcr_opcr'),
    path('update/<int:pk>/', update_ipcr_opcr, name='update_ipcr_opcr'),
    path('update_dpcr/<int:pk>/', update_ipcr_dpcr, name='update_ipcr_dpcr'),
    # path('message/', show_message, name='show_message'),  # Add this line
    path('smart-kpi-not-in-activities/', smart_kpi_not_in_activities_view, name='smart_kpi_not_in_activitiesopcr'),
    path('employees/', employee_list, name='employee_list'),
    path('employee/update/<int:employee_id>/', update_employee, name='update_employee'),
    # path('update-opcr-smart-kpi/<int:pk>/', update_opcr_smart_kpi, name='update_opcr_smart_kpi'),
   
    path('lock-profile/', lock_employee_profile, name='lock_profile'),
    # path('missing-dpcr-kpi/', missing_dpcr_kpi_view, name='missing_dpcr_kpi'),
    
    path('select-employee/', select_employee_view, name='select_employee'),  # New path for selecting employees
    #path('employee/<int:employee_id>/activities/', employee_activity_view, name='employee_activities'),
    # path('employee_report/', employee_report, name='employee_report'),
    # path('activities/', activity_view, name='activity_view'),

    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('pdf-preview/', pdf_preview, name='pdf_preview'),




    path('opcr-smart-kpi_rating/<int:pk>/', rate_opcr_smart_kpi, name='rate_opcr_smart_kpi'),
    path('opcr-smart-kpi_rating_rate/<int:pk>/', rate_opcr_smart_kpi_rate, name='rate_opcr_smart_kpi_rate'),
    path('delete-opcr-smart-kpi/<int:pk>/', delete_opcr_smart_kpi, name='delete_opcr_smart_kpi'),
    
    path('export/', export_to_excel, name='export_to_excel'),
    
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_add'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    

]

