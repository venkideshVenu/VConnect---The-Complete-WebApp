from django.urls import path
from . import views

app_name = 'bikeshare'

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('select-role/', views.select_role, name='select_role'),
    path('customer/', views.customer_page, name='bikeshare-customer'),
    path('manager/', views.manager_page, name='bikeshare-manager'),
    path('operator/', views.operator_page, name='bikeshare-operator'),


    
    path('top-up/', views.top_up_balance, name='top-up'),
    path('top-up/submit/', views.submit_top_up, name='top-up-submit'),


    path('pay-balance/', views.pay_balance, name='pay-balance'),
    path('pay-balance/submit/', views.submit_pay_balance, name='pay-balance-submit'),

    
    path('customer/<int:station_id>/rent', views.rent_bike, name='rent_bike'),
    path('customer/<int:order_id>/return', views.return_bike, name='return_bike'),
    path('customer/<int:order_id>/report_faulty', views.report_faulty, name='report_faulty'),

    
    path('operator/<int:bike_id>/repair_bike', views.repair_bike, name='repair_bike'),
    path('operator/<int:bike_id>/move_bike', views.move_bike, name='move_bike')

]