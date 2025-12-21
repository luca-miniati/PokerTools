import os
import time
import win32gui
from pywinauto.keyboard import send_keys
from datetime import datetime
from pywinauto import Application
from typing import Set
from pokerkit import HandHistory
from .parser import CoinPokerParser


OUT_DIR = r'data\hud\coinpoker\out'
FAILED_DIR = r'data\hud\coinpoker\failed'
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)


class CoinPokerScraper:
    def __init__(self, delay=0.01):
        self.delay = delay
        self.parser = CoinPokerParser()

        self.hwnd = win32gui.FindWindow('Qt673QWindowIcon', 'Instant Hand History')
        print(f'Found window hwnd: {self.hwnd}')

        self.app = Application(backend='uia').connect(handle=self.hwnd)
        self.window = self.app.window(handle=self.hwnd)
        self.window.set_focus()
        print('Connected to window')
        
        self.setup()

    def setup(self) -> None:
        self.maximize_window()
        self.select_all_tables()

    def select_all_tables(self) -> None:
        table_selector = self.window.child_window(
            auto_id='InstantHandHistory.cmbTables',
            control_type='ComboBox'
        )
        table_selector.click_input()
        send_keys('{HOME}{ENTER}')

    def maximize_window(self) -> None:
        caption = self.window.child_window(
            auto_id='InstantHandHistory.WindowCaption',
            control_type='Group'
        )
        maximize_button = caption.child_window(
            auto_id='InstantHandHistory.WindowCaption.ButtonMaximize',
            control_type='Button'
        )
        if maximize_button.exists():
            maximize_button.click()
    
    def save_hh(self, hh) -> None:
        now = datetime.now()
        fn = os.path.join(OUT_DIR, f'coinpoker_{now.strftime("%Y%m%d_%H%M%S%f")}.phh')
        print(f'Got hh with hand_id={hh.hand}, writing to file')
        with open(fn, 'wb') as f:
            hh.dump(f)

    def run(self) -> None:
        splitter = self.window.child_window(
            auto_id='InstantHandHistory.splitter',
            control_type='Custom'
        )
        hand_table = splitter.child_window(
            auto_id='InstantHandHistory.splitter.handListView',
            control_type='Table'
        )
        data_items = hand_table.descendants(control_type='DataItem')
        hand_rows = [item for item in data_items if item.window_text().isnumeric()]

        hand_rows[0].click_input()
        send_keys('{HOME}')
        seen = set()
        while True:
            hh_raw = self.get_raw_hand_history() + '\n' * 2
            if hh_raw[:50] in seen:
                break
            seen.add(hh_raw[:50])

            hh = next(self.parser(hh_raw), None)
            if hh:
                self.save_hh(hh)
            else:
                print(f'Unable to parse hh: {hh_raw[:80]}')
                now = datetime.now()
                fn = os.path.join(FAILED_DIR, f'coinpoker_{now.strftime("%Y%m%d_%H%M%S%f")}.txt')
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(hh_raw)

            send_keys('{DOWN}')
        
    def get_raw_hand_history(self) -> str:
        hand_history_elem = self.window.child_window(
            auto_id='InstantHandHistory.splitter.handContents',
            control_type='Edit'
        )

        return hand_history_elem.window_text()


if __name__ == '__main__':
    scraper = CoinPokerScraper()
    scraper.run()