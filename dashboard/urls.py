from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('women/',views.women, name="women"),
    path('men/', views.men, name="men"),
    path('products/',views.products, name="products"),
    path('account/', views.account, name="account"),
    path('register/', views.register, name="register"),
    path('contact/',views.contact, name="contact"),
    path('checkout/', views.checkout, name="checkout"),
    path('single/',views.single, name="single"),
    path('address/',views.address, name="address"),
    path('customerprofile/',views.customer_profile, name="cprofile"),

    path('accountlogout/', views.accountlogout, name="accountlogout"),

    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),

    path("send_otp",views.send_otp,name="send otp"),
    path("verify_otp/",views.verify_otp,name="verify_otp"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="dashboard/password_reset.html"),
         name="reset_password"),
    path('reset_password_send/',
         auth_views.PasswordResetDoneView.as_view(template_name="dashboard/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="dashboard/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="dashboard/password_reset_complete.html"),
         name="password_reset_complete"),
]