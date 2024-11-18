import os
import random
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from users.models import Book_User
from booksapp.models import Books
from .forms import BookForm, UserRegisterForm
from django.contrib.auth import logout



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['book_title']
            author = form.cleaned_data['book_author']

            try:
                book = Books.objects.get(book_title=title, book_author=author)
                Book_User.objects.create(user=request.user, book=book)
                messages.success(request, f'Книга добавлена')
                return redirect('profile')  # Перенаправление на страницу успеха
            except Books.DoesNotExist:
                # Если книга не найдена, можно отобразить сообщение
                messages.error(request, "Книга не найдена. Пожалуйста, введите другую.")
                return render(request, 'users/add_book.html', {'form': form})

            # Проверяем, существует ли книга с таким названием
            #book= Books.objects.get(book_title=title, book_author=author)

            # Создаем запись в таблице UserBook
            #Book_User.objects.create(user=request.user, book=book)

            #return redirect('profile')  # Перенаправление на страницу успеха
    else:
        form = BookForm()
    
    return render(request, 'users/add_book.html', {'form': form})

@login_required
def profile_view(request):
    # Получаем книги, добавленные текущим пользователем
    user_books = Book_User.objects.filter(user_id=request.user.id)
    return render(request, 'users/profile.html', {'books': user_books})

def download_image() -> list[str]:
    #save_dir = r'C:\Users\Alina\Desktop\Books\images'
    save_dir = r'C:\Users\Alina\Desktop\Books\backend\users\static\users\images'
    queryset = Books.objects.raw('SELECT * FROM booksapp_books ORDER BY RANDOM() LIMIT 115')
    queryset = random.sample(list(queryset), 3)
    #предварительно очищаем директорию
    for filename in os.listdir(save_dir):
        file_path = os.path.join(save_dir, filename)
        # Удаляем файл или директорию
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
    # Извлекаем имя файла из URL
    result_dict = {}
    for one_book in queryset:
        filename = os.path.join(save_dir, one_book.image_url_s.split('/')[-1])
        result_dict[one_book.book_title] = filename
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
        # Скачиваем изображение
        response = requests.get(headers=headers, url=one_book.image_url_l)
        print(response.status_code)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Изображение сохранено: {filename}")
        else:
            print(f"Не удалось скачать изображение: {one_book.image_url_s}")
    return queryset, result_dict
    #urls = os.listdir('images')
    #print(urls)
    #return urls

def book_search(request):
    form = BookForm()
    results = []
    titles = []
    images = []
    queryset, result_dict = download_image() 
    for k, v in result_dict.items():
        titles.append(k)
        images.append(v.split('\\')[-1])
    print(images)
    #titles = [one_book.book_title for one_book in queryset]
    #print(titles)
    #images = os.listdir(r'C:\Users\Alina\Desktop\Books\backend\users\static\users\images')
    if request.method == 'POST':
        if 'search' in request.POST:  # Проверяем, была ли нажата кнопка поиска
            form = BookForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                results = Books.objects.filter(book_title__icontains=query)
                form.fields['book'].queryset = results
        elif 'select' in request.POST:  # Проверяем, была ли нажата кнопка выбора книги
            form = BookForm(request.POST)
            selected_book = form.data.get('book') #достаем айди выбранной книги
            #print(selected_book)
            if selected_book:
                # Сохраняем книгу в базу данных пользователя
                # Сохраняем запись в модели User_Book
                Book_User.objects.create(user=request.user, book_id=selected_book)
                return redirect('home-page')  # Перенаправляем на страницу поиска после добавления
    return render(request, 'users/home.html', {'form': form, 'results': results, 'files':images, 'titles':titles})














