from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('<str:lang>/home/', views.home, name='home'),
    path('<str:lang>/anasayfa/', views.anasayfa, name='anasayfa'),
    path('language/<str:lang>/', views.set_language, name='set_language'),
    path('<str:lang>/servis_detay/<int:id>',views.servis_detay,name='servis_detay'),
    path('<str:lang>/service_detail/<int:id>',views.service_detail,name='service_detail'),
    path('<str:lang>/about/', views.about, name='about'),
    path('<str:lang>/hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('<str:lang>/services/', views.services, name='services'),
    path('<str:lang>/hizmetlerimiz/', views.hizmetlerimiz, name='hizmetlerimiz'),
    path('<str:lang>/iletisim/', views.iletisim, name='iletisim'),
    path('<str:lang>/contact/', views.contact, name='contact'),
    path('<str:lang>/gallery/', views.gallery, name='gallery'),
    path('<str:lang>/galeri/', views.galeri, name='galeri'),
    path('certificates/', views.certificates, name='certificates'),
    path('certificate/<str:name>', views.certificate_detail, name='certificate_detail'),
    # path('<str:lang>/galeri/', views.galeri, name='galeri'),
    path('wbtadminarea/upload_certificates/', views.upload_certificates, name='upload_certificates'),
    path('wbtadminarea/add_services', views.add_service, name='add_services'),
    path('wbtadminarea/login/',views.login_view, name='login'),
    path('wbtadminarea/register/',views.register, name='register'),
    path('logout/',views.logout_view, name='logout'),
    #for brute force
    path('lockout/', views.lockout_view, name='lockout'),
    path('wbtadminarea/add_image/', views.add_image, name='add_image'),
    path('wbtadminarea/company/', views.company, name='company'),
    # path('wbtadminarea/kullanicilari_listele/', views.kullanicilari_yetkilendir, name='kullanicilari_yetkilendir'),
    path('yetki-ver/<int:kullanici_id>/', views.kullanicilari_yetkilendir, name='kullanicilari_yetkilendir'),
    path('wbtadminarea/dashboard/', views.dashboard, name='dashboard'),
    path('wbtadminarea/log/', views.log, name='log'),
    path('kullanici_sil/<int:kullanici_pk>',views.kullanici_sil,name='kullanici_sil'),
    # path('export-excel/', views.export_excel, name='export_excel'),
    path('log_sil/<int:id>', views.log_sil, name='log_sil'),
    path('dead_all_logs', views.dead_all_logs, name='dead_all_logs'),
    path('delete_service/<int:id>', views.delete_service, name='delete_service'),
    path('delete_certificate/<int:id>', views.delete_certificate, name='delete_certificate'),
    path('delete_gallery/<int:id>', views.delete_gallery, name='delete_gallery'),
    path('update_certificate/<int:id>',views.update_certificate, name='update_certificate'),
    
    path('silme_ekranı/', views.silme_ekranı, name='silme_ekranı'),
    #### UPDATE İŞLEMLERİ
    path('update_service/<int:id>',views.update_service, name='update_service'),
    path('iletisim_form/', views.iletisim_form, name='iletisim_form'),
    path('message/', views.message, name='message'),
    path('update_message_status/<int:message_id>/', views.update_message_status, name='update_message_status'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'wbt.views.custom_not_found_view'