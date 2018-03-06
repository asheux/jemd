from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from pagedown.widgets import PagedownWidget
from simplemathcaptcha.fields import MathCaptchaField
from chama.models import Profile, Comment, Member, Account
from .settings import MAX_LENGTH_TEXTAREA


class SignupForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'size': 150, 'maxlength': 50}))


    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        )


class ChangeProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'image',
        )


class UserCommentForm(forms.ModelForm):
    error_msg = _('Cannot be empty nor only contain spaces. Please fill in the field.')
    bodytext = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Comment
        fields = ["bodytext"]
        if MAX_LENGTH_TEXTAREA is not None:
            widgets = {
                'bodytext': forms.Textarea(attrs={'maxlength': MAX_LENGTH_TEXTAREA})
            }

    def clean_bodytext(self):
        bodytext = self.cleaned_data.get('bodytext')
        if bodytext:
            if not bodytext.strip():
                raise forms.ValidationError(self.error_msg)
        return bodytext


class CommentForm(UserCommentForm):
    user_name = forms.CharField(label=_('Username'), initial=_('anonymous'))
    user_email = forms.EmailField(label=_('E-mail'), required=False)
    captcha = MathCaptchaField(
        required=True, error_messages={'invalid': _('Welcome robot')})

    class Meta:
        model = Comment
        fields = ("user_name", "user_email", "bodytext")
        if MAX_LENGTH_TEXTAREA is not None:
            widgets = {
                'bodytext': forms.Textarea(attrs={'maxlength': MAX_LENGTH_TEXTAREA})
            }

    def clean_user_name(self):
        self.error_msg
        user_name = self.cleaned_data.get('user_name')
        if user_name:
            if not user_name.strip():
                raise forms.ValidationError(self.error_msg)
        return user_name


class UserMemberForm(forms.ModelForm):
    
    class Meta:
        model = Member
        fields = (
            'id_number',
            'account_number',
            'bank', 
            'region', 
            'phone',
            'occupation',
            'address',
            'city',
            'nationality',
            'monthly_income'
        )



class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'account_name',
            'location',
            'address',
            'account_leader',
            'slug',
            'member'
        )