"""
Google Places Service

Responsible for:
- Converting city names to coordinates
- Searching nearby places using Google Places API

No Streamlit.
No AI.
No Budget logic.
No Database.
"""

import os
import requests
import streamlit as st

from dotenv import load_dotenv

load_dotenv()


class GooglePlacesService:

    def __init__(self):

        # Local .env
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        # Streamlit Cloud
        if not self.api_key:
            self.api_key = st.secrets.get("GOOGLE_MAPS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GOOGLE_MAPS_API_KEY not found."
            )

        self.geocode_url = (
            "https://maps.googleapis.com/maps/api/geocode/json"
        )

        self.nearby_url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        )

    # ======================================================
    # Get Coordinates
    # ======================================================

    def get_coordinates(self, city):
        """
        Convert a city name into latitude & longitude.
        """

        response = requests.get(
            self.geocode_url,
            params={
                "address": city,
                "key": self.api_key,
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if not data["results"]:
            return None

        location = data["results"][0]["geometry"]["location"]

        return (
            location["lat"],
            location["lng"],
        )

    # ======================================================
    # Nearby Search
    # ======================================================

    def search_places(
        self,
        city,
        place_type,
        keyword=None,
        radius=3000,
    ):
        """
        Search nearby places around a city.
        """

        coordinates = self.get_coordinates(city)

        if coordinates is None:
            return []

        latitude, longitude = coordinates

        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "type": place_type,
            "key": self.api_key,
        }

        if keyword:
            params["keyword"] = keyword

        response = requests.get(
            self.nearby_url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        places = []

        for place in data.get("results", []):

            places.append({

                "name": place.get("name"),

                "address": place.get("vicinity"),

                "rating": place.get("rating", "N/A"),

                "total_ratings": place.get(
                    "user_ratings_total",
                    0,
                ),

                "latitude": place["geometry"]["location"]["lat"],

                "longitude": place["geometry"]["location"]["lng"],

                "business_status": place.get(
                    "business_status",
                    "Unknown",
                ),

                "maps_url": (
                    "https://www.google.com/maps/search/?api=1"
                    f"&query={place['geometry']['location']['lat']},"
                    f"{place['geometry']['location']['lng']}"
                ),
            })

        return places

    # ======================================================
    # Budget Restaurants
    # ======================================================

    def search_budget_restaurants(self, city):

        return self.search_places(
            city=city,
            place_type="restaurant",
            keyword="budget",
        )

    # ======================================================
    # ATM
    # ======================================================

    def search_atms(self, city):

        return self.search_places(
            city=city,
            place_type="atm",
        )

    # ======================================================
    # Currency Exchange
    # ======================================================

    def search_currency_exchange(self, city):

        return self.search_places(
            city=city,
            place_type="finance",
            keyword="currency exchange",
        )

    # ======================================================
    # Convenience Store
    # ======================================================

    def search_convenience_stores(self, city):

        return self.search_places(
            city=city,
            place_type="convenience_store",
        )