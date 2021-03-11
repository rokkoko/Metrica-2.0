from django.urls import path
from .views import UsersListView, UsersCreateView, invite_to_register, UsersDetailView, UsersUpdateView, UsersLoginView, UsersLogoutView, add_user_view

app_name = 'users'

urlpatterns = [
    path('', UsersListView.as_view(), name='users_index'),
    path('login/', UsersLoginView.as_view(), name='login'),
    path('logout/', UsersLogoutView.as_view(), name='logout'),
    path('<int:pk>/', UsersDetailView.as_view(), name='users_detail'),
    path('register/', UsersCreateView.as_view(), name='users_register'),
    path('update/<int:pk>/', UsersUpdateView.as_view(), name='users_update'),
    path('invite_to_register/', invite_to_register, name='invite_to_register'),
    path('add_user/', add_user_view, name='add_user_from_bot'),
]