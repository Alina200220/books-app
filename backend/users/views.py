import os
import random
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .infer import get_result_user, load_decoder, load_encoder, load_model
from users.models import Book_User
from booksapp.models import Books
from .forms import BookCreationForm, BookForm, UserRegisterForm
from django.contrib.auth import logout
from django.templatetags.static import static



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
def get_recommendations(request) -> list[str]: #возвращает isbn рекоммендованных книг
    obj = Book_User.objects.filter(user=request.user)
    books = []
    for one_book in obj:
        book = Books.objects.filter(id=one_book.book_id)[0]
        books.append(book.isbn)
    data_for_model = {"user":obj[0].user_id, "books":books}
    #функция модели
    encoder = load_encoder(r'C:\Users\Alina\Desktop\Books\backend\users\encoder.pkl')
    decoder = load_decoder(r'C:\Users\Alina\Desktop\Books\backend\users\decoder.pkl')
    items = load_model(r"C:\Users\Alina\Desktop\Books\backend\users\items.pkl")
    result_ids = get_result_user(data_for_model["books"], items, encoder, decoder=decoder)
    return result_ids
    

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
    else:
        form = BookForm()
    
    return render(request, 'users/add_book.html', {'form': form})

@login_required
def profile_view(request):
    # Получаем книги, добавленные текущим пользователем
    user_books = Book_User.objects.filter(user_id=request.user.id)
    return render(request, 'users/profile.html', {'books': user_books})

def download_image() -> list[str]:
    save_dir = r'.\users\static\users\images'
    isbns = ['0316769487', '0446612545','0449001954', '0451524934', '844507119X', '0399528504', '193075437X', '0618345841','0812576454', '0060195509']
    #queryset = Books.objects.raw('SELECT * FROM booksapp_books LIMIT 20')
    #queryset = random.sample(list(queryset), 3)
    queryset = []
    for one_isbn in isbns:
        queryset.append(Books.objects.filter(isbn=one_isbn)[0])
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
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
    return queryset, result_dict

def download_image_recommendation(book_isbns:list[str]) -> dict:
    save_dir = r'.\users\static\users\images'
    # Извлекаем имя файла из URL
    result_dict = {}
    for one_book in book_isbns:
        one_book = Books.objects.filter(isbn=one_book)
        filename = os.path.join(save_dir, one_book[0].image_url_s.split('/')[-1])
        result_dict[one_book[0].book_title] = filename
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
        # Скачиваем изображение
        response = requests.get(headers=headers, url=one_book[0].image_url_l)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
    return result_dict

def book_search(request):
    form = BookForm()
    titles = []
    images = []
    titles_recomm = []
    images_recomm = []
    queryset, result_dict = download_image() 
    for k, v in result_dict.items():
        titles.append(k)
        images.append(v.split('\\')[-1])
    books = Books.objects.all()
    form = BookForm(request.POST)
    list_books_isbns = get_recommendations(request)
    #print(list_books_isbns)
    result_dict_recomm = download_image_recommendation(list_books_isbns)
    for k, v in result_dict_recomm.items():
        titles_recomm.append(k)
        images_recomm.append(v.split('\\')[-1])
    if request.method == 'POST':
        if form.is_valid():
            selected_book_title = form.data.get('book') #достаем айди выбранной книги
            print(selected_book_title)
            if selected_book_title:
                matched_books = Books.objects.filter(book_title__istartswith=selected_book_title)
                print(matched_books)
                # Сохраняем книгу в базу данных пользователя
                # Сохраняем запись в модели User_Book
                Book_User.objects.create(user=request.user, book_id=matched_books[0].id)
                return redirect('home-page')  # Перенаправляем на страницу поиска после добавления
        else:
            print("form is invalid")
    return render(request, 'users/home.html', {'form': form,  'files':images, 'titles':titles, 'files_recomm':images_recomm, 'titles_recomm':titles_recomm, 'books':books})


def home(request):
    books = Books.objects.all()
    return render(request, 'users/home.html', {'books': books})
















