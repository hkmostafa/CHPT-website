from django.urls import path,re_path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
  

    path('register/', user_views.register, name='register'),
    path('login/', user_views.userlogin, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='forusers/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),

    #USER URLS
    path('appointment/create/', user_views.CreateRdv, name='createrdv'),
    path('appointment/update/<int:id>/', user_views.UpdateRdv, name='updaterdv'),
    path('appointment/delete/<int:id>/', user_views.DeleteRdv, name='deleterdv'),

    path('ajax/load-doctors/', user_views.load_doctors, name='ajax_load_doctors'),

    #ADMIN URLS
    path('administration/appointments/', user_views.admin_app, name='adminapp'),   

    path('administration/users/', user_views.admin_user, name='adminuser'),  
    path('administration/users/createadmin/', user_views.AdminCreateAdmin,name='createadmin'),
    path('administration/users/createdoctor/', user_views.AdminCreateDoctor,name='createdoctor'),
    path('administration/users/update/<int:id>/', user_views.UpdateUser,name='updateuser'),
    path('administration/users/delete/<int:id>/', user_views.AdminDeleteUser,name='deleteuser'),

    path('administration/contacts/', user_views.admin_cont, name='admincont'),    
    path('administration/contacts/delete/<int:id>/', user_views.DeleteContact,name='deletecontact'),

    path('administration/specialities/', user_views.admin_spec, name='adminspec'),  
    path('administration/specialties/create/', user_views.AdminCreateSpecialty,name='createspecialty'),
    path('administration/specialties/update/<int:id>/', user_views.AdminUpdateSpecialty,name='updatespecialty'),
    path('administration/specialties/delete/<int:id>/', user_views.AdminDeleteSpecialty,name='deletespecialty'),
]    
  
    #CONTACT URLS

   