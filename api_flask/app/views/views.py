# -*- coding: UTF-8 -*-


from flask import render_template

from . import main


@main.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')
