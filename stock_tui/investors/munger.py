# investors/munger.py

from quantitative import QuantitativeAnalysis

PASS_THRESHOLD = 3

def check_munger_requirements(ticker_symbol):
    """Evaluates a stock against Charlie Munger investment criteria."""
    analysis = QuantitativeAnalysis(ticker_symbol)

    # Define criteria based on Munger's investing philosophy
    criteria = {
        'operating_margin': analysis.get_operating_margin() is not None and analysis.get_operating_margin() >= 0.20,
        'price_to_book': analysis.get_price_to_book() is not None and analysis.get_price_to_book() <= 3,
        'debt_to_equity': analysis.get_debt_to_equity() is not None and analysis.get_debt_to_equity() < 0.5,
        'roe': analysis.get_roe() is not None and analysis.get_roe() >= 0.15,
        'free_cash_flow': analysis.get_free_cash_flow() is not None and analysis.get_free_cash_flow() > 0,
    }

    passes = sum(criteria.values()) >= PASS_THRESHOLD
    return passes, criteria
