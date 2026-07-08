from utils.calculations import calculate_trip_duration
from datetime import date

print(calculate_trip_duration)

print(
    calculate_trip_duration(
        date(2026,8,1),
        date(2026,8,10)
    )
)