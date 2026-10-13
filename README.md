# 🇹🇷 turkey-postal-codes

[![Sponsor](https://img.shields.io/badge/Sponsor-uguraltinsoy-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/uguraltinsoy)

Türkiye posta kodları için **hızlı, bağımlılıksız ve çevrimdışı** Python kütüphanesi + JSON, CSV, SQL, SQLite, MongoDB ve XML formatlarında hazır veri seti.

> 💡 Eksik/hatalı kayıt görürseniz lütfen [issue](https://github.com/uguraltinsoy/turkey-postal-codes/issues) açın veya PR gönderin.

## Kurulum

```bash
pip install git+https://github.com/uguraltinsoy/turkey-postal-codes.git
```

## Kullanım

```python
import turkey_postal_codes as tpc

tpc.get("01040")          # {'il': 'Adana', 'ilce': 'Seyhan', 'plaka': 1}
tpc.get(1040)             # int de kabul edilir, başa 0 eklenir
tpc.get_city("01040")     # 'Adana'
tpc.get_district("01040") # 'Seyhan'
tpc.is_valid("00000")     # False

tpc.get_neighborhoods("01040")           # posta koduna ait mahalleler
tpc.search_by_city("ADANA")              # ildeki tüm kayıtlar
tpc.search_by_district("adana", "seyhan")
tpc.list_cities()                        # plaka sırasıyla iller
tpc.list_districts("İstanbul")
tpc.postal_codes_of("Adana", "Seyhan")   # benzersiz posta kodları
```

İl/ilçe aramaları **Türkçe harflere duyarlı ve büyük/küçük harf bağımsızdır** (`"İSTANBUL"` = `"istanbul"`, `"IĞDIR"` = `"ığdır"`).

Kendi veri klasörünüzü kullanmak için:

```python
from turkey_postal_codes import TurkeyPostalCodes
tpc = TurkeyPostalCodes(data_dir="/yol/veri")
```

## Veri Setleri

Dosyalar [`turkey_postal_codes/data`](turkey_postal_codes/data) altındadır ve doğrudan başka dillerde de kullanılabilir.

| Dosya | Yapı | Amaç |
|---|---|---|
| `posta_kodu_haritasi.json` | `{ "01040": { "il", "ilce", "plaka" } }` | Posta kodu → il/ilçe O(1) arama |
| `turkiye_posta_kodlari.json` | `[ { "plaka", "il", "ilce", "mahalle", "posta_kodu" } ]` | Mahalle bazlı tam liste |

## Hazır Formatlar (exports)

Python kullanmıyorsanız [`exports/`](exports) klasöründeki hazır dosyaları doğrudan kullanabilirsiniz (72.887 kayıt, 81 il):

| Format | Dosya | Kullanım |
|---|---|---|
| CSV / TSV | `exports/csv/turkiye_posta_kodlari.csv` / `.tsv` | Excel, Google Sheets, pandas (UTF-8 BOM) |
| MySQL / MariaDB | `exports/sql/mysql.sql` | `mysql -u root -p db < mysql.sql` (utf8mb4_turkish_ci) |
| PostgreSQL | `exports/sql/postgresql.sql` | `psql -d db -f postgresql.sql` |
| SQLite (SQL) | `exports/sql/sqlite.sql` | `sqlite3 db.sqlite < sqlite.sql` |
| SQLite (hazır DB) | `exports/sqlite/turkiye_posta_kodlari.db` | Doğrudan açıp sorgulayın |
| MongoDB | `exports/nosql/mongodb.ndjson` | `mongoimport -d db -c posta_kodlari --file mongodb.ndjson` |
| Hiyerarşik JSON | `exports/nosql/iller_hiyerarsik.json` | İl → İlçe → Mahalle ağacı (`mongoimport --jsonArray`) |
| XML | `exports/xml/turkiye_posta_kodlari.xml` | XML tabanlı sistemler |

Tüm SQL tablolarının adı `posta_kodlari`, kolonları `plaka, il, ilce, mahalle, posta_kodu`; `posta_kodu` ve `(il, ilce)` üzerinde index vardır.

## Test

```bash
python -m unittest discover tests
```

## Katkı

PR'lar memnuniyetle karşılanır. Veri düzeltmelerinde her iki JSON dosyasının da tutarlı kalmasına dikkat edin.

## Lisans

[GPL-3.0](LICENSE) © Uğur ALTINSOY
