from services.google_places_service import GooglePlacesService

service = GooglePlacesService()

places = service.search_budget_restaurants("Tokyo")

for place in places[:5]:
    print(place)