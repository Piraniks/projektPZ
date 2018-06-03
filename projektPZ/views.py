from django.views.generic import View
from django.shortcuts import render

from projektPZ import status


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


def handler404(request):
    return render(request,
                  status=status.HTTP_404_NOT_FOUND,
                  template_name='http404.html')


def handler403(request):
    return render(request,
                  status=status.HTTP_403_FORBIDDEN,
                  template_name='http403.html')
