import json
from django.shortcuts import render
from django.conf import settings
from django.http.response import HttpResponse
from django.views import View


class Welcome(View):

    def get(self, request):
        return HttpResponse('Coming Soon')


class ServeNews(View):
    template_name = 'news.html'

    def get(self, request, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
            news_repository = json.load(json_file)
            link = kwargs['link']

            render_news = {}
            for news in news_repository:
                if news['link'] == int(link):
                    render_news = news
                    break
            return render(request, self.template_name, {'news': render_news})
