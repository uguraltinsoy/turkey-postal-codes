"""Türkiye posta kodları için hızlı ve çevrimdışı sorgulama kütüphanesi."""

from .core import TurkeyPostalCodes, normalize, normalize_postal_code

__version__ = "1.0.0"

# Varsayılan hazır instance (veriler ilk çağrıda yüklenir)
_default = TurkeyPostalCodes()

get = _default.get
get_city = _default.get_city
get_district = _default.get_district
get_neighborhoods = _default.get_neighborhoods
is_valid = _default.is_valid
search_by_city = _default.search_by_city
search_by_district = _default.search_by_district
list_cities = _default.list_cities
list_districts = _default.list_districts
postal_codes_of = _default.postal_codes_of

__all__ = [
    "TurkeyPostalCodes",
    "normalize",
    "normalize_postal_code",
    "get",
    "get_city",
    "get_district",
    "get_neighborhoods",
    "is_valid",
    "search_by_city",
    "search_by_district",
    "list_cities",
    "list_districts",
    "postal_codes_of",
]