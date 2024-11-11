from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from .forms import CustomUserCreatingForm
from django.urls import reverse_lazy
from django.views import View


def index(request):
    return render(request, 'index.html')


# Регистрация
class Register(generic.CreateView):
    template_name = 'catalog/register.html'
    form_class = CustomUserCreatingForm
    success_url = reverse_lazy('catalog:login')


# Вход
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserLoginForm  # Импортируем форму для входа


class UserLoginView(View):
    template_name = 'catalog/login.html'

    def get(self, request):
        form = UserLoginForm()
        next_page = request.GET.get('next', '')  # Получаем next из GET параметров
        return render(request, self.template_name, {'form': form, 'next': next_page})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.POST.get('next') or reverse_lazy('catalog:home')  # Получаем next из POST данных
                return redirect(next_page)
            else:
                form.add_error(None, 'Неверные учетные данные.')

        return render(request, self.template_name, {'form': form})



@login_required
def profile(request):
    # Получаем текущего пользователя
    user = request.user

    if request.method == 'POST':
        form = CustomUserCreatingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('catalog:profile'))  # Перенаправление на профиль после успешного сохранения
    else:
        form = CustomUserCreatingForm(instance=user)  # Инициализация формы с данными пользователя

    return render(request, 'catalog/profile.html', {'form': form})


