from django.contrib.auth.decorators import permission_required, login_required
from django.utils.translation import activate
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from .forms import (
    CompanyForm, GalleryForm, MessageForm, ServicesForm,
    ServicesUpdateForm, UpdateCertificatesForm, UserRegisterForm,
    CertificatesForm
)
from .models import (
    Company, Gallery, Log, Message, wbtUser, Certificates
)
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import AuthenticationForm
import os
from .models import Company, Gallery, Log, Message, wbtUser, Services, Certificates

from django.conf import settings
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def anasayfa(request, lang=None):
    servis_sayisi = Services.objects.all().count()
    mesaj_sayisi = Message.objects.all().count()
    context = {
        'servis_sayisi':servis_sayisi,
        'mesaj_sayisi':mesaj_sayisi,
    }
    print(servis_sayisi)
    lang == 'tr'
    # Eğer dil belirtilmemişse veya dil "tr" ise
    if lang is None or lang == 'tr':
        # Dil seçeneğini Türkçe olarak session'a kaydedin
        request.session['lang_code'] = 'tr'
        # Eğer zaten "tr" dilindeyseniz, tekrar anasayfaya yönlendirmeyin, direkt içeriği gösterin
        if request.session.get('lang_code') == 'tr':
            return render(request, 'home.html',context)
        else:
            # Türkçe ana sayfaya yönlendirin
            return redirect('anasayfa', lang='tr')
    else:
        # Dil seçeneğini İngilizce olarak session'a kaydedin
        request.session['lang_code'] = 'en'
        # İngilizce ana sayfaya yönlendirin
        return redirect('home', lang='en')

def home(request, lang=None):
    mesaj_sayisi = Message.objects.all().count()
    servis_sayisi = Services.objects.all().count()
    context = {
        'servis_sayisi':servis_sayisi,
        'mesaj_sayisi':mesaj_sayisi,
    }
    # Eğer dil belirtilmemişse veya dil "en" ise
    if lang is None or lang == 'en':
        # Dil seçeneğini İngilizce olarak session'a kaydedin
        request.session['lang_code'] = 'en'
        # Eğer zaten "en" dilindeyseniz, tekrar ana sayfaya yönlendirmeyin, direkt içeriği gösterin
        if request.session.get('lang_code') == 'en':
            return render(request, 'home.html',context)
        else:
            # İngilizce ana sayfaya yönlendirin
            return redirect('home', lang='en',)
    else:
        # Dil seçeneğini Türkçe olarak session'a kaydedin
        request.session['lang_code'] = 'tr'
        # Türkçe ana sayfaya yönlendirin
        return redirect('anasayfa', lang='tr')


def hakkimizda(request, lang):
    companies = Company.objects.all()
    context = {
        
        'companies': companies
    }

    if lang == 'tr':
        # Türkçe içerikleri burada döndürün
        request.session['lang_code'] = 'tr'
        return render(request, 'about.html', context)
    elif lang == 'en':
        # İngilizce içerikleri burada döndürün (şu anda sadece Türkçe içerik varsa Türkçe sayfaya yönlendir)
        return redirect('hakkimizda', lang='tr')
    else:
        # Hatalı dil kodu için 404 hatası döndürün veya dil kodunu Türkçe olarak ayarlayın
        request.session['lang_code'] = 'tr'  # Varsayılan olarak Türkçe olarak ayarlandı
        return redirect('hakkimizda', lang='tr')
def about(request, lang):
    companies = Company.objects.all()
    context = {
        'companies': companies
    }
    if lang == 'en':
        # İngilizce içerikleri burada döndürün
        request.session['lang_code'] = 'en'
        return render(request, 'about.html',context)
    if lang == 'tr':
        # Türkçe içerikleri burada döndürün
        request.session['lang_code'] = 'tr'
        return redirect('hakkimizda', lang='tr')
    else:
        # Hatalı dil kodu için 404 hatası döndürün veya dil kodunu İngilizce olarak ayarlayın
        request.session['lang_code'] = 'en'  # Varsayılan olarak İngilizce olarak ayarlandı
        return redirect('about', lang='en')
