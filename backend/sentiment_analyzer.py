from transformers import pipeline
import torch
import re

# Inisialisasi pipeline analisis sentimen
# Menggunakan model ringan untuk kinerja lebih baik
sentiment_pipeline = None

def get_sentiment_analyzer():
    global sentiment_pipeline
    if sentiment_pipeline is None:
        # Menggunakan model analisis sentimen pra-latih
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
    return sentiment_pipeline

def _detect_language(text: str) -> str:
    """Detect if text is in Indonesian or English - improved sensitivity with more patterns"""
    indonesian_indicators = [
        # Kata umum
        'yang', 'dan', 'atau', 'dengan', 'untuk', 'dari', 'ini', 'itu', 'sangat', 'sekali',
        # Kata-kata sentimen
        'bagus', 'jelek', 'buruk', 'mantap', 'keren', 'puas', 'kecewa', 'mengecewakan',
        # Terkait produk
        'produk', 'barang', 'kualitas', 'harga', 'pelayanan', 'pengiriman', 'rekomendasi',
        # Kata ganti dan kata umum
        'saya', 'kami', 'mereka', 'anda', 'sudah', 'belum', 'akan', 'tidak', 'bukan',
        # Partikel dan ekspresi umum
        'jadi', 'juga', 'saja', 'sih', 'nih', 'dong', 'lah', 'kan', 'ya', 'gak', 'ga',
        # Penguat (intensifier)
        'sangat', 'banget', 'sekali', 'amat', 'terlalu', 'cukup', 'lumayan', 'agak',
        # Kata-kata kepuasan
        'memuaskan', 'mengecewakan', 'direkomendasikan', 'tidak direkomendasikan',
        # Spesifik makanan/produk
        'enak', 'enak dimakan', 'lezat', 'nikmat', 'sedap', 'gurih', 'rasanya',
        # Penampilan
        'cantik', 'menarik', 'indah', 'rapi', 'bersih', 'tampilannya', 'tampilan',
        # Frasa umum
        'keren dan', 'bagus dan', 'enak dan', 'keren enak', 'bagus enak',
        # Kata-kata khusus Bahasa Indonesia lainnya
        'produknya', 'barangnya', 'rasanya', 'tampilannya', 'kualitasnya', 'harganya',
        'pelayanannya', 'pengirimannya', 'kemasannya', 'packagingnya',
        # Bentuk kepemilikan Bahasa Indonesia
        'nya', 'ku', 'mu', 'kita', 'kalian',
        # Ekspresi Bahasa Indonesia umum lainnya
        'si', 'sih', 'dong', 'deh', 'kok', 'loh', 'dah', 'nih', 'tuh',
        # Kata sambung Bahasa Indonesia
        'tapi', 'tetapi', 'namun', 'meskipun', 'walaupun', 'karena', 'sehingga',
        # Penanda waktu/tense Bahasa Indonesia
        'sudah', 'belum', 'akan', 'sedang', 'telah', 'pernah', 'selalu', 'kadang',
        # Kata tanya Bahasa Indonesia
        'apa', 'siapa', 'kapan', 'dimana', 'kenapa', 'mengapa', 'bagaimana',
        # Kata tunjuk Bahasa Indonesia
        'ini', 'itu', 'sini', 'situ', 'sana',
        # Preposisi Bahasa Indonesia
        'di', 'ke', 'dari', 'pada', 'dengan', 'untuk', 'oleh', 'kepada', 'terhadap'
    ]
    
    text_lower = text.lower()
    indonesian_count = sum(1 for word in indonesian_indicators if word in text_lower)
    
    # Juga periksa pola khusus Bahasa Indonesia (diperluas)
    indonesian_patterns = [
        # Pola makanan/rasa
        r'\b(enak|lezat|nikmat|sedap|gurih)\s+(dimakan|rasanya|banget|sekali|sangat)',
        r'\b(rasa|rasanya)\s+(enak|lezat|nikmat|sedap|gurih)',
        # Pola penampilan
        r'\b(keren|bagus|mantap|cantik|menarik)\s+(dan|enak|banget|sekali|sangat)',
        r'\b(tampilan|tampilannya)\s+(keren|bagus|cantik|menarik|rapi)',
        # Pola penguat (intensifier)
        r'\b(sangat|banget|amat|terlalu)\s+(enak|lezat|keren|bagus|mantap|puas)',
        r'\b(enak|keren|bagus|mantap)\s+(banget|sekali|sangat|amat)',
        # Pola kepemilikan (sangat khas Bahasa Indonesia)
        r'\b(produk|barang|kualitas|harga|pelayanan|pengiriman|kemasan|packaging)nya\s+',
        r'\b(rasa|tampilan|kualitas|harga)nya\s+',
        # Pola frasa umum Bahasa Indonesia
        r'\b(keren|bagus|mantap)\s+dan\s+(enak|lezat|bagus|keren)',
        r'\b(enak|lezat)\s+dan\s+(keren|bagus|mantap)',
        r'\b(produknya|barangnya)\s+(keren|bagus|enak|mantap)',
        # Pola negasi
        r'\b(tidak|belum|bukan|kurang)\s+(bagus|baik|puas|memuaskan|enak|keren)',
        # Pola rekomendasi
        r'\b(direkomendasikan|rekomendasi|sarankan|disarankan)\s+(untuk|bagi|kepada)',
    ]
    
    pattern_matches = sum(1 for pattern in indonesian_patterns if re.search(pattern, text_lower))
    
    # Periksa pola urutan kata Bahasa Indonesia (subjek-kata kerja-objek yang khas)
    # Bahasa Indonesia sering menggunakan "produknya keren" vs Bahasa Inggris "the product is cool"
    indonesian_word_order_patterns = [
        r'\b\w+nya\s+(keren|bagus|enak|mantap|jelek|buruk)',  # "produknya keren"
        r'\b\w+nya\s+dan\s+\w+',  # "produknya keren dan enak"
    ]
    
    word_order_matches = sum(1 for pattern in indonesian_word_order_patterns if re.search(pattern, text_lower))
    
    # Jika ditemukan indikator/pola/urutan kata khas Indonesia, kemungkinan bahasa adalah Indonesia
    # Turunkan ambang lagi untuk mendeteksi ulasan pendek dengan lebih baik
    if indonesian_count >= 1 or pattern_matches >= 1 or word_order_matches >= 1:
        return 'id'
    return 'en'

