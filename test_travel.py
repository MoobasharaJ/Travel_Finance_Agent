from services.travel_service import TravelService
from datetime import date


travel = TravelService()

trip_id = travel.create_trip(
    destination="Japan",
    start_date=date(2026, 8, 1),
    end_date=date(2026, 8, 10),
    total_budget=100000
)

print(trip_id)

