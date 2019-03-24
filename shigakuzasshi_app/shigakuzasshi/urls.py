# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 19:55:32 2019

@author: owner
"""

from django.conf.urls import url
from .views import ShigakuzasshiView

urlpatterns = [
        url(r'', ShigakuzasshiView.as_view(), name='index'),
]