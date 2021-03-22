from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersListView.as_view(), name='users_index'),
    path('login/', views.UsersLoginView.as_view(), name='login'),
    path('logout/', views.UsersLogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.UsersDetailView.as_view(), name='users_detail'),
    path('register/', views.UsersCreateView.as_view(), name='users_register'),
    path('update/<int:pk>/', views.UsersUpdateView.as_view(), name='users_update'),
    path('add_user/', views.add_user_view, name='add_user_from_bot'),

    path('invite_to_register/', views.invite_to_register, name='invite_to_register'),
    path('send_email_to_admin/', views.feedback_view, name='feedback_to_email'),
    path('contact_us/', views.ClaimCreateView.as_view(), name='feedback'),
]
