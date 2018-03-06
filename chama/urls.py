from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = "chama"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^projects/$', views.projects, name='projects'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^progress/$', views.progress, name='progress'),
    re_path(r'^login/$', auth_views.login, {'template_name': 'chama/login.html'}, name='login'),
    re_path(r'^logout/$', auth_views.logout, {'next_page': 'site'}, name='logout'),
    re_path(r'^signup/$', views.SignupFormView.as_view(), name='signup'),
    # url(r'^signup/success/$', views.signup_success, name='signup_success'),
    re_path(r'^profile/$', views.view_profile, name='view_profile'),
    re_path(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'^profile/password', views.change_password, name='change_password'),
    re_path(r'^change-password/$', views.change_password, name='change_password'),
    re_path(r'^savings/$', views.AccountListView.as_view(), name='savings'),
    re_path(r'^savings/(?P<slug>[-_\w]+)/$', views.AccountDetail.as_view(), name='account_detail'),
    re_path(r'^account/add/$', views.AccountCreate.as_view(), name='account_add'),
    re_path(r'^account/(?P<slug>[-_\w]+)/$', views.AccountUpdate.as_view(), name='account_update'),
    re_path(r'^account/(?P<slug>[-_\w]+)/delete/$', views.AccountDelete.as_view(), name='account_delete'),
    re_path(r'^loans/$', views.borrow_loan, name='borrow_loan'),
    re_path(r'^payments/$', views.payments, name='payments'),
    re_path(r'^reset-password/$', auth_views.password_reset, {
        'template_name': 'chama/reset_password.html',
        'post_reset_redirect': 'chamatu:password_reset_done',
        'email_template_name': 'chama/reset_password_email.html'}, name='password_reset'),

    re_path(r'^reset-password/done/$', auth_views.password_reset_done, {
        'template_name': 'chama/reset_password_done.html'}, name='password_reset_done'),

    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {
        'template_name': 'chama/reset_password_confirm.html',
        'post_reset_redirect': 'chamatu:password_reset_complete'}, name='password_reset_confirm'
        ),

    re_path(r'^reset-password/complete/$', auth_views.password_reset_complete, {
        'template_name': 'chama/reset_password_complete.html'}, name='password_reset_complete'),
    # re_path(r'^latest/feed/$', views.LatestEntriesFeed()),
    re_path(r'^post-lists/$', views.PostListView.as_view(), name='post_list_view'),
    re_path(r'^post-lists/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-_\w]+)/$',
        views.PostDetailView.as_view(),
        name='post_detail',
        ),
]