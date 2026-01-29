import os
import yfinance as yf
from datetime import datetime
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# 1. パスワード読み込み
load_dotenv()

# CrewAIがGeminiを使うための設定
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 2. 為替データの取得
print("--- データを取得中... ---")
try:
    ticker = "JPY=X"
    data = yf.Ticker(ticker)
    price = data.history(period="1d")['Close'].iloc[-1]
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"💰 現在のレート: {price:.2f} 円 ({date_str})")
except Exception as e:
    print(f"データ取得エラー: {e}")
    price = 150.00
    date_str = datetime.now().strftime("%Y-%m-%d")

# 3. エージェント作成
# 【修正】リストにあった「gemini-flash-latest」（安定版）を指定します
analyst = Agent(
    role='FX専属アナリスト',
    goal='現在のレートに基づき、日本の投資家向けに市況レポートを書く',
    backstory='あなたは金融市場で長年の経験を持つプロのアナリストです。',
    verbose=True,
    llm="gemini/gemini-flash-latest"
)

# 4. タスク作成
report_task = Task(
    description=f'現在のドル円レートは【{price:.2f} 円】です。この価格について、投資家へのアドバイスを含む3行程度のレポートを日本語で作成してください。',
    expected_output='日本語の市況レポート',
    agent=analyst
)

# 5. 実行
print("--- 🤖 Gemini (Flash Latest) が分析レポートを作成中... ---")
crew = Crew(
    agents=[analyst],
    tasks=[report_task],
    verbose=True
)

result = crew.kickoff()

# 6. 保存
with open("report.md", "w", encoding="utf-8") as f:
    f.write(f"# 🏦 FXレポート\n\n{result}")

print("\n✅ レポート完成！ 'report.md' を確認してください。")