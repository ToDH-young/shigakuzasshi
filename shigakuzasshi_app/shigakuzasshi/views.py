from django.shortcuts import render
from django.http import HttpResponse
from .forms import ShigakuzasshiForm
from django.views.generic import TemplateView

'''
def index(request):
    if 'year' in request.GET:
        year = request.GET['year']
        result = 'you typed: "' + year + '".'
    else:
        params = {
                'title':'文献検索アプリ',
                'msg':'情報を入力してください',
                'form': ShigakuzasshiForm()
            }
        if (request.method == 'POST'):
            params['msg'] = '出版年：' + request.POST['year'] + '\n' + '雑誌名：' + request.POST['journal']
            params['form'] = ShigakuzasshiForm(request.POST)
        result = render(request, 'shigakuzasshi/index.html', params)
    return HttpResponse(result)
'''

# Create your views here.
class ShigakuzasshiView(TemplateView):
    
    def __init__(self):
        self.params = {
                'title':'文献検索アプリ',
                'msg':'情報を入力してください',
                'form': ShigakuzasshiForm()
            }
    
    def get(self, request):
        return render(request, 'shigakuzasshi/index.html', self.params)
    
    def post(self, request):
        year = request.POST.getlist('year')
        ch = request.POST.getlist('choice')
        message = '出版年：' + str(year) + '\nISSN：' + str(ch)
        self.params['msg'] = message
        self.params['form'] = ShigakuzasshiForm(request.POST)
        return render(request, 'shigakuzasshi/index.html', self.params)
    