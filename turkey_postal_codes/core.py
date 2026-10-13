"""Türkiye posta kodu sorgulama çekirdeği."""

import json
import os
import unicodedata
from typing import Any, Dict, List, Optional

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
_MAP_FILE = "posta_kodu_haritasi.json"
_LIST_FILE = "turkiye_posta_kodlari.json"


def normalize(text: Any) -> str:
    """Türkçe karakterlere duyarlı, büyük/küçük harf bağımsız karşılaştırma anahtarı üretir.

    'İSTANBUL', 'istanbul' ve 'İstanbul' aynı anahtarı verir.
    """
    s = str(text or "").strip()
    s = s.replace("İ", "i").replace("I", "ı")
    s = unicodedata.normalize("NFC", s.lower())
    # Bazı kaynaklarda görülen "i̇" (i + birleşik nokta) bozulmasını temizle
    s = s.replace("\u0307", "")
    return " ".join(s.split())


def normalize_postal_code(postal_code: Any) -> Optional[str]:
    """Girdiyi 5 haneli posta kodu metnine çevirir. Geçersizse None döner."""
    code = str(postal_code).strip().replace(" ", "")
    if not code.isdigit() or len(code) > 5:
        return None
    return code.zfill(5)


class TurkeyPostalCodes:
    """Çevrimdışı Türkiye posta kodu sorgulayıcı.

    Veri dosyaları ilk ihtiyaç anında yüklenir (lazy loading).
    """

    def __init__(self, data_dir: Optional[str] = None) -> None:
        self._data_dir = data_dir or _DATA_DIR
        self._code_map: Optional[Dict[str, Dict[str, Any]]] = None
        self._full_list: Optional[List[Dict[str, Any]]] = None
        self._city_index: Optional[Dict[str, List[Dict[str, Any]]]] = None

    # ------------------------------------------------------------------ #
    # Yükleme
    # ------------------------------------------------------------------ #
    def _read_json(self, filename: str) -> Any:
        path = os.path.join(self._data_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Veri dosyası bulunamadı: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def code_map(self) -> Dict[str, Dict[str, Any]]:
        if self._code_map is None:
            self._code_map = self._read_json(_MAP_FILE)
        return self._code_map

    @property
    def records(self) -> List[Dict[str, Any]]:
        if self._full_list is None:
            self._full_list = self._read_json(_LIST_FILE)
        return self._full_list

    def _cities(self) -> Dict[str, List[Dict[str, Any]]]:
        if self._city_index is None:
            index: Dict[str, List[Dict[str, Any]]] = {}
            for item in self.records:
                index.setdefault(normalize(item.get("il")), []).append(item)
            self._city_index = index
        return self._city_index

    # ------------------------------------------------------------------ #
    # Posta kodu ile sorgulama
    # ------------------------------------------------------------------ #
    def get(self, postal_code: Any) -> Optional[Dict[str, Any]]:
        """Posta kodundan il, ilçe ve plaka bilgisini döner.

        >>> TurkeyPostalCodes().get("34519")
        {'il': 'İstanbul', 'ilce': 'Esenyurt', 'plaka': 34}
        """
        code = normalize_postal_code(postal_code)
        if code is None:
            return None
        result = self.code_map.get(code)
        return dict(result) if result else None

    def get_city(self, postal_code: Any, default: Optional[str] = None) -> Optional[str]:
        """Posta kodunun bağlı olduğu il adını döner."""
        res = self.get(postal_code)
        return res["il"] if res else default

    def get_district(self, postal_code: Any, default: Optional[str] = None) -> Optional[str]:
        """Posta kodunun bağlı olduğu ilçe adını döner."""
        res = self.get(postal_code)
        return res["ilce"] if res else default

    def get_neighborhoods(self, postal_code: Any) -> List[Dict[str, Any]]:
        """Posta koduna ait tüm mahalle kayıtlarını döner."""
        code = normalize_postal_code(postal_code)
        if code is None:
            return []
        return [item for item in self.records if item.get("posta_kodu") == code]

    def is_valid(self, postal_code: Any) -> bool:
        """Posta kodu veri setinde mevcut mu?"""
        return self.get(postal_code) is not None

    # ------------------------------------------------------------------ #
    # İl / ilçe ile arama
    # ------------------------------------------------------------------ #
    def search_by_city(self, city_name: str) -> List[Dict[str, Any]]:
        """Bir ildeki tüm kayıtları döner (Türkçe harf duyarsız)."""
        return list(self._cities().get(normalize(city_name), []))

    def search_by_district(self, city_name: str, district_name: str) -> List[Dict[str, Any]]:
        """Bir il ve ilçedeki tüm mahalle / posta kodu kayıtlarını döner."""
        dist = normalize(district_name)
        return [item for item in self.search_by_city(city_name) if normalize(item.get("ilce")) == dist]

    def list_cities(self) -> List[str]:
        """Veri setindeki illeri plaka sırasına göre döner."""
        seen: Dict[str, int] = {}
        for item in self.records:
            seen.setdefault(item["il"], item.get("plaka", 0))
        return sorted(seen, key=lambda c: seen[c])

    def list_districts(self, city_name: str) -> List[str]:
        """Bir ilin ilçelerini alfabetik döner."""
        return sorted({item["ilce"] for item in self.search_by_city(city_name)}, key=normalize)

    def postal_codes_of(self, city_name: str, district_name: Optional[str] = None) -> List[str]:
        """Bir il (ve isteğe bağlı ilçe) için benzersiz posta kodlarını döner."""
        items = (
            self.search_by_district(city_name, district_name)
            if district_name
            else self.search_by_city(city_name)
        )
        return sorted({item["posta_kodu"] for item in items})