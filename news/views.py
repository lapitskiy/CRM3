from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewsForm
from django.views.generic import ListView

from .models import News, Category

class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

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

# Create your views here.
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            #news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', context = {'form': form})