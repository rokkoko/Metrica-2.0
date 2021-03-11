from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from users.db_actions import add_user_into_db_simple
import json
from django.core import serializers

URL_PATH = 'https://mysterious-reef-49447.herokuapp.com'


class UsersLoginView(LoginView):
    success_message = '%(username)s was successfully login'
    template_name = 'log_in_out.html'


class UsersLogoutView(LogoutView):
    success_message = '%(username)s was successfully logout'
    template_name = 'log_in_out.html'


class UsersListView(ListView):
    model = CustomUser
    template_name = 'users_index.html'
    context_object_name = 'users_list'

    # OPTIONAL
    # def get_queryset(self):
    #     """
    #     OPTIONAL
    #     Override parent method to get custom queryset by filtering
    #     .objects.all() by named param "pk", which send by url_dispatcher from
    #     <int:pk>-part of url. Dispatcher also can send positional param (args).
    #     In class-based view access to this param from url_dispatcher based on
    #     "self.kwargs" or "self.args"
    #     :return: new filtered queryset
    #     """
    #     queryset = CustomUser.objects.filter(pk=self.kwargs['pk'])
    #     return queryset


class UsersDetailView(DetailView):
    model = CustomUser
    template_name = 'users_detail.html'

    def get_context_data(self, **kwargs):
        """
        OPTIONAL
        Override parent method to get context data for template (add JSON -
        format data about current user)
        :param kwargs: captured named param from url_disptacher path()
        :return: additional context var "json" for template rendering
        """
        context = super().get_context_data(**kwargs)
        context['json'] = serializers.serialize(
            'json',
            CustomUser.objects.filter(pk=self.kwargs['pk']),
            fields=(
                'username',
                'first_name',
                'last_name',
                'Email'
            )
        )
        return context


class UsersCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'user_register.html'


class UsersUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('users:users_index')


def invite_to_register(request):
    """
    DRAFT
    :param request:
    :return:    str()__link for user update IF user already login (useless for REST with tg_bot)
                OR redirect to registration page (form)
    """
    if request.user.id:
        return HttpResponse('https://heroku' + str(reverse_lazy('users:users_update', args=[request.user.id])))
    return HttpResponseRedirect(reverse_lazy('users:users_register'))


# disable csrf protection for testing via Postman by using decorator
# @csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        request_raw = request.body
        request_json = json.loads(request_raw)
        user = request_json['user']
        new_user_pk = add_user_into_db_simple(user)

    if request.method == 'GET':
        user = request.GET.get('user')
        new_user_pk = add_user_into_db_simple(user)

    # Return redirect to update_view for created user (in browser)
    # return HttpResponseRedirect(reverse('users:users_update', args=[new_user_pk]))

    # Return text of link for tg_bot to update user account page
    return HttpResponse(URL_PATH + str(reverse_lazy('users:users_update', args=[new_user_pk])))