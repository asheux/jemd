from __future__ import unicode_literals
from .models import Profile, Post, Comment, Account, Member
from django.contrib import admin
from django.db import models as django_models
from pagedown.widgets import AdminPagedownWidget


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile


class PostAdmin(admin.ModelAdmin):
    # Note: this makes pagedown the default editor for ALL text fields
    formfield_overrides = {
        django_models.TextField: {'widget': AdminPagedownWidget },
    }
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'post_date', 'posted_by',
                    'comment_count', 'allow_comments')
    readonly_fields = ('comment_count',)


class CommentAdmin(admin.ModelAdmin):
    # Note: this makes pagedown the default editor for ALL text fields
    formfield_overrides = {
        django_models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ('user_name', 'user_email', 'ip_address', 'post_date')


class AccountAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django_models.TextField: {'widget': AdminPagedownWidget},
    }
    prepopulated_fields = {'slug': ('account_name',)}
    list_display = ('account_name', 'location', 'address', 'account_leader', 'created_date', 'allow_members')


        
class MemberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django_models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = (
            'user',
            'id_number',
            'account_number',
            'region',
            'phone',
            'address',
            'city',
            'nationality',
            'occupation',
            'bank',
            'date_applied',
            'monthly_income'
        )

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Member, MemberAdmin)

