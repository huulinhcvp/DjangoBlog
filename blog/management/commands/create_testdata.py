#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: create_testdata.py
@time: 2017/3/11 上午1:58
"""

from django.core.management.base import BaseCommand
from blog.models import Article, Tag, Category
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'create test datas'

    def handle(self, *args, **options):
        user = get_user_model().objects.get_or_create(
            email='test@test.com', username='Test user', password=make_password('test!q@w#eTYU'))[0]

        pcategory = Category.objects.get_or_create(
            name='I am the parent category', parent_category=None)[0]

        category = Category.objects.get_or_create(
            name='Child category', parent_category=pcategory)[0]

        category.save()
        basetag = Tag()
        basetag.name = "Label"
        basetag.save()
        for i in range(1, 20):
            article = Article.objects.get_or_create(
                category=category,
                title='nice title ' + str(i),
                body='nice content ' + str(i),
                author=user)[0]
            tag = Tag()
            tag.name = "Label" + str(i)
            tag.save()
            article.tags.add(tag)
            article.tags.add(basetag)
            article.save()

        from DjangoBlog.utils import cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS('created test datas \n'))
