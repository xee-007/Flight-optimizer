from datetime import datetime
from helpers import next_24h_date_range_utc

def test_next_24h_date_range_utc_fixed_date():
    # 2025-10-23 13:15 UTC
    fixed = datetime(2025, 10, 23, 13, 15, 0)
    dfrom, dto = next_24h_date_range_utc(fixed)
    assert dfrom == "23/10/2025"
    assert dto == "24/10/2025"
