import yfinance as yf

class QuantitativeAnalysis:
    def __init__(self, ticker_symbol):
        """
        Initialize by fetching stock data from Yahoo Finance.
        """
        ticker = yf.Ticker(ticker_symbol)
        self.info = ticker.info

    # Getter methods for stock data
    def get_roe(self):
        """Get return on equity (ROE)"""
        roe = self.info.get('returnOnEquity')
        return roe if roe is not None else None

    def get_debt_to_equity(self):
        """Get debt-to-equity ratio"""
        debt_to_equity = self.info.get('debtToEquity')
        return debt_to_equity if debt_to_equity is not None else None

    def get_profit_margin(self):
        """Get profit margin"""
        profit_margin = self.info.get('profitMargins')
        return profit_margin if profit_margin is not None else None

    def get_eps_growth(self):
        """Get earnings per share (EPS) growth"""
        eps_growth = self.info.get('earningsQuarterlyGrowth')
        return eps_growth if eps_growth is not None else None

    def get_forward_pe(self):
        """Get forward price-to-earnings (PE) ratio"""
        forward_pe = self.info.get('forwardPE')
        return forward_pe if forward_pe is not None else None

    def get_sgr(self):
        """Get sustainable growth rate (SGR)"""
        roe = self.get_roe()
        payout_ratio = self.info.get('payoutRatio')
        if roe is None or payout_ratio is None:
            return None
        return roe * (1 - payout_ratio)

    # Munger criteria checks
    def get_operating_margin(self):
        """Get operating margin"""
        operating_margin = self.info.get('operatingMargins')
        return operating_margin if operating_margin is not None else None

    def get_price_to_book(self):
        """Get price-to-book ratio"""
        price_to_book = self.info.get('priceToBook')
        return price_to_book if price_to_book is not None else None

    def get_free_cash_flow(self):
        """Get free cash flow"""
        free_cash_flow = self.info.get('freeCashflow')
        return free_cash_flow if free_cash_flow is not None else None

    # Peter Lynch specific checks
    def get_five_year_eps_growth(self):
        """Get 5-year annualized EPS growth"""
        eps_growth = self.info.get('fiveYearAvgDividendYield')  # Might be wrong field name
        return eps_growth if eps_growth is not None else None

    def get_eps_stability(self):
        """Get EPS stability (year-over-year fluctuation)"""
        eps_stability = self.info.get('earningsQuarterlyGrowth')
        return eps_stability if eps_stability is not None else None

    def get_peg_ratio(self):
        """Get PEG ratio"""
        peg_ratio = self.info.get('pegRatio')
        return peg_ratio if peg_ratio is not None else None

    def get_peg_y(self):
        """Get Dividend-Adjusted PEG (PEGY)"""
        dividend_yield = self.get_dividend_yield()
        pe_ratio = self.get_forward_pe()
        eps_growth = self.get_eps_growth()
        if None in (dividend_yield, pe_ratio, eps_growth) or pe_ratio == 0:
            return None
        return (eps_growth + dividend_yield) / pe_ratio

    def get_net_cash_per_share(self):
        """Get net cash per share"""
        net_cash_per_share = self.info.get('netCashPerShare')
        return net_cash_per_share if net_cash_per_share is not None else None

    def get_dividend_yield(self):
        """Get dividend yield"""
        dividend_yield = self.info.get('dividendYield')
        return dividend_yield if dividend_yield is not None else None

    def get_payout_ratio(self):
        """Get payout ratio"""
        payout_ratio = self.info.get('payoutRatio')
        return payout_ratio if payout_ratio is not None else None

    def get_inventory_turnover(self):
        """Get inventory turnover"""
        inventory_turnover = self.info.get('inventoryTurnover')
        return inventory_turnover if inventory_turnover is not None else None

    def get_inventory_growth_vs_sales_growth(self):
        """Get inventory growth vs. sales growth"""
        inventory_growth = self.info.get('inventoryGrowth')  # Check if this is a valid field
        return inventory_growth if inventory_growth is not None else None

    def get_sales_growth(self):
        """Get sales growth"""
        sales_growth = self.info.get('revenueGrowth')
        return sales_growth if sales_growth is not None else None
