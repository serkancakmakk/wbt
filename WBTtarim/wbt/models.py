from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from WBTtarim import settings
# Create your models here.
class Company(models.Model):
    vizion_en = models.CharField(max_length=1000,name='Vizion')
    mission_en = models.CharField(max_length=1000,name='Mission')
    vizyon_tr = models.CharField(max_length=1000,name='Vizyon')
    misyon_tr = models.CharField(max_length=1000,name='Misyon')

    phone = models.IntegerField(name='Telefon')
    mail = models.EmailField(max_length=20,name='Email')
    location = models.CharField(max_length=30,name='Adres')
    google_iframe = models.CharField(max_length=1500,name="google_maps")
    yeni_mesaj = models.IntegerField(default=0)
class Services(models.Model):
    servis_adi_tr = models.CharField(null=True,blank=True,max_length=20)
    service_name_en = models.CharField(null=True,blank=True,max_length=20)
    bilgi_tr = models.TextField(null=True,blank=True,max_length=255)
    info_en = models.TextField(null=True,blank=True,max_length=255)
    image = models.ImageField(null=True,blank=True)
class Log(models.Model):
    hareket = models.CharField(null=False, blank=False,max_length=255)
    kullanici = models.CharField(max_length=255,null=True,blank=True)
    tarih = models.DateTimeField(auto_now_add=True)  # Otomatik olarak oluşturulma tarihi
    kullandigi_view = models.CharField(null=True,blank=True,max_length=255)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    silindi = models.BooleanField(default=False)
    def __str__(self):
        return self.hareket
class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery_images/')

class Certificates(models.Model):
    image = models.ImageField(upload_to='certificates')
    name = models.CharField(max_length=10)
    document = models.ImageField(upload_to='certificate_doc',null=True,blank=True,)
class wbtUser(AbstractUser):
    yetkiler = models.ManyToManyField(Permission)
    # Diğer kullanıcı özel alanlarınızı burada tanımlayabilirsiniz

    # def __str__(self):
    #     yetki_listesi = ', '.join(self.yetkiler.values_list('yetki_adi', flat=True))
    #     return f"{self.username} - Yetkiler: {yetki_listesi}"
class Message(models.Model):
    mesaj = models.CharField(max_length=255)
    konu = models.CharField(max_length=20)
    email = models.EmailField()
    telefon = models.IntegerField()
    DURUM_CHOICES = [
        ("Okundu", "Okundu"),
        ("Geçersiz", "Geçersiz"),
        ("Beklemede", "Beklemede"),
        ("Ulaşılamadı", "Ulaşılamadı"),
        ("Okunmadı", "Okunmadı"),
        ("Silindi","Silindi"),
    ]
    durum = models.CharField(
        max_length=11,
        choices=DURUM_CHOICES,
        default='Okunmadı',
    )
    def __str__(self):
        return self.konu
