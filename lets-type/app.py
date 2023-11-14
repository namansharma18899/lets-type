import curses
import asyncio
import time
from utils import wrap_text, get_fresh_quote, get_logger


logger = get_logger()


def main(stdscr):
    def play(stdscr):
        original_text = "This is a temprary text written from scratch for all of you."
        input_text = ""
        cursor_position = 0
        wrong = []
        # --------------------------------------------------------------------
        curses.curs_set(1)  # Set the cursor to be visible
        stdscr.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

        height, width = stdscr.getmaxyx()
        header_height = 1
        footer_height = 1
        middle_height = height - header_height - footer_height
        header_text = "Lets Type"  # Header
        stdscr.addstr(
            0,
            int((width - len(header_text)) // 2),
            wrap_text(header_text),
            curses.color_pair(1) | curses.A_BOLD,
        )
        stdscr.hline(
            header_height, 0, curses.ACS_HLINE, width, curses.color_pair(4)
        )  # Yellow boundary line
        footer_text = "Press 'q' to exit & 'r' to replay"  # Footer
        stdscr.addstr(
            height - footer_height,
            0,
            wrap_text(footer_text),
            curses.color_pair(5) | curses.A_BOLD,
        )
        stdscr.hline(  # Yellow boundary line
            height - footer_height - 1, 0, curses.ACS_HLINE, width, curses.color_pair(4)
        )
        middle_y = header_height + 1  # Middle portion with active cursor
        middle_x = 0
        input_text = ""
        window_height, window_width = height, width
        start_time = time.time()

        while True:
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
            # original_text = asyncio.run(get_fresh_quote(2))

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
            stdscr.move(middle_y, cursor_position)
            stdscr.refresh()
            if cursor_position >= len(original_text):
                break
            key = stdscr.getch()  # Get Current Character Input
            input_text = input_text + chr(key)
            try:
                if chr(key) != original_text[cursor_position]:
                    wrong.append(cursor_position)
            except IndexError as ie:
                break
            logger.debug(
                f"Key -> {chr(key)} | cursorpis -> {cursor_position} | inpt-> {input_text} | org -> {original_text[cursor_position]}"
            )
            cursor_position += 1
            if key == 10:  # Enter key to Exit
                break
        elapsed_time = (time.time() - start_time) / 60
        logger.info(f"time diff -> {elapsed_time} text len {len(original_text)}")
        report_text = "Report"
        stdscr.addstr(
            middle_y + 12,
            len(report_text) + 1,
            f"Speed: {int(len(input_text.split(' ')))/elapsed_time:.2f} WPM",
            curses.color_pair(1),
        )
        stdscr.addstr(
            middle_y + 13,
            len(report_text) + 1,
            f"Accuracy: {(len(set(original_text.split()).symmetric_difference(set(input_text.split())))//2 * 100)/ len(original_text.split()):.2f} WPM",
            curses.color_pair(1),
        )
        stdscr.addstr(
            middle_y + 15,
            len(report_text) + 1,
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
