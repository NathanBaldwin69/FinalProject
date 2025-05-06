# investors/buffett.py

from quantitative import QuantitativeAnalysis

PASS_THRESHOLD = 4

def check_buffett_requirements(ticker_symbol):
    """Evaluates a stock against Warren Buffett investment criteria."""
    analysis = QuantitativeAnalysis(ticker_symbol)

    # Evaluate each criterion based on Buffett's rules
    criteria = {
        'roe': analysis.get_roe() is not None and analysis.get_roe() >= 0.15,
        'debt_to_equity': analysis.get_debt_to_equity() is not None and analysis.get_debt_to_equity() < 0.5,
        'profit_margin': analysis.get_profit_margin() is not None and analysis.get_profit_margin() >= 0.1,
        'eps_growth': analysis.get_eps_growth() is not None and analysis.get_eps_growth() >= 0.1,
        'forward_pe': analysis.get_forward_pe() is not None and analysis.get_forward_pe() <= 15,
        'sgr': analysis.get_sgr() is not None and analysis.get_sgr() >= 0.10,
    }

    passes = sum(criteria.values()) >= PASS_THRESHOLD
    return passes, criteria
