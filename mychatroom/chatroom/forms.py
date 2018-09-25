from django import forms

class UserForm(forms.Form):
    phone = forms.CharField(label="手机号", max_length=11, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=128, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    gender = (('male', "男"), ('female', "女"),)

    username = forms.CharField(label="用户名称", max_length=64, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="用户密码", max_length=128, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=128, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号", max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    verification_code = forms.CharField(label="短信验证", max_length=6, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", 
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='用户性别', choices=gender)