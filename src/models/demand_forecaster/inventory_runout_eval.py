def calculate_runout_days(stock_on_hand: float, daily_burn_rate: float) -> float:
    if daily_burn_rate <= 0:
        return 999.0
    return round(stock_on_hand / daily_burn_rate, 1)