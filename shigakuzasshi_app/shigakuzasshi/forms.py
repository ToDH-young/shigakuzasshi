# -*- coding: utf-8 -*-
from django import forms
import datetime

class ShigakuzasshiForm(forms.Form):
    year_list = []
    this_year = datetime.date.today().year + 1
    for i in range(1900, this_year):
        year_pair = tuple([i, i])
        year_list.append(year_pair)
    data1 = year_list
    data2 = [
            ('0018-2478', '史学雑誌'),
            ('0386-9253', '西洋史学'),
            ('0447-9114', '西洋古典学研究'),
            ('0386-8869', '現代史研究'),
            ('0386-9369', '史林')
        ]
    year = forms.MultipleChoiceField(label='year', choices=data1, widget=forms.SelectMultiple(attrs={'size': 5}))
    choice = forms.MultipleChoiceField(label='journal', choices=data2, widget=forms.SelectMultiple(attrs={'size': 6}))

    
