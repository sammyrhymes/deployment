from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    # path('register/', views.register_user, name='register'),
    path('user_auth/', views.user_auth, name='user_auth'),
    path('login_user/', views.login_user, name='login-user'),
    path('logout_user/', views.logout_user, name='logout-user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('competitions/', views.competitions, name='competitions'),
    path('competition/<int:competition_id>/', views.competition_details, name='competition'),
    path('competition/<int:id>/add_to_basket/', views.add_to_basket, name='add_to_basket'),
    path('basket/', views.view_basket, name='view_basket'),
    path('token/', views.token, name="token"),
    path('check_out/', views.check_out, name = 'check_out'),
    path('stk/', views.stk, name="stk"),
    path('base/', views.base, name='base'),
    path('portfolio-details/', views.portfolio, name='portfolio-details'),
    path('service-details/', views.service, name='service-details'),
    path('starter-page/', views.starter, name='starter-page'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failure, name='payment_failure'),
    path('remove_from_basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
      ]