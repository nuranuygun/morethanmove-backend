import os
from dotenv import load_dotenv

# Gizli değişkenleri tuttuğum .env dosyasını sisteme yüklüyorum.
load_dotenv()

class Config:
    """
    Projenin genel ayarlarını tek merkezde topladığım sınıf.
    .env içinde tanım varsa onu alıyorum, yoksa varsayılan güvenli değeri atıyorum.
    """
    
    # Oturum güvenliği için secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'morethanmove-gizli-anahtar-12345')
    
    # SQLite veritabanı dosyamın adı
    DATABASE_URL = os.environ.get('DATABASE_URL', 'morethanmove.db')
    
    # Kullanacağım yapay zekâ sağlayıcısı (groq seçtim)
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    
    # AI servisi için API anahtarları
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

    
    # Wix bağlantısına izin veren CORS ayarı
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Chatbot'un nasıl davranacağını belirlediğim sistem talimatı 
    BUSINESS_CONTEXT = os.environ.get(
        'BUSINESS_CONTEXT', 
        'Sen More Than Move platformunun cana yakın, bilgili ve yardımsever yapay zekâ asistanısın. '
        'Kullanıcılara salon doluluk oranları, ders saatleri, rezervasyonlar ve spor tavsiyeleri konusunda yardımcı ol.'
    )

class DevelopmentConfig(Config):
    """
    Kendi bilgisayarımda geliştirme yaparken kullanacağım ortam ayarları.
    Hataları detaylı görmek için DEBUG modunu açık tutuyorum.
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Canlıya alırken kullanılacak ortam ayarları.
    Güvenlik gerekçesiyle DEBUG modunu kapatıyorum.
    """
    DEBUG = False

# Ortam seçimini kolaylaştırmak için oluşturduğum sözlük
# Ana uygulamayı başlatırken tek satırda ayar seçebilmek için
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
