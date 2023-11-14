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
        logger.info(" hellooo ")
        # --------------------------------------------------------------------
        curses.curs_set(1)  # Set the cursor to be visible
        stdscr.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header color
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)  # Footer color
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Middle portion color
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Boundary color

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
            curses.color_pair(2) | curses.A_BOLD,
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
                curses.color_pair(2) | curses.A_BOLD,
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
        time_diff = (time.time() - start_time) / 60
        logger.info(f"time diff -> {time_diff} text len {len(original_text)}")
        report_text = "You had a typing speed of "
        stdscr.addstr(
            middle_y + 10,
            0,
            report_text,
            curses.color_pair(3),
        )
        stdscr.addstr(
            middle_y + 10,
            len(report_text) + 1,
            f"{int(len(input_text.split(' ')))/time_diff} WPM",
            curses.color_pair(1),
        )
    while True:
        play(stdscr)
        key = stdscr.getch()  # Get Current Character Input
        if chr(key) == 'q':
            break
        elif chr(key)== 'r':
            continue
        else:
            break
    curses.endwin()

    # elif key == curses.KEY_BACKSPACE or key == 127:
    #     if cursor_position > 0:
    #         input_text = input_text[:cursor_position - 1] + input_text[cursor_position:]
    #         stdscr.addstr(1, cursor_position, chr(key), curses.color_pair(2))
    #         stdscr.move(1, cursor_position)
    #         stdscr.refresh()
    #         cursor_position -= 1
    # else:
    #     if cursor_position < len(original_text) and chr(key) == original_text[cursor_position]:
    #         input_text = input_text[:cursor_position] + chr(key) + input_text[cursor_position:]
    #         stdscr.addstr(1, cursor_position, chr(key), curses.color_pair(2))
    #         cursor_position += 1
    #         stdscr.move(1, cursor_position)
    #         stdscr.refresh()
    #     else:
    #         input_text = input_text[:cursor_position] + chr(key) + input_text[cursor_position:]
    #         stdscr.addstr(1, cursor_position, chr(key), curses.color_pair(1))
    #         cursor_position += 1
    #         stdscr.move(1, cursor_position)
    #         stdscr.refresh()

    # End curses


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt as ke:
        print("Gracefully Exiting")
