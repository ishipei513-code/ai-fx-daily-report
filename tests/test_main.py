import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import pandas as pd
from datetime import datetime

# Add the project root to sys.path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock modules that main.py imports but we don't want to run
sys.modules['crewai'] = MagicMock()
sys.modules['yfinance'] = MagicMock()
sys.modules['pytz'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

import main

class TestMainRefactor(unittest.TestCase):
    def setUp(self):
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {"GOOGLE_API_KEY": "fake_key"})
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @patch('main.yf.Ticker')
    @patch('main.Crew')
    @patch('main.Agent')
    @patch('main.Task')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('main.pytz.timezone')
    @patch('main.datetime')
    @patch('logging.basicConfig')
    def test_main_logging(self, mock_basicConfig, mock_datetime, mock_timezone, mock_open, mock_task, mock_agent, mock_crew, mock_ticker):
        # Setup mocks
        mock_now = MagicMock()
        mock_now.hour = 9
        mock_now.strftime.return_value = "2024-01-01"
        mock_datetime.now.return_value = mock_now

        # yfinance mock
        mock_hist = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 103.0],
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000, 2000]
        })
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker.return_value = mock_ticker_instance

        # crewai mock
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Mocked Report Content"
        mock_crew.return_value = mock_crew_instance

        # Mock os.path.getsize
        with patch('os.path.getsize', return_value=12345):
             # Mock os.path.exists to simulate index.md exists
            with patch('os.path.exists', return_value=True):
                 # Run main
                with self.assertLogs(level='INFO') as cm:
                    result = main.main()

                # Verify result
                self.assertEqual(result, 0)

                # Verify logs contain expected messages
                logs = [r.getMessage() for r in cm.records]
                self.assertTrue(any("実行時間帯" in log for log in logs), "Missing '実行時間帯' log")
                self.assertTrue(any("市場データを取得中" in log for log in logs), "Missing '市場データを取得中' log")
                self.assertTrue(any("SEO記事を執筆中" in log for log in logs), "Missing 'SEO記事を執筆中' log")
                self.assertTrue(any("記事を追加しました" in log for log in logs), "Missing '記事を追加しました' log")

if __name__ == '__main__':
    unittest.main()
