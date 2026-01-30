import os
import yfinance as yf
from datetime import datetime
import pytz  # JST判定用に追加
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import sys  # exit用

# 1. 設定読み込み
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 2. JST時間帯を取得（複数時間実行対応）
jst = pytz.timezone('Asia/Tokyo')
now_jst = datetime.now(jst)
jst_hour = now_jst.hour

if 6 <= jst_hour < 10:
    time_tag = "朝の市場まとめ"
    emphasis = "前日終値から見た今日の戦略"
elif 14 <= jst_hour < 18:
    time_tag = "午後アップデート"
    emphasis = "午前中の動きを踏まえた最新戦略"
else:
    time_tag = "夜間戦略"
    emphasis = "欧米市場に向けた夜のポイント"

print(f"--- 実行時間帯: {time_tag} ({jst_hour:02d}:00 JST) ---")

# 3. 【強化版】データの取得（過去5日分を取得してトレンドを見させる）
print("--- 📊 市場データを取得中... ---")
try:
    ticker = "JPY=X"
    data = yf.Ticker(ticker)
    hist = data.history(period="5d")
    
    if hist.empty:
        raise ValueError("データが取得できませんでした（空のDataFrame）")
    
    latest = hist.iloc[-1]
    last_close = hist.iloc[-2]['Close'] if len(hist) >= 2 else latest['Close']
    change = latest['Close'] - last_close
    
    market_data = f"""
    【対象通貨ペア】USD/JPY (ドル円)
    【現在日時】{now_jst.strftime("%Y-%m-%d %H:%M JST")}
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
    print("記事生成を中断します。")
    sys.exit(1)  # Actionsで失敗扱いにする

# 4. エージェント作成（SEOのプロ人格）
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
    llm="gemini/gemini-1.5-flash"  # 安定版に変更（flash-latestより推奨）
)

# 5. タスク作成（SEOテンプレートへの流し込み）
report_task = Task(
    description=f"""
    以下の市場データに基づき、個人投資家が「今すぐトレードしたくなる」ブログ記事を作成してください。

    --- 市場データ ---
    {market_data}
    -----------------

    【記事の構成ルール（Markdown形式）】
    
    # 【{now_jst.strftime("%m/%d")} ドル円予想】{time_tag}（{emphasis}）

    ## 📉 今日のポイント（3行要約）
    * (忙しい人のために結論をズバリ)
    * (トレンドの方向性)
    * (今日の注目イベント)

    ## 📊 詳細テクニカル分析
    現在のレートは **{latest['Close']:.2f}円** です。
    (直近5日間の動きから、移動平均線やレジスタンスラインを意識したプロっぽい解説をする)

    ## 🎯 今日のトレード戦略（ここに収益化への伏線を入れる）
    * **買いシナリオ**: (具体的なエントリーポイント)
    * **売りシナリオ**: (具体的な損切りライン)
    * **プロのアドバイス**: 
      「今日の相場は動きが早いので、約定力の高いFX会社を使うのが鉄則です。」
      「初心者はスプレッドの狭い口座でコストを抑えるのが勝つコツです。」
      といった、**口座開設が必要だと感じさせる一言**を必ず添えてください。

    ## ⚠️ 注意すべき経済指標
    今日〜明日の注目経済指標を必ず記載してください。
    （例: 米国雇用統計、FOMC、日銀短観など。なければ「本日は大きな指標発表なし」と明記）

    ---
    """,
    expected_output='Markdown形式のブログ記事',
    agent=analyst
)

# 6. 実行
print("--- 🤖 SEO記事を執筆中... ---")
crew = Crew(
    agents=[analyst],
    tasks=[report_task],
    verbose=True
)

result = crew.kickoff()

# 7. 保存（資産積み上げモード）

# 今日の日付を取得
today_str = now_jst.strftime("%Y-%m-%d")
today_title = now_jst.strftime("%Y/%m/%d")

# Quartz用のメタデータ（draft: false を明示）
frontmatter = f"""---
title: "{today_title} ドル円AI市場分析（{time_tag}）"
date: {today_str}
description: "【AI分析】今日（{today_title}）のドル円相場をプロレベルで徹底解説。最新レート {latest['Close']:.2f}円を踏まえたトレード戦略と今後の見通しをAIが提案します。"
tags: ["USDJPY", "ドル円予想", "FX分析", "テクニカル分析"]
draft: false
---

"""

# 広告ブロック（あなたのリンクに置き換えてください）
ad_block = """
<br>

## 📢 プロも愛用！おすすめFX口座リスト

勝ちトレーダーになるためには、道具（口座）選びが命です。

### 🥇 DMM FX
**迷ったらコレ！国内口座数No.1の実力派。**
* スマホアプリが直感的で使いやすい
* 最短1時間で取引開始できる
* [👉 DMM FXの口座開設はこちら](https://your-affiliate-link-dmm)

### 🥈 GMOクリック証券
**コストを極限まで抑えたい人へ。**
* 業界最安水準のスプレッド
* 高機能なチャートツールが無料
* [👉 GMOクリック証券の詳細を見る](https://your-affiliate-link-gmo)

> ※本記事はAIによる市場分析です。投資の勧誘を目的としたものではありません。
"""

# 全部合体
final_content = frontmatter + str(result) + "\n\n" + ad_block

# 保存パス
save_path = f"quartz/content/posts/{today_str}-report.md"
os.makedirs("quartz/content/posts", exist_ok=True)

with open(save_path, "w", encoding="utf-8") as f:
    f.write(final_content)

# 保存確認ログ
print(f"\n✅ 記事を追加しました！ 保存先: {save_path}")
print(f"ファイルサイズ: {os.path.getsize(save_path)} バイト")
print("内容の先頭10行:")
with open(save_path, "r", encoding="utf-8") as f:
    print("".join(f.readlines()[:10]))