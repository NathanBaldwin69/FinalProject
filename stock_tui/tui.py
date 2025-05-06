import curses
from investors.buffett import check_buffett_requirements
from investors.munger import check_munger_requirements
from investors.lynch import check_lynch_requirements

# Constants for key codes
KEY_ENTER = 10
KEY_ESC = 27
KEY_BACKSPACE_1 = 263
KEY_BACKSPACE_2 = 127

# Display constants
HEADER_LINE = 0
PROMPT_LINE = 2
TICKER_INPUT_LINE = 8
EXIT_PROMPT_LINE = -1

# Mapping of investor names to their evaluation functions
INVESTOR_FUNCTIONS = {
    'Buffett': check_buffett_requirements,
    'Munger': check_munger_requirements,
    'Peter Lynch': check_lynch_requirements,
}

# Color pairs (using terminal's default color support)
COLOR_HEADER = 1
COLOR_SUCCESS = 2
COLOR_FAIL = 3
COLOR_PROMPT = 4
COLOR_DEFAULT = 5

def setup_colors():
    """
    Initialize color pairs for the TUI application.
    """
    curses.start_color()
    curses.init_pair(COLOR_HEADER, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_SUCCESS, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_FAIL, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_PROMPT, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_WHITE, curses.COLOR_BLACK)

def display_header(window, message):
    """
    Clear the screen and show a header message in yellow.
    """
    window.clear()
    window.attron(curses.color_pair(COLOR_HEADER))
    window.addstr(HEADER_LINE, 0, message)
    window.attroff(curses.color_pair(COLOR_HEADER))
    window.refresh()

def get_investor_choice(window):
    """
    Display a list of investors and return user selection.
    Returns a list of selected investor names.
    """
    options = list(INVESTOR_FUNCTIONS.keys()) + ["All (Buffett, Munger, Peter Lynch)"]
    window.addstr(PROMPT_LINE, 0, "Select an investor for stock evaluation:", curses.color_pair(COLOR_PROMPT))
    for i, name in enumerate(options, 1):
        window.addstr(PROMPT_LINE + i, 0, f"{i}. {name}")
    window.refresh()

    choice = window.getch()

    # Valid single selections
    valid_choices = [ord(str(i)) for i in range(1, len(INVESTOR_FUNCTIONS) + 1)]

    # Key for the all option
    all_option = ord(str(len(options)))

    if choice in valid_choices:
        return [list(INVESTOR_FUNCTIONS.keys())[choice - ord('1')]]
    elif choice == all_option:
        return list(INVESTOR_FUNCTIONS.keys())
    else:
        return []

def get_ticker_input(window):
    """
    Prompt user for a ticker symbol and return it.
    Returns uppercase ticker string or empty string on esc.
    """
    window.addstr(PROMPT_LINE + 5, 0, "Enter ticker symbol: ", curses.color_pair(COLOR_PROMPT))
    window.refresh()

    window.move(TICKER_INPUT_LINE, 0)
    ticker = ""

    while True:
        char = window.getch()
        if char == KEY_ENTER:
            break
        elif char == KEY_ESC:
            return ""
        elif char in (KEY_BACKSPACE_1, KEY_BACKSPACE_2):
            ticker = ticker[:-1]
            window.move(TICKER_INPUT_LINE, 0)
            window.clrtoeol()
            window.addstr(TICKER_INPUT_LINE, 0, ticker)
        else:
            ticker += chr(char)
            window.addstr(TICKER_INPUT_LINE, len(ticker) - 1, chr(char))
        window.refresh()

    return ticker.upper()

def get_analysis_mode(window):
    """
    Ask user to choose between single or multiple stock analysis.
    Returns single, multi, or empty string if invalid.
    """
    window.clear()
    window.addstr(PROMPT_LINE, 0, "Select analysis mode:", curses.color_pair(COLOR_PROMPT))
    window.addstr(PROMPT_LINE + 1, 0, "1. Single stock (detailed criteria)")
    window.addstr(PROMPT_LINE + 2, 0, "2. Multiple stocks (summary only)")
    window.refresh()

    choice = window.getch()
    if choice == ord('1'):
        return 'single'
    elif choice == ord('2'):
        return 'multi'
    else:
        return ''

