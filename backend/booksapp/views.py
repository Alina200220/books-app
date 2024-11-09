from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	"""Представление для главной страницы с формой (возвращает html страницу браузера)"""
	return render(request, 'booksapp/home.html')


