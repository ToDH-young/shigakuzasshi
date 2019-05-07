from django.shortcuts import render
from django.http import HttpResponse
from .forms import ShigakuzasshiForm_articles, ShigakuzasshiForm_books
from django.views.generic import TemplateView
from .CiNii import CiNii

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
class ShigakuzasshiView_articles(TemplateView):

    def __init__(self):
        self.params = {
            'title': '文献検索アプリ：論文用',
            'msg': '情報を入力してください',
            'form': ShigakuzasshiForm_articles(),
            'goto': 'books',
            'top': 'articles',
            'output': 'ここに結果が表示されます。',
        }

    def get(self, request):
        return render(request, 'shigakuzasshi/index.html', self.params)

    def post(self, request):
        year = request.POST.getlist('year')
        ch = request.POST.getlist('choice')
        message = '出版年：' + str(year) + '\nISSN：' + str(ch)
        instance = CiNii('articles', ch, year[0], year[0])
        result = instance.search()
        self.params['msg'] = message
        self.params['form'] = ShigakuzasshiForm_articles(request.POST)
<<<<<<< HEAD
        self.params['output'] = result
=======
        self.params['result'] = result
>>>>>>> af67e37bf7b690dc604732e84453cb2fffefb8b5
        return render(request, 'shigakuzasshi/index.html', self.params)


class ShigakuzasshiView_books(TemplateView):

    def __init__(self):
        self.params = {
            'title': '文献検索アプリ:書籍用',
            'msg': '情報を入力してください',
            'form': ShigakuzasshiForm_books(),
            'goto': 'articles',
            'top': 'books',
<<<<<<< HEAD
            'output': 'ここに結果が表示されます。',
=======
            'output': '検索結果'
>>>>>>> af67e37bf7b690dc604732e84453cb2fffefb8b5
        }

    def get(self, request):
        return render(request, 'shigakuzasshi/index.html', self.params)

    def post(self, request):
        year = request.POST.getlist('year')
        ch = request.POST.getlist('choice')
        message = '出版年：' + str(year) + '\npublisher：' + str(ch)
        instance = CiNii('books', ch, year[0], year[0])
        result = instance.search()
        self.params['msg'] = message
        self.params['form'] = ShigakuzasshiForm_books(request.POST)
        self.params['output'] = result
        return render(request, 'shigakuzasshi/index.html', self.params)
