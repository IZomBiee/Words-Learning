from datetime import datetime

def get_current_time() -> str:
    return datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

def get_current_date() -> str:
    return datetime.now().strftime("%d/%m/%Y")

def time_to_numerical_time(time: str) -> int:
    first_part, second_part = time.split('-')

    day, month, year = map(int, first_part.split('/'))
    hour, minute, second = map(int, second_part.split(':'))

    dt = datetime(year, month, day, hour, minute, second)
    return int(dt.timestamp())
