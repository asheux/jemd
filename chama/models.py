from __future__ import unicode_literals
import uuid
import datetime
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.urls import reverse
from .signals import save_comment
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    description = models.TextField(max_length=500, default='', null=True)
    birthdate = models.DateField(blank=True, null=True)
    phone = models.IntegerField(default=0, null=True)
    city = models.CharField(max_length=50, default='', null=True)
    country = models.CharField(max_length=100, default='', blank=True, null=True)
    organization = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='Published')


@python_2_unicode_compatible
class Post(models.Model):
    tags = TaggableManager()
    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.SlugField()
    bodytext = models.TextField(blank=True, verbose_name=_("message"))
    post_date = models.DateTimeField(auto_now_add=True, verbose_name=_("post date"))
    modified = models.DateTimeField(null=True, verbose_name=_("modified"))
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("posted by"),on_delete=models.CASCADE, default=True)
    allow_comments = models.BooleanField(default=True, verbose_name=_("allow comments"))
    comment_count = models.IntegerField(blank=True, default=0, verbose_name=_('comment count'))

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-post_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
            'year': '%04d' % self.post_date.year,
            'month': '%02d' % self.post_date.month,
            'day': '%02d' % self.post_date.day,
        }

        return reverse('chamatu:post_detail', kwargs=kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name=_("post"))
    bodytext = models.TextField(verbose_name=_("message"))
    post_date = models.DateTimeField(auto_now_add=True, verbose_name=_("post date"))
    ip_address = models.GenericIPAddressField(default='0.0.0.0', verbose_name=_("ip address"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_("user"), 
        on_delete=models.CASCADE, related_name='comment_user')
    user_name = models.CharField(max_length=50, default='anonymous', verbose_name=_("user name"))
    user_email = models.EmailField(blank=True, verbose_name=_("user email"))

    def __str__(self):
        return self.bodytext

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['post_date']


post_save.connect(save_comment, sender=Comment)



class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, 
        on_delete=models.CASCADE, related_name='member_user')
    region = models.CharField(max_length=50, verbose_name=_("region"))
    phone = models.IntegerField()
    date_applied = models.DateField(auto_now_add=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    monthly_income = models.BigIntegerField(blank=True, null=True)
    id_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100, default='')


    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')



@python_2_unicode_compatible
class Account(models.Model):
    account_name = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    account_leader = models.ForeignKey(Member, related_name='account_leader', on_delete=models.CASCADE)
    slug = models.SlugField()
    created_date = models.DateField(auto_now_add=True)
    allow_members = models.BooleanField(default=True)
    member = models.ManyToManyField(Member)

    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def get_absolute_url(self):
        return reverse('chamatu:account_detail', kwargs = {'slug': self.slug})  


'''def fabric(names, baseclass=Account):
    for name in names:
        class Meta:
            db_table = '%s_table' % name.lower()
        attrs = {'__module__': baseclass.__module__, 'Meta': Meta}

        attrs.update({'member_name': models.CharField(max_length=100)})
        newclass = type(str(name), (baseclass,), attrs)
        globals()[name] = newclass
fabric(['GroupA', 'GroupB', 'GroupC', 'GroupD'])'''