def hizmetlerimiz(request, lang):
    servisler = Services.objects.all()
    if lang == 'tr':
        # İngilizce içerikleri burada döndürün
        request.session['lang_code'] = 'tr'
        context = {
            'servisler':servisler
        }
        return render(request, 'services.html',context)
    if lang == 'en':
        # Türkçe içerikleri burada döndürün
        request.session['lang_code'] = 'en'
        return redirect('services', lang='en')
    else:
        # Hatalı dil kodu için 404 hatası döndürün veya dil kodunu İngilizce olarak ayarlayın
        request.session['lang_code'] = 'tr'  # Varsayılan olarak İngilizce olarak ayarlandı
        
        return redirect('hizmetlerimiz', lang='tr')
def services(request, lang):
    services = Services.objects.all()
    if lang == 'en':
        # İngilizce içerikleri burada döndürün
        request.session['lang_code'] = 'en'
        context = {
            'services':services
        }
        return render(request, 'services.html',context)
    if lang == 'tr':
        # Türkçe içerikleri burada döndürün
        request.session['lang_code'] = 'tr'
        return redirect('hizmetlerimiz', lang='tr')
    else:
        # Hatalı dil kodu için 404 hatası döndürün veya dil kodunu İngilizce olarak ayarlayın
        request.session['lang_code'] = 'en'  # Varsayılan olarak İngilizce olarak ayarlandı
        return redirect('services', lang='en')
def servis_detay(request, lang, id):
    servis = get_object_or_404(Services, id=id)
    
    if lang == 'tr':
        request.session['lang_code'] = 'tr'
        context = {
            'servis': servis
        }
    else:
        return redirect('servis_detay', lang='tr', id=id)
        
    return render(request, 'service_detail.html', context)

def service_detail(request, lang, id):
    servis = get_object_or_404(Services, id=id)
    
    if lang == 'en':
        request.session['lang_code'] = 'en'
        context = {
            'servis': servis
        }
    else:
        return redirect('service_detail', lang='en', id=id)
        
    return render(request, 'service_detail.html', context)


def set_language(request, lang):
    if lang in ['tr', 'en']:
        request.session['lang_code'] = lang  # Dil seçeneğini session'a kaydet
        activate(lang)  # Dil seçeneğini aktifleştir

    # Ana sayfaya yönlendirirken 'lang' parametresini de gönderin
    return redirect('home', lang=request.session['lang_code'])
def iletisim(request,lang):
    companies = Company.objects.all()
    print(Company.objects.all())
#     # iframe_code = '<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d25529.250022225202!2d30.70286435!3d36.8866101!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1str!2str!4v1691478891334!5m2!1str!2str" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'

# # iframe içindeki src bağlantısını çıkartma
#     src_start = iframe_code.find('src="') + 5
#     src_end = iframe_code.find('"', src_start)
#     src_link = iframe_code[src_start:src_end]

#     # Çıkartılan src bağlantısını görüntüleme
#     print(src_link)
    context = {
        'companies': companies
    }
    if lang == 'tr':
        request.session['lang_code'] = 'tr'
        return render(request,'contact.html',context)
    elif lang =='en':
        request.session['lang_code'] = 'en'
        return redirect('contact',lang='en')
    else:
        return render(request,'contact.html',lang='tr')
def contact(request,lang):
    companies = Company.objects.all()
    print(companies)
    context = {
        'companies': companies
    }
    if lang == 'en':
        request.session['lang_code'] = 'en'
        return render(request,'contact.html',context)
    elif lang =='tr':
        request.session['lang_code'] = 'tr'
        return redirect('iletisim',lang='tr')
    else:

        return render(request,'contact.html',lang='en')
def gallery(request,lang):
    gallery_items = Gallery.objects.all()
    context = {
        'gallery_items':gallery_items
    }
    if lang == 'en':
        return render(request,'gallery.html',context)
    elif lang =='tr':
        request.session['lang_code'] = 'tr'
        return redirect('galeri',lang='tr')
    else:
        request.session['lang_code'] = 'en'
        return render(request,'gallery.html',context)
