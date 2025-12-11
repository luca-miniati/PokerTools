import os
import time
import win32gui
from datetime import datetime
from pywinauto import Application
from pokerkit import HandHistory
from data.hud.coinpoker.parser import CoinPokerParser


OUT_DIR = r'data\hud\coinpoker\out'
os.makedirs(OUT_DIR, exist_ok=True)
print(os.getcwd())


class CoinPokerScraper:
    def __init__(self, delay=0.01):
        self.delay = delay

        self.hwnd = win32gui.FindWindow('Qt673QWindowIcon', 'Instant Hand History')
        print(f'Found window hwnd: {self.hwnd}')

        self.app = Application(backend='uia').connect(handle=self.hwnd)
        self.window = self.app.window(handle=self.hwnd)
        print('Connected to window')

    def run(self) -> None:
        hh_raw = self.get_raw_hand_history()
        print(f'Got raw hand history: {hh_raw[:20]}...')

        now = datetime.now()
        fn = os.path.join(OUT_DIR, f'coinpoker_{now.strftime("%Y%m%d_%H%M")}.phh')

    def get_raw_hand_history(self) -> str:
        hand_history_elem = self.window.child_window(
            auto_id='InstantHandHistory.splitter.handContents', control_type='Edit'
        )

        time.sleep(self.delay)

        return hand_history_elem.window_text()

    def parse_hh(self, hh_raw: str) -> HandHistory:
        pass


if __name__ == '__main__':
    scraper = CoinPokerScraper()
    scraper.run()