import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Inisialisasi API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Inisialisasi API Groq (cadangan)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def _detect_language(text: str) -> str:
    """
    Detect if text is in Indonesian or English.
    Returns 'id' for Indonesian, 'en' for English.
    Improved detection with more Indonesian indicators.
    """
    # Kata dan pola Bahasa Indonesia umum (diperluas untuk sensitivitas lebih baik)
    indonesian_indicators = [
        # Kata umum
        'yang', 'dan', 'atau', 'dengan', 'untuk', 'dari', 'ini', 'itu', 'sangat', 'sekali',
        'saya', 'kami', 'mereka', 'anda', 'sudah', 'belum', 'akan', 'tidak', 'bukan',
        'jadi', 'juga', 'saja', 'sih', 'nih', 'dong', 'lah', 'kan', 'ya', 'gak', 'ga',
        # Kata-kata sentimen
        'bagus', 'jelek', 'buruk', 'mantap', 'keren', 'puas', 'kecewa', 'mengecewakan',
        'memuaskan', 'sangat bagus', 'sangat baik', 'sangat puas', 'sangat memuaskan',
        'luar biasa', 'sempurna', 'terbaik', 'paling bagus', 'paling baik',
        # Terkait produk
        'produk', 'barang', 'kualitas', 'harga', 'pelayanan', 'pengiriman', 'rekomendasi',
        'direkomendasikan', 'tidak direkomendasikan', 'worth it', 'sangat worth it',
        # Frasa umum
        'banget', 'amat', 'terlalu', 'cukup', 'lumayan', 'agak', 'sedikit',
        'suka', 'senang', 'terkesan', 'impressed', 'love it', 'suka banget',
        'ada masalah', 'banyak masalah', 'sering masalah', 'tidak sesuai', 'tidak cocok',
        'kurang baik', 'kurang bagus', 'kurang memuaskan', 'rugi', 'buang uang',
        # Bentuk kepemilikan (sangat khas Indonesia)
        'produknya', 'barangnya', 'kualitasnya', 'harganya', 'pelayanannya', 'pengirimannya',
        'rasanya', 'tampilannya', 'kemasannya', 'packagingnya',
        # Spesifik makanan/rasa
        'enak', 'enak dimakan', 'lezat', 'nikmat', 'sedap', 'gurih', 'manis',
        # Spesifik penampilan
        'cantik', 'menarik', 'indah', 'rapi', 'bersih', 'tampilannya',
        # Pola gabungan
        'keren dan', 'bagus dan', 'enak dan', 'keren enak', 'bagus enak',
        'produknya keren', 'produknya bagus', 'produknya enak', 'barangnya keren'
    ]
    
    text_lower = text.lower()
    
    # Hitung indikator Bahasa Indonesia
    indonesian_count = 0
    for indicator in indonesian_indicators:
        if indicator in text_lower:
            indonesian_count += 1
    
    # Periksa pola khusus Bahasa Indonesia (diperluas)
    indonesian_patterns = [
        r'\b(sangat|amat|terlalu|banget)\s+(bagus|baik|jelek|buruk|puas|kecewa|enak|lezat|keren)',
        r'\b(paling|ter)\s+(bagus|baik|jelek|buruk)',
        r'\b(tidak|belum|bukan)\s+(bagus|baik|puas|memuaskan|direkomendasikan)',
        r'\b(kurang|agak|sedikit)\s+(bagus|baik|puas|memuaskan)',
        r'\b(suka|senang|terkesan)\s+(banget|sekali)',
        r'\b(worth|worth it)\s+(banget|sekali)',
        # Pola kepemilikan (sangat khas Indonesia)
        r'\b(produk|barang|kualitas|harga|rasa|tampilan|kemasan|packaging)nya\s+',
        r'\b(produknya|barangnya)\s+(keren|bagus|enak|mantap|jelek|buruk)',
        r'\b(rasanya|tampilannya)\s+(enak|lezat|keren|bagus)',
        # Pola gabungan
        r'\b(keren|bagus|mantap)\s+dan\s+(enak|lezat|bagus|keren)',
        r'\b(enak|lezat)\s+(dimakan|rasanya|banget)',
        r'\b(keren|bagus|mantap)\s+(enak|lezat)\s+dimakan',
    ]
    
    pattern_matches = sum(1 for pattern in indonesian_patterns if re.search(pattern, text_lower))
    
    # Periksa urutan kata Bahasa Indonesia (subjek-kata kerja-objek khas)
    indonesian_word_order_patterns = [
        r'\b\w+nya\s+(keren|bagus|enak|mantap|jelek|buruk)',  # "produknya keren"
        r'\b\w+nya\s+dan\s+\w+',  # "produknya keren dan enak"
    ]
    
    word_order_matches = sum(1 for pattern in indonesian_word_order_patterns if re.search(pattern, text_lower))
    
    # Jika ditemukan indikator/pola/urutan kata Indonesia, kemungkinan bahasa adalah Indonesia
    # Turunkan ambang untuk deteksi ulasan pendek yang lebih baik
    if indonesian_count >= 1 or pattern_matches >= 1 or word_order_matches >= 1:
        return 'id'
    
    return 'en'


