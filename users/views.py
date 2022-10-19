from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.views.generic import ListView, TemplateView, DetailView
from plugins.utils import RelatedMixin
from django.contrib.auth.models import User

#from django.views.decorators.csrf import csrf_protect
#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.mixins import LoginRequiredMixin

class UserHomeView(LoginRequiredMixin, RelatedMixin, ListView):
    model = User
    template_name = 'users/users_index.html'
    paginate_by = 10
    context_object_name = 'user'
    related_module_name = 'users' #relatedmixin module

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все пользователи'
        print('user context: ', context)
        return context

#UsersHomeViewPermit = permission_required('users.view', raise_exception=True)(UserHomeView.as_view())


class UsersSettingsView(RelatedMixin, TemplateView):
    template_name = 'users/users_settingsPrev.html'
    related_module_name = 'users' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Настройки'
        return self.render_to_response(context)


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
            return redirect('news_home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')
