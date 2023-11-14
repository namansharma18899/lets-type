import curses
import random
import time

def draw_graph(stdscr, data):
    # Get screen size
    height, width = stdscr.getmaxyx()

    # Set up the axes
    x_axis = width - 10
    y_axis = height - 10 

    # Draw the axes
    stdscr.addch(y_axis, x_axis, curses.ACS_ULCORNER)  # Upper left corner
    stdscr.addch(0, x_axis + 1, curses.ACS_URCORNER)  # Upper right corner
    stdscr.addch(y_axis + 1, 0, curses.ACS_LLCORNER)  # Lower left corner
    # stdscr.addch(y_axis + 1, x_axis +1, curses.ACS_LRCORNER)  # Lower right corner

    # Draw the horizontal axis
    stdscr.hline(y_axis + 1, 1, curses.ACS_HLINE, x_axis)

    # Draw the vertical axis
    stdscr.vline(1, 0, curses.ACS_VLINE, y_axis)

    # for i in range(len(data)):
    #     x = int((i / (len(data) - 1)) * x_axis)
    #     y = int((1 - data[i]) * y_axis)
    #     stdscr.addch(y, x, ord('*') | curses.color_pair(1))

def main(stdscr):
    # Set up colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Dummy data points for the graph
    data_points = [random.random() for _ in range(10)]

    while True:
        # Draw the graph
        draw_graph(stdscr, data_points)

        # Refresh the screen
        stdscr.refresh()

        # Wait for a short interval
        time.sleep(1)

        # Generate new dummy data points
        data_points = [random.random() for _ in range(10)]

curses.wrapper(main)