def galeri(request,lang):
    gallery_items = Gallery.objects.all()
    context = {
        'gallery_items':gallery_items
    }
    if lang == 'tr':
        return render(request,'gallery.html',context)
    elif lang =='en':
        request.session['lang_code'] = 'en'
        return redirect('gallery',lang='en')
    else:
        request.session['lang_code'] = 'tr'
        return render(request,'gallery.html',context)

def add_service(request):
    if request.method == 'POST':
        form = ServicesForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()

            # Servis eklenirken log kaydı oluştur
            user = request.user
            if user.is_authenticated:

                messages.success(request, 'İşlem başarıyla gerçekleştirildi.')
            return redirect('add_services')
        else:
            messages.error(request, 'İşlem gerçekleştirilemedi, tekrar deneyiniz.')
    else:
        form = ServicesForm()

    services = Services.objects.all()
    context = {
        'services': services,
        'form': form,
    }
    
    return render(request, 'admin_area/add_services.html', context)


# AUTH

def register(request):
    import uuid
   
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Form verileri geçerli ise, yeni kullanıcıyı oluşturup kaydedelim
            new_user = form.save()
            return redirect('login')  # Başka bir sayfaya yönlendirilebilirsiniz
        else:
            print(form.errors)  # Hataları konsola yazdırın
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'admin_area/register.html', context)


