from django.shortcuts import render, redirect
from django.views import View
from django.forms import Form, CharField
from django.http import Http404
from django.conf import settings
from datetime import datetime
import json
import random


class NewsPageView(View):
    def get(self, request, id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as pages_file:
            pages = json.load(pages_file)
            for page in pages:
                if int(page['link']) == id:
                    return render(request, 'news/article.html', context=page)
        raise Http404


class SearchNewsForm(Form):
    q = CharField()


class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', None)
        search_form = SearchNewsForm()
        with open(settings.NEWS_JSON_PATH, 'r') as pages_file:
            pages = json.load(pages_file)
            date_pages = {}
            for page in pages:
                if q is None or q in page['title']:
                    date = page['created'][:10]
                    if date not in date_pages:
                        date_pages[date] = []
                    date_pages[date].append(page)
            date_pages_list = []
            for k, v in date_pages.items():
                date_pages_list.append({'group': k, 'pages': v})
            date_pages_list.sort(key=lambda x: x.get('group'), reverse=True)
            return render(request, 'news/main.html', context={"date_pages": date_pages_list, "search_form": search_form})
        raise Http404


class CreateNewsForm(Form):
    title = CharField()
    text = CharField()


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        news_form = CreateNewsForm()
        return render(request, 'news/create.html', context={'news_form': news_form})

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        text = request.POST['text']
        current_time = datetime.now()
        with open(settings.NEWS_JSON_PATH, 'r') as pages_file:
            pages = json.load(pages_file)
        with open(settings.NEWS_JSON_PATH, 'w') as pages_file:
            pages.append({
                "created": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "text": text,
                "title": title,
                "link": random.randint(1000000, 9999999)
            })
            json.dump(pages, pages_file)
        return redirect('/news/')
