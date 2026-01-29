import os
import yfinance as yf
from datetime import datetime
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# 1. 設定読み込み
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 2. 【強化版】データの取得（過去5日分を取得してトレンドを見させる）
print("--- 📊 市場データを取得中... ---")
try:
    ticker = "JPY=X"
    data = yf.Ticker(ticker)
    # 過去5日分のデータを取得
    hist = data.history(period="5d")
    
    # AIに渡すためのデータテキストを作成
    latest = hist.iloc[-1]
    last_close = hist.iloc[-2]['Close'] # 前日終値
    change = latest['Close'] - last_close # 前日比
    
    market_data = f"""
    【対象通貨ペア】USD/JPY (ドル円)
    【現在日時】{datetime.now().strftime("%Y-%m-%d %H:%M")}
    【現在レート】{latest['Close']:.3f} 円
    【前日終値】{last_close:.3f} 円
    【前日比】{change:+.3f} 円
    【本日の始値】{latest['Open']:.3f} 円
    【本日の高値】{latest['High']:.3f} 円
    【本日の安値】{latest['Low']:.3f} 円
    
    【直近5日間の終値推移】
    {hist['Close'].to_string()}
    """
    print(market_data)

except Exception as e:
    print(f"データ取得エラー: {e}")
    market_data = "データ取得失敗"

# 3. エージェント作成（SEOのプロ人格）
analyst = Agent(
    role='FX専属のSEOライター兼テクニカルアナリスト',
    goal='読者の信頼を獲得し、検索上位表示を狙える質の高い市況記事を書くこと',
    backstory="""
    あなたは大手金融メディアで活躍するプロの相場解説者です。
    「事実に基づいた正確な分析」と「初心者にもわかりやすい解説」で定評があります。
    読者が「次にどう動けばいいか」具体的なシナリオを提示するのが得意です。
    煽り文句は使わず、冷静で論理的なトーン（です・ます調）で執筆します。
    """,
    verbose=True,
    llm="gemini/gemini-flash-latest"
)

# 4. タスク作成（SEOテンプレートへの流し込み）
report_task = Task(
    description=f"""
    以下の市場データに基づき、ブログ記事を作成してください。
    
    --- 市場データ ---
    {market_data}
    -----------------

    【記事の構成テンプレート（必ずこれに従うこと）】
    
    # 【{datetime.now().strftime("%m/%d")} ドル円予想】(ここにキャッチーなタイトルを追記)

    ## 📉 今日のポイント（3行要約）
    * (ここに要点1)
    * (ここに要点2)
    * (ここに要点3)

    ## 📊 詳細テクニカル分析
    現在のレートは **{latest['Close']:.2f}円** です。
    直近5日間の値動きを見ると...(ここからトレンド分析、高値・安値の更新状況などを詳しく解説)

    ## 🎯 今日のトレード戦略
    * **買いシナリオ**: (どの水準を超えたら買うか、目標値はどこか)
    * **売りシナリオ**: (どの水準を割ったら売るか、損切りはどこか)
    * **様子見判断**: (どういう動きなら手を出さないか)

    ## ⚠️ 注意すべき経済指標・イベント
    (一般的な市場知識から、今日〜明日注目すべきイベントがあれば追記。なければ「特になし」でOK)

    ---
    *※本記事は情報の提供を目的としており、投資の勧誘を目的としたものではありません。投資の最終判断はご自身でお願いいたします。*
    """,
    expected_output='Markdown形式のブログ記事',
    agent=analyst
)

# 5. 実行
print("--- 🤖 SEO記事を執筆中... ---")
crew = Crew(
    agents=[analyst],
    tasks=[report_task],
    verbose=True
)

result = crew.kickoff()

# 6. 保存（Quartzのフォルダに保存する設定に変更！）
# index.md という名前にすると、サイトのトップページとして認識されます
file_name = "quartz/content/index.md"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(str(result))

print(f"\n✅ サイト更新完了！ '{file_name}' を上書きしました。")