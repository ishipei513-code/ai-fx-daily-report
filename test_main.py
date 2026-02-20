import pytest
import logging
from unittest.mock import MagicMock, patch, mock_open
import sys
import pandas as pd
import os

from main import main

@pytest.fixture
def mock_dependencies(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "fake_key")

    with patch('main.yf') as mock_yf, \
         patch('main.Crew') as mock_crew, \
         patch('main.Agent') as mock_agent, \
         patch('main.Task') as mock_task, \
         patch('main.load_dotenv') as mock_load_dotenv, \
         patch('builtins.open', mock_open(read_data="## 📋 最新のレポート\n\n- [Old Report](./old-report)")) as mock_file, \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.path.getsize', return_value=1234) as mock_getsize, \
         patch('os.path.exists', return_value=True) as mock_exists, \
         patch('main.pytz') as mock_pytz, \
         patch('main.datetime') as mock_datetime:

        mock_ticker = MagicMock()
        mock_yf.Ticker.return_value = mock_ticker

        data = {
            'Open': [150.0, 150.5, 151.0, 151.5, 152.0],
            'High': [151.0, 151.5, 152.0, 152.5, 153.0],
            'Low': [149.0, 149.5, 150.0, 150.5, 151.0],
            'Close': [150.5, 151.0, 151.5, 152.0, 152.5],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        }
        df = pd.DataFrame(data)
        mock_ticker.history.return_value = df

        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        mock_crew_instance.kickoff.return_value = "Mocked Article Content"

        mock_tz = MagicMock()
        mock_pytz.timezone.return_value = mock_tz

        mock_now = MagicMock()
        mock_now.hour = 8
        mock_now.strftime.return_value = "2025-02-20"

        mock_datetime.now.return_value = mock_now

        yield

def test_main_logs(mock_dependencies, caplog):
    caplog.set_level(logging.INFO)

    # Run main
    try:
        main()
    except SystemExit:
        pass
    except Exception as e:
        pytest.fail(f"main() raised exception: {e}")

    # Check for expected log messages
    # We expect these messages to be logged
    expected_substrings = [
        "実行時間帯:",
        "市場データを取得中...",
        "SEO記事を執筆中...",
        "記事を追加しました",
        "posts/index.md を更新しました"
    ]

    captured_messages = [record.message for record in caplog.records]

    for expected in expected_substrings:
        assert any(expected in msg for msg in captured_messages), f"Expected log message containing '{expected}' not found."
