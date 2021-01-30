from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import News, Category

# Create your views here.
def index(request):
    #print(request)
    news = News.objects.order_by('-created_at')
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    return render(request,'news/index.html',context = context)

# Create your views here.
def get_category(request,category_id):
    #print(request)
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {
        'news': news,
        'category': category,
    }
    return render(request,'news/category.html',context = context)

# Create your views here.
def view_news(request,news_id):
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'news_item': news_item,
    }
    return render(request,'news/view_news.html',context = context)
