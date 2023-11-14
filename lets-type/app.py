import curses
import time

class Args:
    def __init__(self) -> None:
        pass

class LetsType:
    def __init__(self) -> None:
        curses.wrapper(self._start_typing)
    
    def _start_typing(self, stdscr):
        curses.curs_set(1)  # Set the cursor to be visible
        stdscr.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header color
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Footer color
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Middle portion color

        height, width = stdscr.getmaxyx()

        header_height = 1
        footer_height = 1
        middle_height = height - header_height - footer_height

        # Header
        header_text = "Header"
        stdscr.addstr(0, 0, header_text, curses.color_pair(1) | curses.A_BOLD)

        # Footer
        footer_text = "Footer - Press 'q' to exit"
        stdscr.addstr(height - footer_height, 0, footer_text, curses.color_pair(2) | curses.A_BOLD)

        # Middle portion with active cursor
        middle_y = header_height
        middle_x = 0
        input_text = ""

        while True:
            stdscr.clear()
            stdscr.bkgd(curses.color_pair(3))

            # Header
            stdscr.addstr(0, 0, header_text, curses.color_pair(1) | curses.A_BOLD)

            # Footer
            stdscr.addstr(height - footer_height, 0, footer_text, curses.color_pair(2) | curses.A_BOLD)

            # Middle portion
            stdscr.addstr(middle_y, middle_x, input_text, curses.color_pair(3) | curses.A_BOLD)

            # Refresh the screen
            stdscr.refresh()

            # Get user input
            key = stdscr.getch()

            # Handle input
            if key == ord('q'):
                break
            elif key == 10:  # Enter key
                input_text = ""
            elif key == curses.KEY_BACKSPACE:
                input_text = input_text[:-1]
            elif key >= 32 and key < 127:
                input_text += chr(key)
obj = LetsType()