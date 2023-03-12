import calendar
import datetime


def get_all_dates_in_month(year: int, month: int):
    """
    Возвращает все даты заданного месяца и года.

    Args:
        year: Год
        month: Месяц
    """
    return [
        date for date in calendar.Calendar().itermonthdates(year, month)
        if date.month == month
    ]


today = datetime.date.today()
ALL_DATES_IN_MONTH = get_all_dates_in_month(today.year, today.month)
