import google.generativeai as genai
import os
from dotenv import load_dotenv

# .envからキーを読み込む
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ エラー: .envファイルに GOOGLE_API_KEY が見つかりません。")
else:
    print(f"🔑 APIキーを確認中... (末尾: {api_key[-4:]})")
    
    # Googleへの接続設定
    genai.configure(api_key=api_key)

    print("\n📡 Googleに問い合わせています... あなたのキーで使えるモデル一覧はこちら：")
    print("-" * 50)
    
    try:
        found = False
        # 利用可能なモデルを全部リストアップする
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                found = True
        
        if not found:
            print("⚠️ 利用可能なモデルが1つも見つかりませんでした。")
            print("👉 原因：APIキーが「古いプロジェクト」のものか、課金設定などの問題の可能性があります。")
            
    except Exception as e:
        print(f"❌ 接続エラーが発生しました:\n{e}")
        print("-" * 50)
        print("👉 このエラーが出る場合、APIキー自体が無効か、プロジェクト設定が間違っています。")