"""
Test Gemini API quota status
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_quota():
    """Test if Gemini API is available and quota is not exceeded"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("✗ GEMINI_API_KEY not found in .env file")
        return False
    
    try:
        genai.configure(api_key=api_key)
        
        # Coba gunakan model dengan pengujian sederhana
        print("Testing Gemini API quota...")
        print("=" * 60)
        
        models_to_test = [
            'gemini-2.5-flash',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
        ]
        
        for model_name in models_to_test:
            try:
                print(f"\nTesting {model_name}...", end=" ")
                model = genai.GenerativeModel(model_name)
                
                # Permintaan pengujian sederhana
                response = model.generate_content("Say 'OK' if you can read this.")
                
                if response and response.text:
                    print("✓ SUCCESS - Quota available!")
                    print(f"  Response: {response.text.strip()}")
                    print(f"\n✓ {model_name} is working and quota is available")
                    return True
                    
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'quota' in error_msg.lower():
                    print(f"✗ Quota exceeded")
                    print(f"  Error: {error_msg[:100]}...")
                    continue
                elif '404' in error_msg or 'not found' in error_msg.lower():
                    print(f"✗ Model not found")
                    continue
                else:
                    print(f"✗ Error: {error_msg[:100]}...")
                    continue
        
        print("\n" + "=" * 60)
        print("✗ All models tested - quota may be exceeded or models unavailable")
        print("\nAplikasi akan menggunakan simple extraction sebagai fallback")
        return False
        
    except Exception as e:
        print(f"✗ Error testing Gemini: {e}")
        return False

if __name__ == "__main__":
    result = test_gemini_quota()
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Gemini API is available and working!")
        print("   Aplikasi akan menggunakan Gemini untuk key points extraction")
    else:
        print("\n" + "=" * 60)
        print("⚠️  Gemini API quota exceeded or unavailable")
        print("   Aplikasi akan menggunakan simple extraction (tetap berfungsi)")

