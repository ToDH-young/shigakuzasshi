# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 19:55:32 2019

@author: owner
"""

from django.conf.urls import url
from django.urls import path
from .views import ShigakuzasshiView_articles
from .views import ShigakuzasshiView_books

urlpatterns = [
        path('', ShigakuzasshiView_articles.as_view(), name='articles'),
        path('books', ShigakuzasshiView_books.as_view(), name="books")
]