def extract_key_points(review_text: str) -> str:
    """
    Extract key points from the review using AI APIs.
    Priority: Gemini → Groq → Simple Extraction
    Returns: A string containing key points extracted from the review.
    """
    # Langkah 1: Coba API Gemini
    if GEMINI_API_KEY:
        result = _try_gemini_extraction(review_text)
        if result:
            return result
    
    # Langkah 2: Coba API Groq (cadangan)
    if GROQ_API_KEY:
        result = _try_groq_extraction(review_text)
        if result:
            return result
    
    # Langkah 3: Cadangan ke ekstraksi sederhana
    print("Warning: No AI API available, using simple extraction")
    return _simple_key_points_extraction(review_text)


def _try_gemini_extraction(review_text: str) -> str:
    """Try to extract key points using Gemini API"""
    if not GEMINI_API_KEY:
        return None
    
    # Deteksi bahasa
    language = _detect_language(review_text)
    
    # Coba model Gemini berbeda (terbaru dulu)
    models_to_try = [
        'gemini-2.5-flash',      # Latest fast model (recommended)
        'gemini-2.5-pro',        # Latest capable model
        'gemini-2.0-flash',      # Previous version
        'gemini-flash-latest',   # Latest flash (alias)
        'gemini-pro-latest',     # Latest pro (alias)
        'gemini-1.5-flash',      # Older version (fallback)
        'gemini-1.5-pro',        # Older version (fallback)
        'gemini-pro',            # Legacy (last resort)
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            
            # Buat prompt khusus bahasa (ditingkatkan untuk Bahasa Indonesia dengan sensitivitas lebih tinggi)
            if language == 'id':
                prompt = f"""Analisis review produk berikut dengan SENSITIVITAS SANGAT TINGGI terhadap nuansa bahasa Indonesia. Pahami konteks, ekspresi sehari-hari, pola kalimat, dan makna tersirat dengan sangat detail.

Teks review:
{review_text}

Instruksi analisis (SANGAT PENTING - baca dengan teliti):

1. Pahami konteks dan nuansa bahasa Indonesia dengan sangat detail:
   - Perhatikan ekspresi sehari-hari seperti "keren", "enak dimakan", "mantap", "banget", "produknya", "barangnya"
   - Deteksi makna tersirat dari kalimat pendek atau sederhana - jangan abaikan review singkat!
   - Pahami pola bahasa Indonesia: "produknya keren" = produk memiliki tampilan/desain yang menarik
   - Pahami bahwa "keren dan enak" menunjukkan kepuasan positif pada 2 aspek: tampilan DAN rasa
   - Perhatikan kombinasi kata yang menunjukkan sentimen (contoh: "keren dan enak dimakan" = positif kuat pada tampilan dan rasa)
   - Pahami bentuk posesif "-nya": "produknya keren" = "produk ini keren", "rasanya enak" = "rasa produk ini enak"
   - Deteksi aspek produk yang disebutkan: "keren" biasanya tentang tampilan/desain, "enak" tentang rasa/kualitas

2. Ekstrak poin penting dengan fokus SANGAT SPESIFIK:
   - Kekurangan atau kelebihan utama produk: sebutkan ASPEK SPESIFIK (rasa, tampilan, kualitas, harga, dll)
   - Fitur, kualitas, harga, atau aspek produk: ekstrak dari kata-kata yang digunakan
     * "keren" = tampilan/desain menarik
     * "enak" atau "enak dimakan" = rasa/kualitas baik
     * "keren dan enak" = tampilan menarik DAN rasa baik
   - Kesan keseluruhan pengguna: dari konteks dan kombinasi kata, bukan hanya kata kunci
   - Rekomendasi atau peringatan: jika tersirat dari sentimen positif/negatif
   - Masalah atau kelebihan yang menonjol: dari keseluruhan review

3. Format output (HARUS RINGKAS DAN SPESIFIK):
   - Berikan 3-5 poin penting yang paling relevan (jika review singkat, bisa 2-3 poin)
   - Maksimal 2 baris per poin (ringkas dan padat)
   - Gunakan bahasa Indonesia yang natural, seperti orang Indonesia berbicara sehari-hari
   - Hindari kalimat yang terlalu panjang atau bertele-tele
   - Hindari frasa generik seperti "Produk ini memiliki..." atau "Pengguna mengatakan..." atau "Review ini menunjukkan..."
   - Langsung ke poin: "Rasa enak dan tampilan menarik" bukan "Produk ini memiliki rasa yang enak dan tampilan yang menarik"
   - Jika review singkat, ekstrak makna tersirat dengan tepat, jangan hanya parafrase ulang

4. Sensitivitas khusus untuk review singkat:
   - Jika review "produknya keren dan enak dimakan":
     * Ekstrak: "Tampilan produk menarik (keren)" dan "Rasa produk enak dan layak dikonsumsi"
     * Jangan hanya: "Produk memiliki tampilan yang keren dan rasa yang enak dimakan" (terlalu literal)
   - Jika review "keren dan enak":
     * Ekstrak: "Tampilan menarik" dan "Rasa/kualitas baik"
   - Pahami bahwa review singkat pun bisa mengandung informasi penting - jangan abaikan!
   - Jangan membuat asumsi berlebihan, tapi juga jangan terlalu literal
   - Fokus pada apa yang BENAR-BENAR dikatakan atau tersirat, bukan template generik
   - Untuk setiap kata kunci, pahami aspek produk yang dimaksud:
     * "keren" = tampilan/desain/visual
     * "enak" = rasa/kualitas konsumsi
     * "bagus" = kualitas umum
     * "mantap" = kepuasan umum

5. Contoh ekstraksi yang benar:
   - Review: "produknya keren dan enak dimakan"
   - Output yang BENAR:
     • Tampilan produk menarik dan menarik perhatian
     • Rasa produk enak dan layak dikonsumsi
     • Pengguna puas dengan aspek visual dan rasa produk
   - Output yang SALAH (terlalu generik):
     • Produk ini memiliki tampilan yang keren
     • Produk ini memiliki rasa yang enak dimakan
     • Pengguna mengatakan bahwa produk ini keren dan enak dimakan

Jawab LANGSUNG dengan poin-poin penting, tanpa header, pengantar, atau penjelasan tambahan. Gunakan format bullet point (•) untuk setiap poin. Fokus pada informasi SPESIFIK dan RELEVAN."""
            else:
                prompt = f"""Analyze the following product review and extract the key points concisely.
                
Focus on:
- Main concerns or praises
- Specific features mentioned
- Overall impression
- Any recommendations or warnings

Review text:
{review_text}

Provide a concise summary of key points (3-5 points, max 2 lines per point). Be brief and relevant."""
            
            response = model.generate_content(prompt)
            if response and response.text:
                result = response.text.strip()
                # Post-proses untuk memastikan ringkas
                if language == 'id':
                    result = _post_process_indonesian(result)
                return result
        except Exception as e:
            error_msg = str(e)
            # Jika model tidak ditemukan, coba model berikutnya
            if '404' in error_msg or 'not found' in error_msg.lower() or 'not supported' in error_msg.lower():
                continue
            elif '429' in error_msg or 'quota' in error_msg.lower() or 'rate limit' in error_msg.lower():
                # Kuota terlampaui - coba Groq sebagai gantinya
                print(f"Gemini quota exceeded, trying Groq...")
                return None
            else:
                # Error lain - coba model berikutnya
                continue
    
    return None


def _try_groq_extraction(review_text: str) -> str:
    """Try to extract key points using Groq API"""
    if not GROQ_API_KEY:
        return None
    
    try:
        from groq import Groq
        
        client = Groq(api_key=GROQ_API_KEY)
        
        # Deteksi bahasa
        language = _detect_language(review_text)
        
        # Coba model Groq berbeda (tercepat dulu)
        models_to_try = [
            'llama-3.1-8b-instant',  # Fast and efficient
            'llama-3.1-70b-versatile', # More capable
            'llama-3-8b-8192',        # Alternative
            'mixtral-8x7b-32768',     # Mixtral model
        ]
        
        # Buat prompt khusus bahasa (ditingkatkan untuk Bahasa Indonesia dengan sensitivitas lebih tinggi)
        if language == 'id':
            prompt = f"""Analisis review produk berikut dengan SENSITIVITAS SANGAT TINGGI terhadap nuansa bahasa Indonesia. Pahami konteks, ekspresi sehari-hari, pola kalimat, dan makna tersirat dengan sangat detail.

Teks review:
{review_text}

Instruksi analisis (SANGAT PENTING - baca dengan teliti):

1. Pahami konteks dan nuansa bahasa Indonesia dengan sangat detail:
   - Perhatikan ekspresi sehari-hari seperti "keren", "enak dimakan", "mantap", "banget", "produknya", "barangnya"
   - Deteksi makna tersirat dari kalimat pendek atau sederhana - jangan abaikan review singkat!
   - Pahami pola bahasa Indonesia: "produknya keren" = produk memiliki tampilan/desain yang menarik
   - Pahami bahwa "keren dan enak" menunjukkan kepuasan positif pada 2 aspek: tampilan DAN rasa
   - Perhatikan kombinasi kata yang menunjukkan sentimen (contoh: "keren dan enak dimakan" = positif kuat pada tampilan dan rasa)
   - Pahami bentuk posesif "-nya": "produknya keren" = "produk ini keren", "rasanya enak" = "rasa produk ini enak"
   - Deteksi aspek produk yang disebutkan: "keren" biasanya tentang tampilan/desain, "enak" tentang rasa/kualitas

2. Ekstrak poin penting dengan fokus SANGAT SPESIFIK:
   - Kekurangan atau kelebihan utama produk: sebutkan ASPEK SPESIFIK (rasa, tampilan, kualitas, harga, dll)
   - Fitur, kualitas, harga, atau aspek produk: ekstrak dari kata-kata yang digunakan
     * "keren" = tampilan/desain menarik
     * "enak" atau "enak dimakan" = rasa/kualitas baik
     * "keren dan enak" = tampilan menarik DAN rasa baik
   - Kesan keseluruhan pengguna: dari konteks dan kombinasi kata, bukan hanya kata kunci
   - Rekomendasi atau peringatan: jika tersirat dari sentimen positif/negatif
   - Masalah atau kelebihan yang menonjol: dari keseluruhan review

3. Format output (HARUS RINGKAS DAN SPESIFIK):
   - Berikan 3-5 poin penting yang paling relevan (jika review singkat, bisa 2-3 poin)
   - Maksimal 2 baris per poin (ringkas dan padat)
   - Gunakan bahasa Indonesia yang natural, seperti orang Indonesia berbicara sehari-hari
   - Hindari kalimat yang terlalu panjang atau bertele-tele
   - Hindari frasa generik seperti "Produk ini memiliki..." atau "Pengguna mengatakan..." atau "Review ini menunjukkan..."
   - Langsung ke poin: "Rasa enak dan tampilan menarik" bukan "Produk ini memiliki rasa yang enak dan tampilan yang menarik"
   - Jika review singkat, ekstrak makna tersirat dengan tepat, jangan hanya parafrase ulang

4. Sensitivitas khusus untuk review singkat:
   - Jika review "produknya keren dan enak dimakan":
     * Ekstrak: "Tampilan produk menarik (keren)" dan "Rasa produk enak dan layak dikonsumsi"
     * Jangan hanya: "Produk memiliki tampilan yang keren dan rasa yang enak dimakan" (terlalu literal)
   - Jika review "keren dan enak":
     * Ekstrak: "Tampilan menarik" dan "Rasa/kualitas baik"
   - Pahami bahwa review singkat pun bisa mengandung informasi penting - jangan abaikan!
   - Jangan membuat asumsi berlebihan, tapi juga jangan terlalu literal
   - Fokus pada apa yang BENAR-BENAR dikatakan atau tersirat, bukan template generik
   - Untuk setiap kata kunci, pahami aspek produk yang dimaksud:
     * "keren" = tampilan/desain/visual
     * "enak" = rasa/kualitas konsumsi
     * "bagus" = kualitas umum
     * "mantap" = kepuasan umum

5. Contoh ekstraksi yang benar:
   - Review: "produknya keren dan enak dimakan"
   - Output yang BENAR:
     • Tampilan produk menarik (keren)
     • Rasa produk enak dan layak dikonsumsi
     • Pengguna puas dengan aspek visual dan rasa produk
   - Output yang SALAH (terlalu generik - JANGAN GUNAKAN):
     • Produk ini memiliki tampilan yang keren
     • Produk ini memiliki rasa yang enak dimakan
     • Pengguna mengatakan bahwa produk ini keren dan enak dimakan
     • Kekurangan utama produk ini tidak disebutkan secara spesifik
     • Harga produk tidak disebutkan dalam review ini
     • Fitur produk tidak disebutkan secara rinci

6. PENTING - JANGAN LAKUKAN (SANGAT PENTING!):
   - JANGAN PERNAH menyebutkan hal-hal yang TIDAK disebutkan dalam review
   - JANGAN PERNAH menulis: "tidak disebutkan", "tidak ada informasi", "tidak spesifik", "belum disebutkan"
   - JANGAN PERNAH menggunakan template generik seperti:
     * "Produk ini memiliki..." → GANTI dengan: "Produk memiliki..." atau langsung "Rasa enak"
     * "Pengguna mengatakan..." → HAPUS, langsung ke poin
     * "Review ini menunjukkan..." → HAPUS, langsung ke poin
     * "Kekurangan atau kelebihan utama produk:" → HAPUS header ini
     * "Fitur dan kualitas:" → HAPUS header ini
     * "Kesan keseluruhan pengguna:" → HAPUS header ini
     * "Rekomendasi atau peringatan:" → HAPUS header ini
   - JANGAN membuat poin tentang informasi yang TIDAK ADA dalam review
   - HANYA ekstrak informasi yang BENAR-BENAR ada atau TERSIRAT dalam review
   - Jika review singkat, ekstrak apa yang ada, JANGAN membuat poin tentang apa yang tidak ada
   - JANGAN gunakan format dengan header seperti "**Kekurangan atau kelebihan utama**:"
   - LANGSUNG tulis poin tanpa pengantar apapun

7. FORMAT OUTPUT YANG BENAR:
   Untuk review "produknya keren dan enak dimakan", output yang BENAR:
   • Tampilan produk menarik (keren)
   • Rasa produk enak dan layak dikonsumsi
   • Pengguna puas dengan aspek visual dan rasa
   
   Output yang SALAH (JANGAN GUNAKAN):
   • Kekurangan atau kelebihan utama produk: Produk ini memiliki kelebihan utama pada desain yang keren
   • Fitur dan kualitas: Kualitas produk ini tidak disebutkan secara spesifik
   • Kesan keseluruhan pengguna: Pengguna merasa puas dengan produk ini
   • Rekomendasi atau peringatan: Produk ini direkomendasikan, tetapi kualitas tidak disebutkan

Jawab LANGSUNG dengan poin-poin penting, TANPA header apapun, TANPA pengantar, TANPA template. Gunakan format bullet point (•) untuk setiap poin. Fokus pada informasi SPESIFIK dan RELEVAN yang BENAR-BENAR ada dalam review. JANGAN menyebutkan apapun yang tidak ada dalam review."""
            system_prompt = "Anda adalah ahli analisis review produk yang SANGAT memahami nuansa bahasa Indonesia. Anda mampu menangkap makna tersirat, ekspresi sehari-hari, pola kalimat, dan konteks budaya Indonesia dengan sangat detail. PENTING SEKALI: HANYA ekstrak informasi yang BENAR-BENAR ada dalam review. JANGAN PERNAH membuat poin tentang hal-hal yang TIDAK disebutkan. JANGAN PERNAH menulis 'tidak disebutkan', 'tidak spesifik', 'tidak ada informasi'. JANGAN PERNAH gunakan template generik seperti 'Produk ini memiliki...', 'Pengguna mengatakan...', 'Kekurangan atau kelebihan utama produk:', 'Fitur dan kualitas:'. LANGSUNG tulis poin tanpa header atau pengantar. Untuk review 'produknya keren dan enak dimakan', langsung tulis: 'Tampilan produk menarik' dan 'Rasa produk enak', BUKAN 'Produk ini memiliki kelebihan utama pada desain yang keren' atau 'Kualitas tidak disebutkan secara spesifik'."
        else:
            prompt = f"""Analyze the following product review and extract the key points concisely.

Focus on:
- Main concerns or praises
- Specific features mentioned
- Overall impression
- Any recommendations or warnings

Review text:
{review_text}

Provide a concise summary of key points (3-5 points, max 2 lines per point). Be brief and relevant."""
            system_prompt = "You are a helpful assistant that extracts key points from product reviews. Be concise and relevant."
        
        for model_name in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                
                if response and response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        print(f"✓ Using Groq ({model_name}) for key points extraction")
                        result = content.strip()
                        # Post-proses untuk Bahasa Indonesia
                        if language == 'id':
                            result = _post_process_indonesian(result)
                        return result
            except Exception as e:
                error_msg = str(e)
                # Jika model tidak ditemukan atau kuota terlampaui, coba model berikutnya
                if '404' in error_msg or 'not found' in error_msg.lower():
                    continue
                elif '429' in error_msg or 'quota' in error_msg.lower() or 'rate limit' in error_msg.lower():
                    print(f"Groq quota exceeded for {model_name}, trying next model...")
                    continue
                else:
                    # Error lain - coba model berikutnya
                    continue
        
        return None
    except ImportError:
        print("Groq library not installed. Install with: pip install groq")
        return None
    except Exception as e:
        print(f"Error with Groq API: {str(e)[:100]}...")
        return None


def _post_process_indonesian(text: str) -> str:
    """
    Post-process Indonesian text to make it more concise and natural.
    Remove generic phrases, improve naturalness, and make it shorter.
    """
    # Hapus frasa generik umum (daftar diperluas untuk sensitivitas lebih baik)
    generic_phrases = [
        r'berikut adalah\s*:?',
        r'ini adalah\s*:?',
        r'poin-poin penting\s*:?',
        r'ringkasan\s*:?',
        r'kesimpulan\s*:?',
        r'secara umum\s*,?',
        r'pada dasarnya\s*,?',
        r'produk ini memiliki\s+',
        r'produk ini mempunyai\s+',
        r'produk memiliki\s+',
        r'produk mempunyai\s+',
        r'pengguna mengatakan\s+',
        r'pengguna menyebutkan\s+',
        r'pengguna mengungkapkan\s+',
        r'pengguna menulis\s+',
        r'pengguna menyatakan\s+',
        r'pengguna mengungkap\s+',
        r'review ini menunjukkan\s+',
        r'review ini mengindikasikan\s+',
        r'review menunjukkan\s+',
        r'review mengindikasikan\s+',
        r'dari review ini\s*,?\s*',
        r'dari review\s*,?\s*',
        r'berdasarkan review\s*,?\s*',
        r'berdasarkan review ini\s*,?\s*',
        r'dapat disimpulkan\s+',
        r'dapat dilihat\s+',
        r'dari analisis\s+',
        r'secara keseluruhan\s*,?\s*',
        r'pada review\s+',
        r'dalam review\s+',
        # Hapus frasa tentang informasi yang hilang
        r'tidak disebutkan\s+(secara\s+)?(spesifik|rinci|detail|eksplisit)',
        r'tidak disebutkan\s+dalam\s+review',
        r'tidak\s+(disebutkan|disebut|diketahui|diketahui|tersedia)',
        r'hanya saja\s*,?\s*',
        r'namun\s+,?\s*(tidak|belum|kurang)',
        r'perlu\s+(lebih|informasi|data|detail)',
        r'kurang\s+informasi',
        r'tidak\s+ada\s+informasi',
    ]
    
    for phrase in generic_phrases:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)
    
    # Tingkatkan naturalitas: hapus "yang" yang tidak perlu di beberapa konteks
    # Namun hati-hati - "yang" penting dalam Bahasa Indonesia, jadi hanya hapus kasus yang jelas
    text = re.sub(r'\s+yang\s+(memiliki|mempunyai|adalah)\s+', ' ', text, flags=re.IGNORECASE)
    
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Pecah menjadi baris dan proses masing-masing
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Lewati baris kosong
        if not line:
            continue
        
        # Lewati baris yang menyebut informasi hilang/tidak ditentukan (tidak berguna)
        missing_info_patterns = [
            r'tidak\s+(disebutkan|disebut|diketahui|tersedia|ada|spesifik|rinci|detail)',
            r'belum\s+(disebutkan|disebut|diketahui)',
            r'kurang\s+(informasi|data|detail|spesifik)',
            r'perlu\s+(lebih|informasi|data|detail)',
            r'hanya saja\s*,?\s*',
            r'namun\s+,?\s*(tidak|belum|kurang)',
            r'tidak\s+ada\s+informasi',
            r'tidak\s+tersedia\s+informasi',
            r'tidak\s+disebutkan\s+secara\s+(spesifik|rinci|detail)',
            r'kualitas\s+(produk\s+)?(ini\s+)?tidak\s+disebutkan',
            r'harga\s+(produk\s+)?(ini\s+)?tidak\s+disebutkan',
            r'kekurangan\s+(utama\s+)?(produk\s+)?(ini\s+)?tidak\s+disebutkan',
        ]
        
        # Periksa apakah baris tentang informasi yang hilang
        is_about_missing = any(re.search(pattern, line, re.IGNORECASE) for pattern in missing_info_patterns)
        if is_about_missing:
            continue  # Skip this line entirely
        
        # Hapus header gaya template (mis. "**Kekurangan dan kelebihan utama**:")
        # Ini terlalu generik dan tidak berguna
        line = re.sub(r'\*\*[^*]+\*\*\s*:?\s*', '', line)
        line = re.sub(r'^\*\s+', '', line)  # Remove leading asterisk if any
        
        # Hapus header template umum
        template_headers = [
            r'kekurangan\s+atau\s+kelebihan\s+utama\s*(produk)?\s*:?\s*',
            r'fitur\s+dan\s+kualitas\s*:?\s*',
            r'kesan\s+keseluruhan\s+(pengguna|user)\s*:?\s*',
            r'rekomendasi\s+atau\s+peringatan\s*:?\s*',
            r'key\s+points?\s*:?\s*',
            r'main\s+concerns?\s*:?\s*',
            r'specific\s+features?\s*:?\s*',
            r'overall\s+impression\s*:?\s*',
        ]
        for header in template_headers:
            line = re.sub(header, '', line, flags=re.IGNORECASE)
        
        # Hapus "Produk ini memiliki", "Pengguna mengatakan", dll.
        line = re.sub(r'produk\s+(ini\s+)?(memiliki|mempunyai)\s+', '', line, flags=re.IGNORECASE)
        line = re.sub(r'pengguna\s+(mengatakan|menyebutkan|mengungkapkan|menulis|menyatakan)\s+', '', line, flags=re.IGNORECASE)
        line = re.sub(r'review\s+(ini\s+)?(menunjukkan|mengindikasikan)\s+', '', line, flags=re.IGNORECASE)
        
        # Lewati baris yang hanya header tanpa konten
        if len(line.strip()) < 15 and (':' in line or line.endswith(':')):
            continue
        
        # Lewati baris yang dimulai dengan frasa template
        if re.match(r'^(produk\s+(ini\s+)?(memiliki|mempunyai)|pengguna\s+(mengatakan|menyebutkan)|review\s+(ini\s+)?(menunjukkan|mengindikasikan))', line, re.IGNORECASE):
            # Coba ekstrak konten berguna setelah template
            cleaned = re.sub(r'^(produk\s+(ini\s+)?(memiliki|mempunyai)|pengguna\s+(mengatakan|menyebutkan)|review\s+(ini\s+)?(menunjukkan|mengindikasikan))\s+', '', line, flags=re.IGNORECASE)
            if len(cleaned.strip()) > 10:
                line = cleaned.strip()
            else:
                continue  # Skip if nothing useful left
        
        # Hapus angka, strip, atau bullet di depan jika sudah diformat
        line = re.sub(r'^[\d\.\)\-\•\*]\s*', '', line)
        
        # Hapus titik di akhir jika baris terlalu pendek (kemungkinan header)
        if len(line) < 30 and line.endswith('.'):
            line = line[:-1]
        
        # Batasi setiap baris maksimum 120 karakter (ditingkatkan untuk keterbacaan lebih baik)
        if len(line) > 120:
            # Coba pisahkan di batas kalimat
            if '. ' in line:
                parts = line.split('. ')
                for part in parts:
                    part = part.strip()
                    if part and len(part) > 10:  # Only add meaningful parts
                        if not part.endswith('.'):
                            part += '.'
                        processed_lines.append(part)
            elif ', ' in line and len(line) > 150:
                # Coba pisahkan di koma untuk baris yang sangat panjang
                parts = line.split(', ')
                current_line = parts[0]
                for part in parts[1:]:
                    if len(current_line + ', ' + part) <= 120:
                        current_line += ', ' + part
                    else:
                        if current_line:
                            processed_lines.append(current_line)
                        current_line = part
                if current_line:
                    processed_lines.append(current_line)
            else:
                # Potong saja jika terlalu panjang dan tidak ada titik pisah yang baik
                processed_lines.append(line[:117] + '...')
        elif line:
            processed_lines.append(line)
    
    # Pastikan setiap baris dimulai dengan bullet jika belum diformat
    formatted_lines = []
    for line in processed_lines:
        line = line.strip()
        if line:
            # Jika baris tidak diawali bullet, tambahkan satu
            if not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                formatted_lines.append('• ' + line)
            else:
                formatted_lines.append(line)
    
    result = '\n'.join(formatted_lines)
    
    # Bersihkan akhir: hapus bullet duplikat
    result = re.sub(r'•\s*•\s*', '• ', result)
    
    return result


