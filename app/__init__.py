from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.database import init_db, close_db
from app.routes import pages_bp, api_bp

def create_app(config_class=Config):
    """
    Application Factory (Uygulama Fabrikası) Fonksiyonu.
    Sistemin tüm parçalarını bir araya getirerek Flask uygulamasını oluşturur.
    """
    app = Flask(__name__)
    
    # 1. Ayarları Yükle
    app.config.from_object(config_class)

    # 2. CORS Aç (Wix ve dış isteklerin engellenmemesi için)
    CORS(app)

    # 3. Veritabanı Temizliği için Teardown Bağlantısı
    app.teardown_appcontext(close_db)

    # 4. Veritabanını Uygulama Bağlamında (App Context) İlklendir
    with app.app_context():
        init_db(app)

    # 5. Blueprint'leri Kaydet
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp) # url_prefix='/api' tanımı routes.py içinde yapılmıştı

    # 6. Ana Dizin Karşılama Rotası (/)
    @app.route('/')
    def home():
        return jsonify({
            "status": "healthy",
            "message": "More Than Move Backend API Aktif"
        }), 200

    # 7. Sunucu Canlılık Kontrolü (/health)
    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "Sunucu sorunsuz çalışıyor."
        }), 200

    # 8. Uygulamayı Döndür
    return app 