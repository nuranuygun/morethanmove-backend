import requests
from config import Config

class AIServiceError(Exception):
    """
    Yapay zekâ servisinde bir sorun oluştuğunda fırlatılacak özel hata sınıfı.
    Bu sayede hataları diğer sistem hatalarından ayırt edebiliriz.
    """
    pass

class AIService:
    def _get_system_instruction(self):
        """
        Sistem talimatını (asistan kişiliğini) config.py üzerinden okuyan yardımcı metot.
        """
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını ve sohbet geçmişini alıp Groq API'sine gönderir ve yanıtı döndürür.
        """
        if gecmis is None:
            gecmis = []

        # 1. API Anahtarı Kontrolü (Anahtar yoksa demo modu mesajı döndür)
        api_key = Config.GROQ_API_KEY
        if not api_key:
            return "Demo modundayım. Gerçek yapay zekâ yanıtları için lütfen GROQ_API_KEY değerini .env dosyasına ekleyin."

        # 2. 'messages' listesini yönergedeki sırayla oluştur:
        # Önce sistem talimatı (role: system)
        messages = [
            {"role": "system", "content": self._get_system_instruction()}
        ]

        # Sonra sohbet geçmişi
        for g in gecmis:
            messages.append(g)

        # En sonda yeni kullanıcı mesajı
        messages.append({"role": "user", "content": mesaj})

        # 3. Groq API İstek Yapılandırması
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.7
        }

        # 4. İstegi try-except ile sarmalayarak güvenli şekilde gönder
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code != 200:
                raise AIServiceError(f"Groq API Hatası ({response.status_code}): {response.text}")

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            if isinstance(e, AIServiceError):
                raise e
            raise AIServiceError(f"Yapay zekâ servisi ile iletişim kurulurken bir hata oluştu: {str(e)}")

# Dosya sonunda tek bir örnek (instance) oluşturuyoruz
ai_service = AIService()