def _simple_key_points_extraction(review_text: str) -> str:
    """
    Simple key points extraction as fallback when AI APIs are not available.
    Uses basic text analysis to extract key points.
    Supports both Indonesian and English.
    """
    # Deteksi bahasa
    language = _detect_language(review_text)
    
    # Pecah menjadi kalimat
    sentences = re.split(r'[.!?]+', review_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if not sentences:
        if language == 'id':
            return "• Teks review terlalu pendek untuk mengekstrak poin penting"
        return "• Review text is too short to extract key points"
    
    # Kata kunci khusus bahasa (diperluas untuk Bahasa Indonesia)
    if language == 'id':
        important_keywords = {
            'positive': [
                'bagus', 'mantap', 'keren', 'puas', 'sangat bagus', 'sangat baik', 'sangat puas',
                'sempurna', 'luar biasa', 'memuaskan', 'sangat memuaskan', 'terbaik',
                'paling bagus', 'paling baik', 'recommended', 'rekomendasi', 'direkomendasikan',
                'sangat direkomendasikan', 'worth it', 'sangat worth it', 'worth every penny',
                'suka banget', 'love it', 'sangat suka', 'sangat senang', 'terkesan',
                'impressed', 'excellent', 'amazing', 'fantastic', 'wonderful', 'outstanding'
            ],
            'negative': [
                'jelek', 'buruk', 'kecewa', 'sangat kecewa', 'tidak puas', 'tidak memuaskan',
                'mengecewakan', 'sangat mengecewakan', 'gagal', 'sangat gagal', 'gagal total',
                'rusak', 'cacat', 'tidak sesuai', 'tidak cocok', 'tidak worth it',
                'tidak direkomendasikan', 'terburuk', 'paling jelek', 'paling buruk',
                'waste of money', 'buang uang', 'rugi', 'sangat rugi', 'terrible', 'awful',
                'horrible', 'worst', 'disappointed', 'very disappointed', 'masalah', 'ada masalah',
                'banyak masalah', 'sering masalah', 'kurang baik', 'kurang bagus'
            ],
            'recommendation': [
                'rekomendasi', 'direkomendasikan', 'sangat direkomendasikan', 'sarankan',
                'sebaiknya', 'harus', 'disarankan', 'recommend', 'highly recommend',
                'suggest', 'should', 'must', 'advise', 'worth it', 'worth buying'
            ],
            'features': [
                'kualitas', 'harga', 'pengiriman', 'pelayanan', 'customer service', 'fitur',
                'desain', 'performa', 'performance', 'nilai', 'value', 'barang', 'produk',
                'packaging', 'kemasan', 'ukuran', 'size', 'warna', 'color', 'material',
                'bahan', 'durability', 'ketahanan', 'warranty', 'garansi', 'return',
                'pengembalian', 'refund', 'pengembalian dana'
            ]
        }
    else:
        important_keywords = {
            'positive': ['excellent', 'great', 'good', 'amazing', 'wonderful', 'love', 'perfect', 'fantastic', 'awesome', 'outstanding'],
            'negative': ['bad', 'terrible', 'awful', 'disappointed', 'hate', 'worst', 'poor', 'horrible', 'waste'],
            'recommendation': ['recommend', 'suggest', 'should', 'must', 'advise', 'highly recommend'],
            'features': ['quality', 'price', 'delivery', 'shipping', 'customer service', 'feature', 'design', 'performance', 'value']
        }
    
    # Beri skor kalimat berdasarkan kepentingan
    scored_sentences = []
    for sentence in sentences[:15]:  # Check first 15 sentences
        score = 0
        lower_sentence = sentence.lower()
        
        # Periksa kata kunci
        for category, keywords in important_keywords.items():
            for keyword in keywords:
                if keyword in lower_sentence:
                    score += 2 if category in ['positive', 'negative', 'recommendation'] else 1
                    break
        
        # Bonus untuk kalimat lebih panjang (biasanya lebih informatif)
        if len(sentence) > 50:
            score += 1
        
        scored_sentences.append((score, sentence))
    
    # Urutkan berdasarkan skor (tertinggi dulu)
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    
    # Pilih 5 kalimat teratas
    selected = [sentence for _, sentence in scored_sentences[:5] if sentence]
    
    # Jika tidak ada kalimat skor tinggi, gunakan beberapa kalimat bermakna pertama
    if not selected:
        selected = sentences[:3]
    
    # Format sebagai poin bullet
    formatted_points = []
    for point in selected:
        # Bersihkan poin
        point = point.strip()
        # Hapus strip atau bullet di depan jika ada
        point = re.sub(r'^[-•]\s*', '', point)
        # Potong jika terlalu panjang (maks 100 karakter)
        if len(point) > 100:
            point = point[:97] + '...'
        if point:
            formatted_points.append(f"• {point}")
    
    if formatted_points:
        result = '\n'.join(formatted_points)
        if language == 'id':
            result = _post_process_indonesian(result)
        return result
    else:
        # Cadangan terakhir
        truncated = review_text[:200] + '...' if len(review_text) > 200 else review_text
        return f"• {truncated}"
