More Than Move 

More Than Move, farklı spor dallarını tek bir platform üzerinden keşfetmeyi ve kullanıcıların kendilerine uygun spor deneyimlerine ulaşmasını amaçlayan web tabanlı bir projedir.

Proje kapsamında Wix Studio üzerinde kullanıcı arayüzü, Python/Flask ve Render üzerinde ise backend sistemi geliştirilmiştir.

=Proje Yapısı=

Proje iki ana bölümden oluşmaktadır:

*Wix Studio: Kullanıcı arayüzü ve web sitesi.
*Flask / Render: API, yapay zekâ servisi ve veritabanı işlemlerini gerçekleştiren backend.

Wix ile Render backend arasında API bağlantısı kullanılmaktadır.

=Kullanılan Teknolojiler=
*Python
*Flask
*SQLite
*Flask-CORS
*Gunicorn
*Python-dotenv
*Yapay zekâ API'si(GROQ)
*Wix Studio / Velo
*Render
*GitHub

===Temel Özellikler===

=Yapay Zekâ Destekli Sohbet=

Kullanıcının gönderdiği mesaj Flask backend üzerinden yapay zekâ servisine iletilir ve oluşturulan yanıt Wix arayüzüne gönderilir.

Endpoint:

*POST /api/sohbet

=Müşteri Adayı Kaydı=

Wix üzerindeki form aracılığıyla alınan müşteri adayı bilgileri backend üzerinden veritabanına kaydedilir.

Desteklenen bilgiler:

*İsim
*Telefon
*Cinsiyet
*Doğum tarihi
*Mesaj

Endpointler:

*POST /api/leads
*GET /api/leads

=Yönetim Paneli=

Yönetim panelinde backend üzerinden alınan müşteri adayı kayıtları Wix Repeater bileşeni kullanılarak listelenmektedir.

Panelde temel olarak:

*İsim
*Telefon
*Mesaj

=Sunucu Sağlık Kontrolü=

Backend'in çalışıp çalışmadığını kontrol etmek için /health endpoint'i bulunmaktadır.

Endpoint:

*GET /health

Başarılı çalıştığında aşağıdaki gibi bir cevap döndürür:
{ "status": "healthy", "message": "Sunucu sorunsuz çalışıyor." }

=Kurulum=

Projeyi GitHub üzerinden indirdikten sonra gerekli Python paketleri yüklenmelidir:

pip install -r requirements.txt

Gizli API anahtarları .env dosyasında tutulmalıdır.
.env dosyası güvenlik nedeniyle GitHub deposuna yüklenmemelidir.

=Çalıştırma=

Projeyi çalıştırmak için:

python run.py

Uygulama lokal Flask sunucusunda çalışacaktır.

=Render Deployment=

Backend Render üzerinde yayınlanmıştır.

=Start Command=

gunicorn run:app

Gizli API anahtarları Render üzerindeki Environment Variables bölümünde tanımlanmalıdır.

=Canlı backend=

https://morethanmove-backend.onrender.com

=Sunucu sağlık kontrolü=

https://morethanmove-backend.onrender.com/health
