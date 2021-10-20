from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.views.generic import ListView, TemplateView
from plugins.utils import RelatedMixin
from django.contrib.auth.decorators import permission_required


class UserHomeView(RelatedMixin, TemplateView):
    template_name = 'users/users_index.html'
    related_module_name = 'users' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return self.render_to_response(context)


UsersHomeViewPermit = permission_required('users.view', raise_exception=True)(UserHomeView.as_view())


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')
