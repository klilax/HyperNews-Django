import json
import random
from datetime import datetime
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


class AddNews(View):
    template_name = 'postNews.html'

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')




class ListNews(View):
    template_name = 'newsLinks.html'

    def get(self, request):
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
            news_repository = json.load(json_file)
            news_link = {}
            for news in news_repository:
                date = news['created'].split().pop(0)
                time = news['created'].split().pop(1)
                link_str = news["link"]
                link = {"link": link_str, "title": news["title"], "time": time}
                if date in news_link:
                    news_link[date].append(link)
                    news_link[date] = sorted(news_link[date], key=lambda i: i["time"], reverse=True)
                else:
                    news_link[date] = [link]
            sorted_news = dict(sorted(news_link.items()))
            return render(request, self.template_name, {"news_list": sorted_news})
