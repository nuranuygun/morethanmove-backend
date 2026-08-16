import sqlite3
from flask import g, current_app

def get_db():
    """
    Veritabanına güvenli bağlantı kurar.
    'g' objesi Flask'ın istek (request) ömrünce veri saklayan özel alanıdır.
    Böylece aynı istek içinde defalarca veritabanı bağlantısı açılmaz, var olan bağlantı kullanılır.
    """
    if 'db' not in g:
        # config.py içindeki DATABASE_URL yolunu okuyarak SQLite veritabanına bağlanıyoruz
        g.db = sqlite3.connect(
            current_app.config['DATABASE_URL'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Veritabanından çekilen satırların 'sözlük' (row['isim']) gibi okunabilmesini sağlar
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Kullanıcının isteği tamamlandığında veritabanı bağlantısını kapatır.
    Sistemde açık bağlantı kalmasını ve bellek sızıntısını engeller.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """
    Uygulama başlatıldığında veritabanı tablosunu hazırlar.
    'leads' adında bir tablo yoksa otomatik olarak oluşturur.
    """
    with app.app_context():
        db = get_db()
        # id: Otomatik artan benzersiz numara
        # isim & telefon: Müşteri adayı için zorunlu bilgiler
        # cinsiyet & dogum_tarihi: Opsiyonel kişisel bilgiler
        # mesaj: Kullanıcının bıraktığı isteğe bağlı not
        # tarih: Kayıt eklendiği andaki sistem saati
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                cinsiyet TEXT,
                dogum_tarihi TEXT,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit() # Değişiklikleri veritabanına işler

def lead_ekle(isim, telefon, cinsiyet=None, dogum_tarihi=None, mesaj=None):
    """
    Wix üzerinden form dolduran yeni müşteri adayını veritabanına kaydeder.
    Yeni eklenen cinsiyet ve dogum_tarihi parametreleri varsayılan olarak None (boş) bırakılabilir.
    GÜVENLİK NOTU: SQL Injection koruması için '?' yer tutucuları kullanıyoruz.
    """
    db = get_db()
    cursor = db.cursor()
    
    # 5 adet veri alanımız olduğu için 5 adet '?' yer tutucu kullanıyoruz
    cursor.execute(
        'INSERT INTO leads (isim, telefon, cinsiyet, dogum_tarihi, mesaj) VALUES (?, ?, ?, ?, ?)',
        (isim, telefon, cinsiyet, dogum_tarihi, mesaj)
    )
    db.commit() # Kaydı onaylar
    return cursor.lastrowid # Eklenen son kaydın ID'sini döndürür

def tum_leadleri():
    """
    Tüm kayıtlı müşteri adaylarını getirir.
    ORDER BY tarih DESC sayesinde en yeni gelen başvurular en üstte yer alır.
    """
    db = get_db()
    leads = db.execute(
        'SELECT * FROM leads ORDER BY tarih DESC'
    ).fetchall()
    return leads