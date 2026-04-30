from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Страница профиля пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def user_list(request):
    """Список всех пользователей (для соцсети)"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_detail(request, pk):
    """Страница другого пользователя"""
    other_user = get_object_or_404(User, pk=pk)
    
    # Проверка: можно ли смотреть страницу
    if not request.user.is_friend(other_user) and request.user != other_user:
        messages.error(request, 'Вы можете просматривать только страницы своих друзей!')
        return redirect('user_list')
    
    return render(request, 'users/user_detail.html', {'viewed_user': other_user})


@login_required
def add_friend(request, pk):
    """Добавление в друзья"""
    friend = get_object_or_404(User, pk=pk)
    if request.user.add_friend(friend):
        messages.success(request, f'{friend.username} добавлен в друзья!')
    else:
        messages.warning(request, 'Не удалось добавить в друзья')
    return redirect('user_detail', pk=pk)


@login_required
def remove_friend(request, pk):
    """Удаление из друзей"""
    friend = get_object_or_404(User, pk=pk)
    if request.user.remove_friend(friend):
        messages.success(request, f'{friend.username} удален из друзей!')
    return redirect('user_detail', pk=pk)