def login_view(request):
    user = request.user
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # messages.success(request, 'Giriş başarılı.')
                # Log.objects.create(hareket=f"{user.username} kullanıcısı giriş yaptı.", user=user, kullanici=user.username, kullandigi_view='login' '-' 'giriş')
                return redirect('home' ,lang='en')
                # if user.yetkiler.filter(codename='super_kullanici').exists():
                #     print(user.yetkiler.all())
                #     # Kullanıcının "admin" yetkisi varsa çıkış yap ve ana sayfaya yönlendir
                #     return redirect('dashboard')
                # else:
                #     # Kullanıcının "admin" yetkisi yoksa diğer sayfaya yönlendir
                #     Log.objects.create(hareket=f"{user.username} yetkisi olmadığı halde giriş yapmaya çalıştı sistem tarafından engellendi.", user=user, kullanici=user.username, kullandigi_view='login' '-' 'giriş')
                #     return redirect('home')
                
            else:
                messages.error(request, 'Kullanıcı adı veya parola hatalı.')
        else:
            messages.error(request, 'Form geçersiz. Lütfen gerekli alanları doldurun.')
            print(form.errors)  # Formdaki hataları konsola yazdır
    else:
        form = AuthenticationForm()

    return render(request, 'admin_area/login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    user = request.user
    Log.objects.create(hareket=f"{user.username} kullanıcısı çıkış yaptı.", user=user, kullanici=user.username, kullandigi_view='logout' '-' 'çıkış')
    logout(request)
    return redirect('home','en')
def lockout_view(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    else:
        HttpResponse(400)
    return render(request, 'admin_area/lockout.html')  # lockout.html adlı şablonu gösteriyoruz
def custom_not_found_view(request, exception):
    # Your custom 404 view code here...
    return render(request, 'admin_area/404.html')
# def gallery(request):
#     gallery_items = Gallery.objects.all()
#     context = {
#         'gallery_items': gallery_items
#     }
    
#     return render(request, 'gallery.html', context)

def add_image(request):
    user = request.user
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            Log.objects.create(hareket=f"{user.username} kullanıcısı galeriye yeni bir fotoğraf ekledi.", user=user, kullanici=user.username, kullandigi_view='add-image' '-' 'fotoğraf-ekle')
            return redirect('gallery','en')  # Redirect to the gallery page after successful form submission
        else:
            print('Form geçersiz. Lütfen gerekli alanları doldurun.')
    else:
        form = GalleryForm()

    return render(request, 'admin_area/add_image.html', {'form': form})
def company(request):
    user = request.user
    company = Company.objects.first()
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            # Log.objects.create(hareket=f"{user.username} kullanıcısı Şirket Bilgilerinde güncelleme yaptı.", user=user, kullanici=user.username, kullandigi_view='Şirket' '-' 'Company')
            form.save()
            
            messages.success(request,'Güncelleme Başarılı')
            # Başarılı form işlemi için yapılacaklar
    else:
        form = CompanyForm(instance=company)
        print(form.errors)
    print(form.errors)
    
    return render(request, 'admin_area/company.html', {'form': form})

def certificate_detail(request, name):                  # SERTİFİKA DETAY SAYFASI
    certificate = get_object_or_404(Certificates, name=name)
    context = {
        'certificate': certificate
    }
    return render(request, 'certificate_detail.html', context)
def certificates(request):                               # SERTİFİKALAR SAYFASI
    certificates = Certificates.objects.all()
    context = {
        'certificates':certificates
    }
    return render(request,'certificates.html',context)

# ...

def upload_certificates(request):
    user = request.user
    if request.method == 'POST':
        form = CertificatesForm(request.POST, request.FILES)
        if form.is_valid():
            # Kontrol et: Aynı ada sahip bir sertifika daha önce var mı?
            existing_certificate = Certificates.objects.filter(name=form.cleaned_data['name']).exists()
            if existing_certificate:
                messages.error(request, "Bu ada sahip bir sertifikanız bulunuyor")
                print('HATA VERDİ AYNI ADDA OLDUĞU İÇİN')
                return render(request, 'admin_area/upload_certificates.html', {'form': form})

            certificate = form.cleaned_data['image']

            # Yüklenen resmi media dizinine kaydet
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(certificate.name, certificate)

            # Dosya yolu
            img_path = os.path.join(settings.MEDIA_ROOT, filename)

            try:
                # Rembg ile arka planı kaldırma işlemi
                img = Image.open(img_path).convert("RGBA")
                img = remove_background(img)

                # İşlenmiş resmi yeni bir klasöre kaydet
                processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed_img', 'certificates')
                os.makedirs(processed_dir, exist_ok=True)
                processed_filename = os.path.splitext(filename)[0] + '_processed.png'
                processed_img_path = os.path.join(processed_dir, processed_filename)
                img.save(processed_img_path)

                # Eski geçici dosyayı sil
                fs.delete(filename)

                # Yeni işlenmiş resmi veritabanına kaydet
                certificate_instance = form.save(commit=False)
                certificate_instance.image = 'processed_img/certificates/' + processed_filename
                certificate_instance.save()
                Log.objects.create(hareket=f"{user.username} kullanıcısı bir sertifika ekledi.", user=user, kullanici=user.username, kullandigi_view='upload-certificate' '-' 'sertifika-ekle')

                messages.success(request, 'Certificate uploaded successfully.')
                return redirect('certificates')  # Yükleme başarılıysa başka sayfaya yönlendir
            except Exception as e:
                error_message = f"Error during rembg: {e}"
                print(error_message)
                return render(request, 'admin_area/upload_certificates.html', {'form': form, 'error_message': error_message})

    else:
        form = CertificatesForm()
    
    return render(request, 'admin_area/upload_certificates.html', {'form': form})


def remove_background(img):
    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixdata[x, y]
            if (r > 200 and g > 200 and b > 200) or a < 50:
                pixdata[x, y] = (255, 255, 255, 0)

    return img

# Daha sonra kontrol edilecek yetki için
def kullanicilari_yetkilendir(request, kullanici_id):
    try:
        kullanici = wbtUser.objects.get(pk=kullanici_id)
    except wbtUser.DoesNotExist:
        # Kullanıcı ID'si hatalıysa veya kullanıcı bulunamazsa burada işlem yapabilirsiniz
        # Örneğin, bir hata mesajı gösterebilir veya yönlendirebilirsiniz.
        pass
    else:
        yetkiler = Permission.objects.filter(group__name='Tanıtım')

        if request.method == 'POST':
            yetki_listesi = request.POST.getlist(f"yetkiler_{kullanici_id}")
            mevcut_yetkiler = kullanici.yetkiler.all()  # Özel yetkiler
            django_yetkiler = kullanici.user_permissions.all()  # Django yetkileri

            # Seçilen yetkileri ekleyin
            for yetki_kod_adi in yetki_listesi:
                try:
                    yetki = Permission.objects.get(codename=yetki_kod_adi)
                    kullanici.yetkiler.add(yetki)  # Model alanına ekleyin
                    kullanici.user_permissions.add(yetki)  # Django yetkilerine ekleyin
                except Permission.DoesNotExist:
                    pass

            # Seçilmeyen yetkileri kaldırın
            for yetki in mevcut_yetkiler:
                if yetki.codename not in yetki_listesi:
                    kullanici.yetkiler.remove(yetki)  # Model alanından kaldırın

            # Django yetkileri için aynı işlemi yapın
            for yetki in django_yetkiler:
                if yetki.codename not in yetki_listesi:
                    kullanici.user_permissions.remove(yetki)  # Django yetkilerinden kaldırın

            # Değişiklikleri veritabanına kaydet
            kullanici.save()

        return redirect('dashboard')

def kullanici_sil(request, kullanici_pk):
    user = request.user
    try:
        kullanici = wbtUser.objects.get(pk=kullanici_pk)
        kullanici.delete()
        Log.objects.create(hareket=f"{user.username} { kullanici.username }kullanıcısını sildi.", user=user, kullanici=user.username, kullandigi_view='delete_user' '-' 'kullanici_sil')
        return redirect('dashboard')  # Kullanıcı silme işlemi başarılı olursa kullanicilari_listele sayfasına yönlendir
    except wbtUser.DoesNotExist:
        return redirect('dashboard') 
     # Eğer kullanıcı bulunamazsa veya silinemezse yine kullanicilari_listele sayfasına yönlendir


@login_required
# @permission_required('tanitim.dashboard')  # Belirli bir izne sahip olması gerekiyor
def dashboard(request):
    user = request.user
    # log_kayitlari_perm = Permission.objects.get(codename='log_kayitlari')
    # servis_ekle_perm = Permission.objects.get(codename='servşs_ekle')
    # log_kayitlari_perm = Permission.objects.get(codename='log_kayitlari')
    # log_kayitlari_perm = Permission.objects.get(codename='log_kayitlari')
    # log_kayitlari_perm = Permission.objects.get(codename='log_kayitlari')
    # log_kayitlari_perm = Permission.objects.get(codename='log_kayitlari')
    # Log.objects.create(hareket=f"{user.username} admin sayfasına giriş yaptı.", user=user, kullanici=user.username, kullandigi_view='dashboard' '-' 'admin-sayfası')
    company = Company.objects.first()

    context = {
            # 'yeni_mesaj': company.yeni_mesaj,
        }

    return render(request, 'dashboard.html', context)
@permission_required('tanitim.log_kayitlari')
def log(request):
    user = request.user
    logs = Log.objects.filter(silindi=False).order_by('-id')
    context = {
        'logs':logs,
    }
    return render(request,'admin_area/log_kayitlari.html',context)
# import tablib
# def export_excel(request):
#     logs = Log.objects.all()
    
#     # Verileri tabloya dönüştürme
#     data = tablib.Dataset()
#     data.headers = ['ID', 'Kullanıcı', 'İşlem', 'Tarih']
    
#     for log in logs:
#         data.append([log.id, log.kullanici, log.hareket, log.tarih.strftime('%d.%m.%Y %H:%M:%S')])
    
#     # Excel dosyası oluşturma
#     response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="loglar.xlsx"'
#     return response
# SİLME İŞLEMLERİ  #
def log_sil(request, id):
    if request.method == 'POST':
        log = get_object_or_404(Log, id=id)       
        log.silindi = True
        log.save()  # Silme işlemi
        
        return redirect('log')
    else:
        return redirect('log')
def dead_all_logs(request):
    user = request.user
    if user.username =="serkan":
        log = Log.objects.all()
        log.delete()
        return redirect('log')
    else:
        print('yönetici değil')
        return redirect('log')
# SİLME İŞLEMLERİ

@permission_required('tanitim.silme_islemi', raise_exception=True)
def silme_ekranı(request):
    try:
        services = Services.objects.all()
        gallery = Gallery.objects.all()
        certificates = Certificates.objects.all()
        context = {
            'services': services,
            'certificates': certificates,
            'gallery': gallery,
        }
        return render(request, 'admin_area/silme_ekranı.html', context)
    except PermissionDenied:
        if PermissionDenied:
            messages.error(request, f'Hata oluştu: {str(e)}')
    except Exception as e:
        messages.error(request, f'Hata oluştu: {str(e)}')
        return redirect(reverse('dashboard'))

@csrf_protect
def delete_service(request, id):
    if request.method == 'POST':
        service = get_object_or_404(Services, id=id)
        service.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseNotAllowed(['POST'])
def delete_certificate(request,id):
    if request.method == 'POST':
        certificates = get_object_or_404(Certificates, id=id)
        certificates.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseNotAllowed(['POST'])
def delete_gallery(request,id):
    if request.method == 'POST':
        image = get_object_or_404(Gallery, id=id)
        image.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseNotAllowed(['POST'])
    ##      ##          ###     #####
######                                   GÜNCELLEME İŞLEMLERİ                        ########
def update_service(request, id):
    service = get_object_or_404(Services, id=id)
    
    if request.method == 'POST':
        form = ServicesUpdateForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            # Güncelleme işlemi başarılı olduğunda yönlendirme yapabilirsiniz.
            return redirect('services',lang='en')  # Sizin sayfa isminize göre düzenleyin
    else:
        form = ServicesUpdateForm(instance=service)
    
    context = {
        'form': form,
        'service': service,
    }
    
    return render(request, 'admin_area/update_service.html', context)
def update_certificate(request, id):
    certificates = get_object_or_404(Certificates, id=id)
    
    if request.method == 'POST':
        form = UpdateCertificatesForm(request.POST, request.FILES, instance=certificates)
        if form.is_valid():
            form.save()
            # Güncelleme işlemi başarılı olduğunda yönlendirme yapabilirsiniz.
            return redirect('certificates')  # Sizin sayfa isminize göre düzenleyin
    else:
        form = UpdateCertificatesForm(instance=certificates)
    
    context = {
        'form': form,
        'certificates': certificates,
    }
    
    return render(request, 'admin_area/update_certificates.html', context)
def iletisim_form(request):
    company = Company.objects.first()
    yeni_mesaj = company.yeni_mesaj
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            # Form verilerini işleme kodu burada
            message = form.cleaned_data['mesaj']
            subject = form.cleaned_data['konu']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['telefon']
            company.yeni_mesaj += 1
            company.save()
            form.save()
            
            # Verileri işleme, kaydetme vb. işlemler
            
            return redirect('home', {'form': form,'message': message, 'subject': subject, 'email': email, 'phone': phone})
    print(form.errors)
    return redirect(request.META.get('HTTP_REFERER'))
def message(request):
    messages = Message.objects.exclude(durum="Silindi")
    
    # Company modelinden yeni_mesaj değerini alın
    company = Company.objects.first()  # veya gerekli nesneyi alın
    company.yeni_mesaj = 0
    company.save()
    context = {
        'messages': messages,
         # yeni_mesaj değerini context'e ekleyin
    }
    
    return render(request, 'admin_area/messages.html', context)
def update_message_status(request, message_id):
    user = request.user
    if request.method == "GET":
        new_status = request.GET.get("new_status")
        valid_statuses = [status[0] for status in Message.DURUM_CHOICES]
        
        if new_status in valid_statuses:
            message = Message.objects.get(pk=message_id)
            message.durum = new_status
            message.save()
            Log.objects.create(hareket=f"{user.username} kullanıcısı {message.mesaj} mesajının durumunu {message.durum} olarak güncelledi.", user=user, kullanici=user.username, kullandigi_view='add-image' '-' 'fotoğraf-ekle')            
            return redirect("message")
        else:
            return HttpResponse("Invalid status value")
    else:
        return HttpResponse("Invalid request method")