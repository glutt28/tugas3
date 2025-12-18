"""
Check available Gemini models for your API key
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def check_available_models():
    """List all available Gemini models"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("✗ GEMINI_API_KEY not found in .env file")
        print("\nPlease add GEMINI_API_KEY to your .env file")
        return
    
    try:
        genai.configure(api_key=api_key)
        print("✓ API Key configured")
        print("\nChecking available models...")
        print("=" * 60)
        
        available_models = []
        all_models = genai.list_models()
        
        for model in all_models:
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name.replace('models/', '')
                available_models.append(model_name)
                print(f"✓ {model_name}")
        
        if not available_models:
            print("✗ No models with generateContent support found")
            print("\nPossible issues:")
            print("1. API key may not have access to Gemini models")
            print("2. API key may be invalid")
            print("3. Check API key permissions in Google AI Studio")
        else:
            print("\n" + "=" * 60)
            print(f"Found {len(available_models)} available model(s)")
            print("\nRecommended model to use:")
            if 'gemini-1.5-flash' in available_models:
                print("  → gemini-1.5-flash (fast and efficient)")
            elif 'gemini-1.5-pro' in available_models:
                print("  → gemini-1.5-pro (more capable)")
            elif 'gemini-pro' in available_models:
                print("  → gemini-pro (legacy)")
            else:
                print(f"  → {available_models[0]} (first available)")
            
            print("\nUpdate key_points_extractor.py to use one of these models")
        
        return available_models
        
    except Exception as e:
        print(f"✗ Error checking models: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. Network connection problem")
        print("3. API service unavailable")
        return None

if __name__ == "__main__":
    check_available_models()