def _analyze_sentiment_indonesian(text: str) -> str:
    """
    Rule-based sentiment analysis specifically for Indonesian text.
    More accurate for Indonesian reviews.
    """
    text_lower = text.lower()
    
    # Indikator positif kuat (Bahasa Indonesia) - diperluas dengan ekspresi yang lebih nuansa
    strong_positive = [
        'sangat bagus', 'sangat baik', 'sangat puas', 'sangat memuaskan', 'sangat direkomendasikan',
        'luar biasa', 'sempurna', 'mantap banget', 'keren banget', 'bagus banget',
        'sangat suka', 'sangat senang', 'sangat terkesan', 'sangat impressed',
        'worth it', 'worth every penny', 'sangat worth it', 'sangat worth',
        'terbaik', 'paling bagus', 'paling baik', 'paling puas',
        'excellent', 'amazing', 'fantastic', 'wonderful', 'outstanding',
        'recommended', 'sangat recommended', 'highly recommended', 'sangat direkomendasikan',
        'love it', 'suka banget', 'cinta banget', 'fall in love',
        # Ekspresi gabungan positif (umum di Indonesia) - diperluas
        'keren dan enak', 'bagus dan enak', 'keren dan bagus', 'enak dan keren',
        'keren enak', 'bagus enak', 'mantap enak', 'enak mantap',
        'sangat enak', 'enak banget', 'sangat lezat', 'lezat banget',
        'sangat menarik', 'menarik banget', 'cantik banget', 'sangat cantik',
        # Kombinasi kepuasan kuat
        'puas banget', 'sangat cocok', 'cocok banget', 'sangat sesuai', 'sesuai banget',
        # Kepemilikan + positif (pola khas Indonesia: "produknya keren")
        'produknya keren', 'produknya bagus', 'produknya enak', 'produknya mantap',
        'barangnya keren', 'barangnya bagus', 'barangnya enak', 'barangnya mantap',
        'rasanya enak', 'rasanya lezat', 'rasanya nikmat', 'rasanya sedap',
        'tampilannya keren', 'tampilannya bagus', 'tampilannya cantik', 'tampilannya menarik',
        'kualitasnya bagus', 'kualitasnya baik', 'kualitasnya memuaskan',
        'harganya worth', 'harganya sesuai', 'harganya pas',
        # Ekspresi positif spesifik makanan
        'enak dimakan', 'lezat dimakan', 'nikmat dimakan', 'sedap dimakan',
        'enak banget dimakan', 'lezat banget dimakan', 'sangat enak dimakan',
        # Pola gabungan lainnya - kecocokan PERSIS untuk frasa umum Indonesia
        'keren dan enak dimakan', 'bagus dan enak dimakan', 'keren enak dimakan',
        'produknya keren dan enak', 'produknya bagus dan enak', 'produknya keren enak',
        'produknya keren dan enak dimakan', 'barangnya keren dan enak dimakan',
        # Pola eksak tambahan
        'produknya keren dan enak', 'barangnya keren dan enak',
        'keren dan enak', 'bagus dan enak', 'mantap dan enak'
    ]
    
    # Indikator positif sedang (diperluas dengan ekspresi Bahasa Indonesia)
    moderate_positive = [
        'bagus', 'baik', 'puas', 'memuaskan', 'oke', 'ok', 'lumayan', 'cukup baik',
        'keren', 'mantap', 'nice', 'good', 'great', 'fine', 'decent',
        'rekomendasi', 'direkomendasikan', 'recommend', 'suggest',
        'senang', 'suka', 'terkesan', 'impressed', 'satisfied',
        # Food/product specific positive expressions - expanded
        'enak', 'enak dimakan', 'enak banget', 'rasanya enak', 'rasa enak',
        'lezat', 'nikmat', 'sedap', 'gurih', 'manis',
        # Visual/appearance positive - expanded
        'cantik', 'menarik', 'indah', 'rapi', 'bersih', 'bagus tampilannya',
        # General satisfaction
        'cocok', 'sesuai', 'pas', 'tepat', 'benar', 'tepat sasaran',
        # Possessive forms (moderate positive)
        'produknya', 'barangnya', 'kualitasnya', 'harganya', 'pelayanannya',
        # Simple combinations (moderate)
        'keren dan', 'bagus dan', 'enak dan', 'mantap dan',
        # Short positive expressions
        'keren', 'enak', 'bagus', 'mantap'  # Standalone can be positive
    ]
    
    # Indikator negatif kuat
    strong_negative = [
        'sangat jelek', 'sangat buruk', 'sangat kecewa', 'sangat mengecewakan',
        'sangat tidak puas', 'sangat tidak memuaskan', 'sangat tidak direkomendasikan',
        'sangat tidak sesuai', 'sangat tidak cocok', 'sangat tidak worth it',
        'terburuk', 'paling jelek', 'paling buruk', 'paling kecewa',
        'gagal total', 'sangat gagal', 'sangat rusak', 'sangat cacat',
        'waste of money', 'buang uang', 'rugi', 'sangat rugi',
        'terrible', 'awful', 'horrible', 'worst', 'disappointed', 'very disappointed'
    ]
    
    # Indikator negatif sedang
    moderate_negative = [
        'jelek', 'buruk', 'kecewa', 'mengecewakan', 'tidak puas', 'tidak memuaskan',
        'tidak sesuai', 'tidak cocok', 'tidak worth it', 'tidak direkomendasikan',
        'gagal', 'rusak', 'cacat', 'kurang baik', 'kurang bagus', 'kurang memuaskan',
        'bad', 'poor', 'disappointed', 'unsatisfied', 'not good', 'not worth',
        'masalah', 'ada masalah', 'banyak masalah', 'sering masalah'
    ]
    
    # Hitung kemunculan - gunakan pencocokan fleksibel untuk frasa Bahasa Indonesia
    # Untuk frasa multi-kata, gunakan pencarian substring (lebih fleksibel untuk Bahasa Indonesia)
    strong_pos_count = 0
    for phrase in strong_positive:
        if len(phrase.split()) > 1:
            # Frasa multi-kata: gunakan pencocokan substring (lebih fleksibel)
            # Ini menangkap contoh seperti "produknya keren dan enak dimakan"
            if phrase in text_lower:
                strong_pos_count += 1
        else:
            # Kata tunggal: gunakan batas kata
            if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower):
                strong_pos_count += 1
    
    moderate_pos_count = 0
    for phrase in moderate_positive:
        if len(phrase.split()) > 1:
            if phrase in text_lower:
                moderate_pos_count += 1
        else:
            if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower):
                moderate_pos_count += 1
    
    strong_neg_count = sum(1 for phrase in strong_negative if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower))
    moderate_neg_count = sum(1 for phrase in moderate_negative if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower))
    
    # Juga periksa pola khusus Bahasa Indonesia yang mengindikasikan sentimen positif
    # Pola: "produknya keren dan enak dimakan" - harus memberikan skor tinggi
    indonesian_positive_patterns = [
        r'produknya\s+(keren|bagus|enak|mantap)',
        r'barangnya\s+(keren|bagus|enak|mantap)',
        r'(keren|bagus|mantap)\s+dan\s+(enak|lezat)',
        r'(enak|lezat)\s+(dimakan|rasanya|banget)',
        r'(keren|bagus|mantap)\s+(enak|lezat)\s+dimakan',
        r'produknya\s+(keren|bagus)\s+dan\s+enak',
        # More specific patterns for common combinations
        r'produknya\s+(keren|bagus|mantap)\s+dan\s+(enak|lezat)\s+dimakan',
        r'produknya\s+(keren|bagus|mantap)\s+dan\s+(enak|lezat)',
        r'barangnya\s+(keren|bagus|mantap)\s+dan\s+(enak|lezat)',
        # Pattern for "keren dan enak" anywhere in text
        r'(keren|bagus|mantap)\s+dan\s+(enak|lezat)\s+dimakan',
        r'(keren|bagus|mantap)\s+dan\s+(enak|lezat)',
    ]
    
    pattern_pos_count = sum(1 for pattern in indonesian_positive_patterns if re.search(pattern, text_lower))
    
    # Juga periksa jika teks mengandung banyak kata positif (meskipun tidak persis dalam pola)
    # Ini membantu menangkap kasus seperti "produknya keren dan enak dimakan"
    individual_positive_words = ['keren', 'enak', 'bagus', 'mantap', 'lezat', 'nikmat', 'sedap', 'gurih']
    positive_word_count = sum(1 for word in individual_positive_words if re.search(r'\b' + word + r'\b', text_lower))
    
    # Pemeriksaan khusus: jika teks mengandung "produknya" atau "barangnya" + kata positif, besar kemungkinan positif
    has_possessive = bool(re.search(r'\b(produknya|barangnya|rasanya|tampilannya)\b', text_lower))
    if has_possessive and positive_word_count >= 1:
        pattern_pos_count += 2  # Bonus kuat untuk kepemilikan + kata positif
    
    # Jika terdapat 2+ kata positif, kemungkinan besar positif (terutama untuk ulasan pendek)
    if positive_word_count >= 2:
        pattern_pos_count += 2  # Bonus meningkat untuk banyak kata positif
    elif positive_word_count >= 1 and len(text_lower.split()) <= 15:
        # Untuk ulasan pendek, bahkan 1 kata positif dengan pola kemungkinan besar positif
        if pattern_pos_count > 0:
            pattern_pos_count += 1
    
    # Hitung skor (indikator kuat diberi bobot lebih, pola menambah bonus)
    positive_score = (strong_pos_count * 3) + moderate_pos_count + (pattern_pos_count * 3)  # Increased pattern weight
    negative_score = (strong_neg_count * 3) + moderate_neg_count
    
    # Periksa pola negasi (Bahasa Indonesia)
    negation_patterns = [
        r'tidak\s+(bagus|baik|puas|memuaskan|direkomendasikan|worth|suka|senang)',
        r'belum\s+(bagus|baik|puas|memuaskan)',
        r'bukan\s+(bagus|baik|puas|memuaskan)',
        r'kurang\s+(bagus|baik|puas|memuaskan)',
        r'tidak\s+(jelek|buruk|kecewa|mengecewakan)',
    ]
    
    # Jika ditemukan negasi, sesuaikan skor
    for pattern in negation_patterns:
        if re.search(pattern, text_lower):
            # Jika membalikkan positif, tingkatkan skor negatif
            if 'bagus' in pattern or 'baik' in pattern or 'puas' in pattern:
                negative_score += 2
            # Jika membalikkan negatif, tingkatkan skor positif
            elif 'jelek' in pattern or 'buruk' in pattern or 'kecewa' in pattern:
                positive_score += 2
    
    # Tentukan sentimen (logika diperbaiki untuk kepekaan yang lebih baik terhadap Bahasa Indonesia)
    # Untuk Bahasa Indonesia, sangat peka terhadap indikator positif, terutama pada ulasan pendek
    
    # PRIORITAS 1: Kasus khusus untuk pola Bahasa Indonesia - jika cocok pola, sangat besar kemungkinannya positif
    if pattern_pos_count > 0:
        # Jika terdapat pola positif jelas dan tidak ada negatif kuat, pasti positif
        if negative_score == 0 or positive_score >= negative_score:
            return 'positive'
        # Bahkan dengan beberapa negatif, jika pola kuat tetap positif
        if pattern_pos_count >= 2:
            return 'positive'
    
    # PRIORITAS 2: Banyak kata positif (terutama dengan bentuk kepemilikan)
    if positive_word_count >= 2:
        # Dua atau lebih kata positif = pasti positif (kecuali ada negatif kuat)
        if negative_score == 0 or (positive_score >= negative_score and strong_neg_count == 0):
            return 'positive'
    
    # PRIORITAS 3: Kepemilikan + kata positif (pola yang sangat umum di Indonesia)
    if has_possessive and positive_word_count >= 1 and negative_score == 0:
        return 'positive'
    
    # PRIORITAS 4: Logika pemeringkatan standar
    if positive_score > negative_score:
        # Meskipun skornya rendah, jika lebih tinggi dari negatif, maka positif
        if positive_score >= 1:
            return 'positive'
        # Untuk ulasan sangat pendek dengan indikator positif, anggap positif
        elif len(text_lower.split()) <= 15 and (strong_pos_count > 0 or moderate_pos_count > 0 or pattern_pos_count > 0):
            return 'positive'
    elif negative_score > positive_score:
        if negative_score >= 1:
            return 'negative'
        # Untuk ulasan sangat pendek dengan indikator negatif, anggap negatif
        elif len(text_lower.split()) <= 15 and (strong_neg_count > 0 or moderate_neg_count > 0):
            return 'negative'
    
    # PRIORITAS 5: Fallback - periksa adanya indikator apapun
    if strong_pos_count > 0 or pattern_pos_count > 0 or (moderate_pos_count >= 2):
        return 'positive'
    elif moderate_pos_count >= 1 and negative_score == 0:
        # Satu kata positif tanpa negatif = positif (untuk ulasan pendek)
        if len(text_lower.split()) <= 15:
            return 'positive'
    elif strong_neg_count > 0 or moderate_neg_count >= 2:
        return 'negative'
    else:
        return 'neutral'

