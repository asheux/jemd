from .forms import SignupForm, ChangeProfile, ImageUploadForm, CommentForm, UserCommentForm, UserMemberForm
from django.shortcuts import render, redirect
from .models import Profile, Post, Comment, Account, Member
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.sites.models import Site
from django.views.generic.dates import DateDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic import View
from el_pagination.views import AjaxListView
from django.contrib.syndication.views import Feed


def index(request):
    return render(request, 'chama/index.html')


def projects(request):
    return render(request, 'chama/projects.html')


def about(request):
    return render(request, 'chama/about.html')


def progress(request):
    return render(request, 'chama/progress.html')


def login(request):
    return render(request, 'chama/login.html')



class SignupFormView(View):
    form_class = SignupForm
    template_name = 'chama/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('chamatu:index')

        return render(request, self.template_name, {'form': form})


def view_profile(request):
    if request.method == 'POST':
        profile_pic = ImageUploadForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_pic.is_valid():
            profile_pic.save()

            messages.success(request, 'Image uploaded successfully!')
            return redirect(reverse('chamatu:view_profile'))

    else:
        profile_pic = ImageUploadForm(instance=request.user.profile)
    args = {
        'user': request.user,
        'profile_pic': profile_pic
    }
    return render(request, 'chama/profile.html', args)


def edit_profile(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    form = ChangeProfile(instance=request.user)

    profile_inline_formset = inlineformset_factory(
        User,
        Profile,
        fields=(
            'description',
            'birthdate',
            'phone',
            'city',
            'country',
            'organization'
        )
    )
    
    profile_form = profile_inline_formset(instance=request.user)

    if request.user.is_authenticated and request.user.pk == user.pk:
        if request.method == 'POST':
            form = ChangeProfile(request.POST, instance=request.user)
            profile_form = profile_inline_formset(request.POST, request.FILES)

            if form.is_valid():
                created_user = form.save(commit=True)
                profile_form = profile_inline_formset(request.POST, request.FILES, instance=created_user)

                if profile_form.is_valid():
                    created_user.save()
                    profile_form.save()

                    messages.success(request, 'Your profile was updated successfully!')
                    return redirect(reverse('chamatu:edit_profile'))

                else:
                    messages.warning(request, "Please correct the error highlighted below:")
                    return redirect(reverse('chamatu:edit_profile'))

        args = {
            'pk': pk,
            'form': form,
            'profile_form': profile_form
        }

        return render(request, 'chama/change_profile.html', args)
        
    else:
        raise PermissionDenied


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was change successfully!')
            return redirect(reverse('chamatu:change_password'))
        else:
            messages.warning(request, 'Please check that you have provided the correct password')
            return redirect(reverse('chamatu:change_password'))

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'chama/change_password.html', args)


'''class LatestEntriesFeed(Feed):
    title = "%s entries" % (Site.objects.get_current())
    description = "The latest entries"
    link = "/chama/"

    def items(self):
        return Post.objects.order_by('-post_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.bodytext'''


class PostListView(AjaxListView):
    context_object_name = "posts"
    queryset = Post.objects.all().select_related()


class AccountListView(generic.ListView):
    template_name = 'chama/account_list.html'
    context_object_name = "accounts"

    def get_queryset(self):
        return Account.objects.all()


class AccountDetail(generic.DetailView):
    model = Account
    page_template = "chama/account_detail.html"

    def get_queryset(self):
        queryset = super(AccountDetail, self).get_queryset()
        return queryset.select_related()

    def post(self, request, *args, **kwargs):
        self.request = request
        self.object = post = self.get_object()

        member_form = UserMemberForm(request.POST)
        if member_form.is_valid():
            member = member_form.save(commit=False)
            member.post = post
            member.user = request.user
            member.user_name = request.user
            member.user_email = request.user.email
            member.save()
            messages.success(request, 'Application was submitted successfully! Thank you for applying')
            return redirect(post.get_absolute_url())

        context = self.get_context_data(object=post)
        context['member_form'] = member_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            form = UserMemberForm()
        else:
            return None
        context = {
            'page_template': self.page_template,
            'member_form': form,
            'members': Member.objects.filter(account=self.object.id).select_related()
        }
        return super(AccountDetail, self).get_context_data(**context)

    def render_to_response(self, context, **response_kwargs):

        if self.request.is_ajax():
            template = self.page_template
        else:
            template = self.get_template_names()
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )

class AccountCreate(CreateView):
    model = Account
    fields = ['account_name']


class AccountUpdate(UpdateView):
    model = Account
    fields = ['account_name']


class AccountDelete(DeleteView):
    model = Account
    success_url =reverse_lazy('chamatu:index')


class PostDetailView(DateDetailView):
    model = Post
    date_field = 'post_date'
    month_format = '%m'
    page_template = "chama/post_detail.html"

    def get_queryset(self):
        queryset = super(PostDetailView, self).get_queryset()
        return queryset.select_related()

    def post(self, request, *args, **kwargs):
        self.request = request
        self.object = post = self.get_object()
        if request.user.is_authenticated:
            comment_form = UserCommentForm(request.POST)
        else:
            return None
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
                comment.user_name = request.user
                comment.user_email = request.user.email
            comment.ip = '0.0.0.0'
            comment.save()
            return redirect(post.get_absolute_url())
        context = self.get_context_data(object=post)
        context['comment_form'] = comment_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            form = UserCommentForm()
        else:
            return None
        context = {
            'page_template': self.page_template,
            'comment_form': form,
            'comments': Comment.objects.filter(post=self.object.id).select_related()
        }
        return super(PostDetailView, self).get_context_data(**context)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template depending if the request is ajax
        or not and it renders with the given context.
        """
        if self.request.is_ajax():
            template = self.page_template
        else:
            template = self.get_template_names()
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )


def borrow_loan(request):
    return render(request, 'chama/borrow_loan.html')


def payments(request):
    return render(request, 'chama/payments.html')



















