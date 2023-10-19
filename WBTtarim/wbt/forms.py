from django import forms

from .models import Certificates, Company, Gallery, Message,Services, wbtUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CompanyForm(forms.ModelForm):
    Vizyon = forms.CharField(widget=forms.Textarea)
    Misyon = forms.CharField(widget=forms.Textarea)
    Vizion = forms.CharField(widget=forms.Textarea)
    Mission = forms.CharField(widget=forms.Textarea)
    google_maps = forms.CharField(label='google_iframe')
    class Meta:
        model = Company
        fields = ['Vizion', 'Mission', 'Vizyon', 'Misyon', 'Telefon', 'Email', 'Adres','google_maps']
        labels = {
            'Vizion': 'Vision',
            'Mission': 'Mission',
            'Vizyon': 'Vizyon',
            'Misyon': 'Misyon',
            'Telefon': 'Phone',
            'Email': 'Email',
            'Adres': 'Address'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['Vizyon'].initial = instance.Vizyon
            self.fields['Misyon'].initial = instance.Misyon
            self.fields['Vizion'].initial = instance.Vizion
            self.fields['Mission'].initial = instance.Mission
class wbtUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = wbtUser
        fields = ['username', 'password1', 'password2', 'email', 'yetkiler']
class ServicesForm(forms.ModelForm):
    servis_adi_tr = forms.CharField(required=True, label='Servis Adı (Türkçe)')
    bilgi_tr = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True, label='Bilgi (Türkçe)')
    service_name_en = forms.CharField(required=True, label='Service Name (English)')
    info_en = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True, label='Info (English)')
    image = forms.ImageField(required=True, label='Image')
   

    class Meta:
        model = Services
        fields = ['service_name_en', 'servis_adi_tr', 'bilgi_tr', 'info_en', 'image']
        widgets = {
            'bilgi_tr': forms.Textarea(attrs={'rows': 5}),
        }
class ServicesUpdateForm(forms.ModelForm):
    servis_adi_tr = forms.CharField(required=True, label='Servis Adı (Türkçe)')
    bilgi_tr = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True, label='Bilgi (Türkçe)')
    service_name_en = forms.CharField(required=True, label='Service Name (English)')
    info_en = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True, label='Info (English)')
    image = forms.ImageField(required=True, label='Image')
   

    class Meta:
        model = Services
        fields = ['service_name_en', 'servis_adi_tr', 'bilgi_tr', 'info_en', 'image']
        widgets = {
            'bilgi_tr': forms.Textarea(attrs={'rows': 5}),
        }
class CertificatesForm(forms.ModelForm):
    class Meta:
        model = Certificates
        image = forms.ImageField(required=True, label='Image')
        fields = ['name', 'image','document']  # Kullanmak istediğiniz alanları buraya ekleyin
# AUTHENTİCATİON
from django.contrib.auth.models import User
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # E-posta alanını ekleyin (isteğe bağlı)

    class Meta:
        model = wbtUser
        fields = ['username', 'email', 'password1', 'password2']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
from django import forms

from django import forms

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']
class GalleryUpdateForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']
class UpdateCertificatesForm(forms.ModelForm):
    class Meta:
        model = Certificates
        image = forms.ImageField(required=True, label='Image')
        fields = ['name', 'image','document']  # Kullanmak istediğiniz alanları buraya ekleyin
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['mesaj', 'konu','email','telefon']  # Kullanmak istediğiniz alanları buraya ekleyin