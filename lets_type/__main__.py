import curses
import asyncio
import time
from typing import Any

from lets_type.utils import wrap_text, get_fresh_quote, get_logger, get_speed_emoticons

logger = get_logger()


def main(stdscr):
    def handle_resize(stdscr):
        height, width = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.addstr(0, 0, f"Terminal resized to {height}x{width}")
        stdscr.refresh()

    def play(stdscr):
        original_text = get_fresh_quote(2)
        cursor_position = 0
        wrong = []
        # Setup Window
        curses.curs_set(1)  # Set the cursor to be visible
        stdscr.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        input_text = ""
        header_text = "Lets Type"  # Header
        footer_text = (
            "powered by Python🐍  "   #"Press 'q' to exit & 'r' to replay"  # Foote
        )
        start_time = time.time()
        header_height = 1
        footer_height = 1
        middle_y = header_height + 1  # Middle portion with active cursor
        middle_x = 0
        while True:  # Event Loop
            window_height, window_width = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.bkgd(curses.color_pair(3))
            stdscr.addstr(
                0,
                int((window_width - len(header_text)) // 2),
                wrap_text(header_text),
                curses.color_pair(1) | curses.A_BOLD,
            )  # Header
            stdscr.hline(  # Yellow boundary line
                header_height, 0, curses.ACS_HLINE, window_width, curses.color_pair(4)
            )
            stdscr.addstr(  # Footer
                window_height - footer_height,
                0,
                wrap_text(footer_text),
                curses.color_pair(5) | curses.A_BOLD,
            )
            stdscr.hline(  # Yellow boundary line
                window_height - footer_height - 1,
                0,
                curses.ACS_HLINE,
                window_width,
                curses.color_pair(4),
            )
            stdscr.addstr(middle_y, middle_x, original_text)
            for posi in range(cursor_position):
                if posi in wrong:
                    stdscr.addstr(
                        middle_y,
                        posi,
                        original_text[posi],
                        curses.color_pair(2) if posi in wrong else curses.color_pair(1),
                    )
            stdscr.addstr(
                middle_y + 5,
                0,
                input_text,
                curses.color_pair(3),
            )
            try:
                stdscr.move(middle_y, cursor_position)
            except Exception as e:
                logger.info(
                    f"window spec {window_height}, {window_width} \
                            {middle_y}, {cursor_position}"
                )
            stdscr.refresh()
            if len(input_text) >= len(original_text):
                break
            KEY = stdscr.getch()  # Get Current Character Input
            if KEY == curses.KEY_RESIZE:
                window_height, window_width = stdscr.getmaxyx()
                stdscr.clear()
                logger.info(f"Terminal resized to {window_height}x {window_width}")
                stdscr.refresh()
                # handle_resize(stdscr)
                continue
            input_text = input_text + chr(KEY)
            try:
                if chr(KEY) != original_text[cursor_position]:
                    wrong.append(cursor_position)
            except IndexError as ie:
                break
            logger.debug(
                f"Key -> {chr(KEY)} | cursorpis -> {cursor_position} | \
                inpt-> {input_text} | org -> {original_text[cursor_position]}"
            )
            if int((cursor_position + 1) / window_width) > 0:
                cursor_position = int((cursor_position + 1) % window_width)
                middle_y += 1
            else:
                cursor_position += 1
            if KEY == 10:  # Enter key to Exit
                break
        logger.info(f"wrong -> {wrong}, input -> {len(input_text)}")
        elapsed_time = (time.time() - start_time) / 60
        logger.info(f"time diff -> {elapsed_time} text len {len(original_text)}")
        speed_wpm = round(int(len(input_text.split(" "))) / round(elapsed_time, 2), 2)
        accuracy = int(((len(input_text) - len(wrong)) * 100) / len(input_text))
        stdscr.addstr(
            middle_y + 12,
            7,
            f"Speed: {speed_wpm} WPM",
            curses.color_pair(1),
        )
        stdscr.addstr(
            middle_y + 13,
            7,
            f"Accuracy: {accuracy}%",
            curses.color_pair(1),
        )
        stdscr.addstr(
            middle_y + 14,
            7,
            f"Time: {round(elapsed_time, 2)} sec",
            curses.color_pair(1),
        )
        stdscr.addstr(
            middle_y + 17,
            7,
            get_speed_emoticons(int(speed_wpm), accuracy),
            curses.color_pair(3),
        )
        stdscr.addstr(
            middle_y + 19,
            7,
            f"Press 'q' to Quit and 'r' to Replay",
            curses.color_pair(4),
        )

    while True:
        play(stdscr)
        key = stdscr.getch()  # Get Current Character Input
        if chr(key) == "q":
            break
        elif chr(key) == "r":
            continue
        else:
            break
    curses.endwin()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt as ke:
        print("Gracefully Exiting")


class TypingSession:
    _start_time = None
    _end_time = None
    _accuracy = None
    _speed = None

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    @property
    def accuracy(self):
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value):
        self._accuracy = value


class LetsType:
    def __init__(self, stdscr) -> None:
        self.window = stdscr
        self.wrong_inputs = []
        self.cursor_position = 0
        self.org_word_mtd = {
            "cursor_position": [0, 0],  # x,y
            "word": get_fresh_quote(2),
        }
        self.input_word_mtd = {"cursor_position": [0, 10], "word": ""}  # x,y
        self.session = {
            "start_time": None,
            "end_time": None,
            "accuracy": None,
            "speed": None,
        }

    def __setup_window(self):
        curses.curs_set(1)  # Set the cursor to be visible
        self.window.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.header_text = "Lets Type"  # Header
        self.footer_text = "Press 'q' to exit & 'r' to replay"  # Footer
        self.header_height = 1
        self.footer_height = 1
        self.banner_coord = [0, self.header_height + 1]
        # self.banner+middle_y = self.header_height + 1  # Middle portion with active cursor
        # self.middle_x = 0

    def setup(self):
        self.__setup_window()
        self.start_time = time.time()
        # wait for text to proceed or used cached one incase InternetError
        # Play
        # Show stats
        pass

    def teardown(self):
        pass

    def setup_window(self):
        pass

    def pull_text(self):
        pass

    def play(self):
        pass

    def show_stats(self):
        pass
