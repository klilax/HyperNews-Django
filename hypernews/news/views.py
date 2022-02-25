from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View


class Welcome(View):

    def get(self, request):
        return HttpResponse('Coming Soon')
