from flask import Blueprint, render_template, request, jsonify
from app.services.ai_service import ai_service, AIServiceError
from app.database import lead_ekle, tum_leadleri

# İki Ayrı Blueprint Tanımlıyoruz
pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')


# SAYFA ROTALARI

@pages_bp.route('/')
def home():
    """
    Karşılama (ana) sayfasını gösterir.
    """
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    """
    Yönetim panelini gösterir.
    """
    return render_template('dashboard.html')


# --- API UÇ NOKTALARI (/api öneki ile) ---

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """
    Kullanıcıdan gelen mesajı alır ve AI servisine iletir.
    """
    data = request.get_json() or {}
    mesaj = data.get('mesaj')
    gecmis = data.get('gecmis', [])

    # Eksik veri kontrolü (400 Hatası)
    if not mesaj or not str(mesaj).strip():
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı boş bırakılamaz."
        }), 400

    # Yapay zekâ çağrısı try-except ile sarılıyor
    try:
        yanit = ai_service.yanit_uret(mesaj=mesaj, gecmis=gecmis)
        return jsonify({
            "basari": True,
            "yanit": yanit
        }), 200
    except AIServiceError as e:
        # AI Servis Hatası (503 Hizmet Dışı Hatası)
        return jsonify({
            "basari": False,
            "hata": f"Yapay zekâ servisinde bir sorun oluştu: {str(e)}"
        }), 503
    except Exception as e:
        return jsonify({
            "basari": False,
            "hata": "Beklenmeyen bir hata oluştu."
        }), 500


@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    """
    Wix veya form üzerinden gelen yeni müşteri adayını veritabanına kaydeder.
    """
    data = request.get_json() or {}
    isim = data.get('isim')
    telefon = data.get('telefon')
    cinsiyet = data.get('cinsiyet')
    dogum_tarihi = data.get('dogum_tarihi')
    mesaj = data.get('mesaj')

    # Eksik veri kontrolü (400 Hatası)
    if not isim or not str(isim).strip():
        return jsonify({
            "basari": False,
            "hata": "İsim alanı zorunludur."
        }), 400

    if not telefon or not str(telefon).strip():
        return jsonify({
            "basari": False,
            "hata": "Telefon alanı zorunludur."
        }), 400

    # Kayıt ekleme (201 Oluşturuldu Kodu)
    try:
        lead_id = lead_ekle(
            isim=isim.strip(),
            telefon=telefon.strip(),
            cinsiyet=cinsiyet.strip() if cinsiyet else None,
            dogum_tarihi=dogum_tarihi.strip() if dogum_tarihi else None,
            mesaj=mesaj.strip() if mesaj else None
        )
        return jsonify({
            "basari": True,
            "mesaj": "Müşteri adayı başarıyla kaydedildi.",
            "id": lead_id
        }), 201
    except Exception as e:
        return jsonify({
            "basari": False,
            "hata": "Kayıt sırasında veritabanı hatası oluştu."
        }), 500


@api_bp.route('/leads', methods=['GET'])
def tum_leadleri_getir():
    """
    Veritabanındaki tüm müşteri adaylarını listeler.
    """
    try:
        raw_leads = tum_leadleri()
        # sqlite3.Row objelerini JSON formatına dönüştürüyoruz
        lead_listesi = [dict(row) for row in raw_leads]
        
        return jsonify({
            "basari": True,
            "data": lead_listesi
        }), 200
    except Exception as e:
        return jsonify({
            "basari": False,
            "hata": "Müşteri adayları getirilirken bir hata oluştu."
        }), 500
    