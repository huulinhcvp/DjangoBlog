from django.db import models

# Create your models here.
from django.conf import settings
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class OAuthUser(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='User',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    openid = models.CharField(max_length=50)
    nikename = models.CharField(max_length=50, verbose_name='Nickname')
    token = models.CharField(max_length=150, null=True, blank=True)
    picture = models.CharField(max_length=350, blank=True, null=True)
    type = models.CharField(blank=False, null=False, max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    matedata = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField('Created time', default=now)
    last_mod_time = models.DateTimeField('Modified time', default=now)

    def __str__(self):
        return self.nikename

    class Meta:
        verbose_name = 'oauth user'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class OAuthConfig(models.Model):
    TYPE = (
        ('weibo', 'Weibo'),
        ('google', 'Google'),
        ('github', 'GitHub'),
        ('facebook', 'FaceBook'),
        ('qq', 'QQ'),
    )
    type = models.CharField('Type', max_length=10, choices=TYPE, default='a')
    appkey = models.CharField(max_length=200, verbose_name='AppKey')
    appsecret = models.CharField(max_length=200, verbose_name='AppSecret')
    callback_url = models.CharField(
        max_length=200,
        verbose_name='Callback address',
        blank=False,
        default='http://www.baidu.com')
    is_enable = models.BooleanField(
        'Whether to show', default=True, blank=False, null=False)
    created_time = models.DateTimeField('Created time', default=now)
    last_mod_time = models.DateTimeField('Modified time', default=now)

    def clean(self):
        if OAuthConfig.objects.filter(
                type=self.type).exclude(
                id=self.id).count():
            raise ValidationError(_(self.type + 'Already exists'))

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'oauth configuration'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
