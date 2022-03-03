import json
import random
from datetime import datetime
from django.shortcuts import render, redirect
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


def write_news(title, text):
    random.seed(5)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    link = random.randint(1000, 99999)
    new_news_str = '"created": "{}", "text": "{}", "title": "{}", "link": {}'.format(date, text, title, link)
    new_news_str = ' {' + new_news_str + '}]'

    with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as f:
        news_repository = f.read()
        news_repository = news_repository[:-1] + ',' + new_news_str
        with open(settings.NEWS_JSON_PATH, 'w', encoding='utf-8') as w:
            w.write(news_repository)


class AddNews(View):
    template_name = 'postNews.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        write_news(title, text)

        return redirect('/news/')


class ListNews(View):
    template_name = 'newsLinks.html'

    def get(self, request):
        query = request.GET.get('q')
        if query is None:
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
        else:
            with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
                news_repository = json.load(json_file)
                news_link = {}
                for news in news_repository:
                    if query in news["title"]:
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
