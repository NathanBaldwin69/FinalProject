# investors/peter_lynch.py

from quantitative import QuantitativeAnalysis

PASS_THRESHOLD = 6

def check_lynch_requirements(ticker_symbol):
    """Evaluates a stock against Peter Lynch investment criteria."""
    analysis = QuantitativeAnalysis(ticker_symbol)

    # Evaluate each criterion based on Peter Lynch's investing rules
    criteria = {
        # Earnings Analysis
        'eps_growth': analysis.get_five_year_eps_growth() is not None and analysis.get_five_year_eps_growth() >= 0.10,
        'eps_stability': analysis.get_eps_stability() is not None and analysis.get_eps_stability() < 0.20,

        # Valuation Metrics
        'peg_ratio': analysis.get_peg_ratio() is not None and analysis.get_peg_ratio() < 1,
        'peg_y': analysis.get_peg_y() is not None and analysis.get_peg_y() >= 1,

        # Balance Sheet Strength
        'debt_to_equity': analysis.get_debt_to_equity() is not None and analysis.get_debt_to_equity() < 0.5,
        'net_cash_per_share': analysis.get_net_cash_per_share() is not None and analysis.get_net_cash_per_share() > 0,

        # Dividend Metrics
        'dividend_yield': analysis.get_dividend_yield() is not None and analysis.get_dividend_yield() >= 0.02,
        'payout_ratio': analysis.get_payout_ratio() is not None and analysis.get_payout_ratio() < 0.6,

        # Operational Efficiency
        'inventory_growth_vs_sales_growth': (
            analysis.get_inventory_growth_vs_sales_growth() is not None
            and analysis.get_sales_growth() is not None
            and analysis.get_inventory_growth_vs_sales_growth() < analysis.get_sales_growth()
        ),
        'inventory_turnover': analysis.get_inventory_turnover() is not None and analysis.get_inventory_turnover() > 6,
    }

    passes = sum(criteria.values()) >= PASS_THRESHOLD
    return passes, criteria
