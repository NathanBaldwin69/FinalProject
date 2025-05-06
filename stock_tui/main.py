# main.py

from investors.buffett import BuffettInvestor
from investors.munger import MungerInvestor

def main():
    ticker_symbol = input("Enter ticker symbol: ").upper()

    # Check Buffett's requirements
    passes, criteria = BuffettInvestor.check_requirements(ticker_symbol)
    if passes:
        print(f"{ticker_symbol} meets Buffett's quantitative requirements (at least 4 of 6 tests passed).")
    else:
        print(f"{ticker_symbol} does NOT meet Buffett's quantitative requirements (fewer than 4 tests passed).")
    print("\nCriteria breakdown:")
    for key, value in criteria.items():
        print(f" - {key}: {'PASS' if value else 'FAIL'}")

    # Check Munger's requirements
    passes, criteria = MungerInvestor.check_requirements(ticker_symbol)
    if passes:
        print(f"\n{ticker_symbol} meets Munger's interpreted criteria (at least 3 of 5 tests passed).")
    else:
        print(f"\n{ticker_symbol} does NOT meet Munger's interpreted criteria (fewer than 3 tests passed).")
    print("\nCriteria breakdown:")
    for key, value in criteria.items():
        print(f" - {key}: {'PASS' if value else 'FAIL'}")

if __name__ == "__main__":
    main()
