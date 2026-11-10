import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Frontend va Backend orasidagi xavfsiz aloqani ta'minlash (CORS)
CORS(app)

# 1. Gemini API Kalitini sozlash
# O'z API kalitingizni shu yerga kiriting yoki muhit o'zgaruvchisiga (Environment Variable) joylang
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "curl "AQ.Ab8RN6Jv2Ba5yzd-mNOsw0xDSLedigmDEo56hCpVjnYUZYyMJw" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AQ.Ab8RN6Jv2Ba5yzd-mNOsw0xDSLedigmDEo56hCpVjnYUZYyMJw' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'")
genai.configure(api_key=GEMINI_API_KEY)

# 2. O'zbekiston ta'lim muassasalari va tizimi uchun maxsus tizimli ko'rsatma (System Prompt)
SYSTEM_INSTRUCTION = """
Siz MuallimUz platformasining intellektual ta'lim yordamchisiz. Foydalanuvchilarga faqat O'zbekiston Respublikasining maktabgacha ta'lim, umumiy o'rta ta'lim, o'rta maxsus va oliy ta'lim muassasalari bilan bog'liq ishonchli va rasmiy ma'lumotlarni taqdim etasiz. Ma'lumotlarni tahlil qilishda faqat quyidagi rasmiy manbalar va ularga tegishli ochiq ma'lumotlar bazasiga tayanishingiz shart:
1. O'zbekiston Respublikasi Maktabgacha va maktab ta'limi vazirligi (uzedu.uz)
2. Oliy ta'lim, fan va innovatsiyalar vazirligi (edu.uz)
3. Ta'lim portallari (ziyonet.uz, umail.uz)

Agar foydalanuvchi ta'lim tizimiga aloqador bo'lmagan mavzularda savol bersa, ularga xushmuomalalik bilan rad javobini bering va faqat O'zbekiston ta'lim tizimi doirasida yordam bera olishingizni eslating. Javoblaringiz aniq, sodda va o'zbek tilida bo'lishi lozim.
"""

# Modelni tizimli prompt bilan sozlash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

@app.route('/gemini-chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"reply": "Xabar bo'sh bo'lishi mumkin emas."}), 400
        
        # Gemini modelidan javob olish
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"Xatolik yuz berdi: {str(e)}")
        return jsonify({"reply": "Tizimda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."}), 500

if __name__ == '__main__':
    # Mahalliy serverni 5000-portda ishga tushirish
if __name__ == '__main__':
    # Render muhitidagi portni avtomatik aniqlash (Render talabi)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
