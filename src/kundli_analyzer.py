import swisseph as swe
import datetime
from typing import Dict, List, Tuple

class KundliAnalyzer:
    def __init__(self, name: str, birth_datetime: datetime.datetime, place: str):
        self.name = name
        self.birth_datetime = birth_datetime
        self.place = place
        self.planets: Dict[str, Dict[str, float]] = {}
        self.aspects: List[Tuple[str, str, float]] = []
        self.analyze_kundli()

    def analyze_kundli(self):
        jd = swe.julday(
            self.birth_datetime.year,
            self.birth_datetime.month,
            self.birth_datetime.day,
            self.birth_datetime.hour + self.birth_datetime.minute / 60.0
        )

        planets = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE,
            # Ketu will be computed based on Rahu's position
        }

        for planet_name, planet_id in planets.items():
            planet_result = swe.calc_ut(jd, planet_id)
            # planet_result is a tuple (list of params, flag)
            # Usually planet_result[0] is list: [longitude, latitude, distance, speed, ...]
            data = planet_result[0]
            self.planets[planet_name] = {
                'longitude': data[0],
                'latitude': data[1],
                'distance': data[2],
                'speed': data[3]
            }

        # Compute Ketu's longitude (opposite of Rahu)
        self.planets['Ketu'] = self.planets['Rahu'].copy()
        self.planets['Ketu']['longitude'] = (self.planets['Rahu']['longitude'] + 180) % 360

        # Compute aspects
        self.aspects = self._calculate_aspects()

    def _calculate_aspects(self) -> List[Tuple[str, str, float]]:
        aspects = []
        for p1 in self.planets:
            for p2 in self.planets:
                if p1 < p2:
                    diff = abs(self.planets[p1]['longitude'] - self.planets[p2]['longitude'])
                    if diff > 180:
                        diff = 360 - diff
                    aspects.append((p1, p2, diff))
        return aspects

    def get_response(self, query: str) -> str:
        query = query.lower()

        if "hello" in query or "hi" in query:
            return f"Hello {self.name}! How can I help you with your kundli analysis today?"

        elif "sun" in query:
            return f"The Sun is at {self.planets['Sun']['longitude']:.2f}°."

        elif "moon" in query:
            return f"The Moon is at {self.planets['Moon']['longitude']:.2f}°."

        elif "planets" in query:
            return "\n".join([f"{p}: {d['longitude']:.2f}°" for p, d in self.planets.items()])

        elif "birth" in query:
            return f"Name: {self.name}\nDOB: {self.birth_datetime}\nPlace: {self.place}"

        elif "aspects" in query:
            return "\n".join([f"{a[0]} - {a[1]}: {a[2]:.2f}°" for a in self.aspects])

        else:
            return "I can help you with planetary positions, aspects, and birth info. Ask me about the Sun, Moon, planets, or aspects."

    def get_planet_position(self, planet: str) -> float:
        return self.planets.get(planet, {}).get('longitude', 0.0)

    def get_aspects(self) -> List[Tuple[str, str, float]]:
        return self.aspects
