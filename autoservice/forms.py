from django import forms
from autoservice import models
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='Почта')
    last_name = forms.CharField(required=True,
                                label='Фамилия')
    first_name = forms.CharField(required=True,
                                 label='Имя')
    password = forms.CharField(widget=forms.PasswordInput,
                               min_length=6,
                               required=True,
                               label='пароль')
    password1 = forms.CharField(widget=forms.PasswordInput,
                                required=True,
                                label='Повторите пароль')
    lang = forms.ModelChoiceField(widget=forms.Select,
                             label='Язык',
                             required=True,
                             queryset=models.Language.objects.all(),)

class LoginForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='Почта')
    password = forms.CharField(widget=forms.PasswordInput,
                               min_length=6,
                               required=True,
                               label='пароль')
class CarFormForUser(forms.Form):
    name = forms.CharField(required=True,
                                label='Название машины')
    year = forms.IntegerField(required=True,
                              label='Год выпуска')

class UserDataForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email','first_name','last_name']

    def get_data(self):
        self.fields['email'].label = 'email'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

class ChangeLang(forms.ModelForm):
    class Meta:
        model = models.AS_user
        fields = ['lang']

    def get_data(self):
        self.fields['lang'].label = 'Язык'










