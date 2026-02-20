import os

import google.generativeai as genai
from dotenv import load_dotenv

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout)

    # .envからキーを読み込む
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        logging.error("❌ エラー: .envファイルに GOOGLE_API_KEY が見つかりません。")
        return 1
    else:
        logging.info(f"🔑 APIキーを確認中... (末尾: {api_key[-4:]})")

        # Googleへの接続設定
        genai.configure(api_key=api_key)

        logging.info("\n📡 Googleに問い合わせています... あなたのキーで使えるモデル一覧はこちら：")
        logging.info("-" * 50)
        
        try:
            found = False
            # 利用可能なモデルを全部リストアップする
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    logging.info(f"✅ {m.name}")
                    found = True
            
            if not found:
                logging.warning("⚠️ 利用可能なモデルが1つも見つかりませんでした。")
                logging.warning("👉 原因：APIキーが「古いプロジェクト」のものか、課金設定などの問題の可能性があります。")

        except Exception as e:
            logging.error(f"❌ 接続エラーが発生しました: {type(e).__name__}")
            logging.error("-" * 50)
            logging.error("👉 このエラーが出る場合、APIキー自体が無効か、プロジェクト設定が間違っています。")
            return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