def display_results(window, ticker_symbol, investor_results):
    """
    Display evaluation results for one or more investors.
    Shows full criteria if one investor, otherwise summary only.
    """
    def wait_and_clear():
        # Prompt user before clearing when screen fills up
        window.addstr(curses.LINES + EXIT_PROMPT_LINE, 0, "Press any key to continue...", curses.color_pair(COLOR_PROMPT))
        window.refresh()
        window.getch()
        window.clear()

    window.clear()
    line_index = 2
    window.addstr(0, 0, f"Results for {ticker_symbol}:\n\n", curses.color_pair(COLOR_HEADER))
    max_lines = curses.LINES - 2

    for name, results in investor_results.items():
        criteria = results['criteria']
        passes = results['passes']

        if len(investor_results) == 1:
            window.addstr(line_index, 0, f"{name} Results:", curses.color_pair(COLOR_HEADER))
            line_index += 1
            window.addstr(line_index, 0, f"Overall: {'PASS' if passes else 'FAIL'}", curses.color_pair(COLOR_SUCCESS if passes else COLOR_FAIL))
            line_index += 1
            for key, passed in criteria.items():
                window.addstr(line_index, 0, f" - {key}: {'PASS' if passed else 'FAIL'}", curses.color_pair(COLOR_SUCCESS if passed else COLOR_FAIL))
                line_index += 1
                if line_index >= max_lines:
                    wait_and_clear()
                    line_index = 2
        else:
            # For multiple investors, show summary only
            passed_tests = sum(criteria.values())
            total_tests = len(criteria)
            window.addstr(line_index, 0, f"{name} Summary: Passed {passed_tests} of {total_tests} tests", curses.color_pair(COLOR_DEFAULT))
            line_index += 1
            if line_index >= max_lines:
                wait_and_clear()
                line_index = 2

    window.refresh()

def main(stdscr):
    """
    Main function for running the tui application.
    Handles input flow, evaluation, and output display.
    """
    curses.curs_set(0)
    setup_colors()  # Initialize color pairs
    display_header(stdscr, "Stock Evaluation TUI")

    selected = get_investor_choice(stdscr)
    if not selected:
        stdscr.addstr(10, 0, "Invalid choice! Please select a valid option.", curses.color_pair(COLOR_FAIL))
        stdscr.refresh()
        stdscr.getch()
        return

    mode = get_analysis_mode(stdscr)
    if not mode:
        stdscr.addstr(10, 0, "Invalid analysis mode selected. Exiting...", curses.color_pair(COLOR_FAIL))
        stdscr.refresh()
        stdscr.getch()
        return

    if mode == 'single':
        ticker = get_ticker_input(stdscr)
        if not ticker:
            stdscr.addstr(10, 0, "No ticker symbol entered. Exiting...", curses.color_pair(COLOR_FAIL))
            stdscr.refresh()
            stdscr.getch()
            return

        investor_results = {}

        # Run evaluation for selected investors
        for name in selected:
            func = INVESTOR_FUNCTIONS[name]
            passed, criteria = func(ticker)
            investor_results[name] = {"passes": passed, "criteria": criteria}

        display_results(stdscr, ticker, investor_results)

    elif mode == 'multi':
        tickers = []
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Enter ticker symbol (or press ENTER to finish): ", curses.color_pair(COLOR_PROMPT))
            stdscr.refresh()
            ticker = get_ticker_input(stdscr)
            if not ticker:
                break
            tickers.append(ticker)

        stdscr.clear()
        line_index = 0
        max_lines = curses.LINES - 2

        for ticker in tickers:
            stdscr.addstr(line_index, 0, f"{ticker}:", curses.color_pair(COLOR_HEADER))
            line_index += 1

            # Evaluate each investor for current ticker
            for name in selected:
                func = INVESTOR_FUNCTIONS[name]
                passed, criteria = func(ticker)
                summary = f"{name}: {'PASS' if passed else 'FAIL'} ({sum(criteria.values())}/{len(criteria)})"
                stdscr.addstr(line_index, 2, summary, curses.color_pair(COLOR_DEFAULT))
                line_index += 1

            line_index += 1

            # Handle screen overflow
            if line_index >= max_lines:
                stdscr.addstr(curses.LINES + EXIT_PROMPT_LINE, 0, "Press any key to continue...", curses.color_pair(COLOR_PROMPT))
                stdscr.refresh()
                stdscr.getch()
                stdscr.clear()
                line_index = 0

        stdscr.refresh()

    stdscr.addstr(curses.LINES + EXIT_PROMPT_LINE, 0, "Press any key to exit.", curses.color_pair(COLOR_PROMPT))
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
