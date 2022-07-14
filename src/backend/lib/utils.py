import pytz
from datetime import datetime

def get_utc_now_date():
    return pytz.utc.localize(datetime.utcnow())