def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of the review text.
    Uses ML model first, then falls back to rule-based analysis for Indonesian.
    Returns: 'positive', 'negative', or 'neutral'
    """
    # Detect language
    language = _detect_language(text)
    
    # Untuk Bahasa Indonesia, gunakan pendekatan hibrida: model ML + berbasis aturan
    if language == 'id':
        # Pertama coba berbasis aturan (lebih akurat untuk Bahasa Indonesia)
        rule_based_result = _analyze_sentiment_indonesian(text)
        
        # Juga coba model ML
        try:
            analyzer = get_sentiment_analyzer()
            ml_result = analyzer(text)[0]
            
            label = ml_result['label'].upper()
            score = ml_result['score']
            
            # Map ML result
            ml_sentiment = 'neutral'
            if 'LABEL_2' in label or 'POSITIVE' in label or 'POS' in label:
                ml_sentiment = 'positive'
            elif 'LABEL_0' in label or 'NEGATIVE' in label or 'NEG' in label:
                ml_sentiment = 'negative'
            
            # Jika kepercayaan ML tinggi (score > 0.7), utamakan hasilnya
            # Jika tidak, utamakan metode berbasis aturan untuk Bahasa Indonesia
            if score > 0.7:
                # Hasil ML dengan kepercayaan tinggi
                if ml_sentiment == rule_based_result:
                    return ml_sentiment
                # Jika keduanya berbeda, gunakan berbasis aturan (lebih akurat untuk Bahasa Indonesia)
                return rule_based_result
            else:
                # ML dengan kepercayaan rendah, utamakan berbasis aturan
                return rule_based_result
        except Exception as e:
            print(f"ML sentiment analysis error: {e}, using rule-based")
            return rule_based_result
    
    # Untuk Bahasa Inggris, gunakan model ML
    try:
        analyzer = get_sentiment_analyzer()
        result = analyzer(text)[0]
        
        label = result['label'].upper()
        score = result['score']
        
        # Model cardiffnlp menggunakan LABEL_0 (negatif), LABEL_1 (netral), LABEL_2 (positif)
        if 'LABEL_2' in label or 'POSITIVE' in label or 'POS' in label:
            return 'positive'
        elif 'LABEL_0' in label or 'NEGATIVE' in label or 'NEG' in label:
            return 'negative'
        elif 'LABEL_1' in label or 'NEUTRAL' in label:
            return 'neutral'
        else:
            # Cadangan: gunakan skor untuk menentukan sentimen
            if score < 0.5:
                return 'neutral'
            label_lower = label.lower()
            if 'positive' in label_lower or 'pos' in label_lower:
                return 'positive'
            elif 'negative' in label_lower or 'neg' in label_lower:
                return 'negative'
            else:
                return 'neutral'
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        # Cadangan: kembali ke metode berbasis aturan bahkan untuk bahasa Inggris
        return _analyze_sentiment_indonesian(text)

