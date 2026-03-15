#!/usr/bin/env python3
"""
ww_flags TTF → WOFF2 (только флаги стран)
Использование: python convert_flags.py ww_flags.ttf
"""

import sys
import os
import itertools
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.ttLib.woff2 import compress

def get_flag_unicodes():
    """Regional Indicator символы U+1F1E6–U+1F1FF (буквы A–Z для флагов)"""
    return list(range(0x1F1E6, 0x1F1FF + 1))

def get_all_flag_sequences():
    """Все двухбуквенные пары Regional Indicators (все возможные флаги)"""
    ri = list(range(0x1F1E6, 0x1F1FF + 1))
    sequences = []
    for a, b in itertools.product(ri, ri):
        sequences.append((a, b))
    return sequences

def subset_font(input_path):
    base = os.path.splitext(input_path)[0]
    output_ttf = base + "_flags.ttf"
    output_woff2 = base + "_flags.woff2"

    print(f"[*] Читаем: {input_path}")
    
    # Собираем все unicodes: Regional Indicators + ZWJ + VS16 на всякий случай
    flag_unicodes = get_flag_unicodes()
    extra = [0x200D, 0xFE0F]  # ZWJ, Variation Selector-16
    all_unicodes = flag_unicodes + extra

    unicode_str = ",".join(f"U+{cp:04X}" for cp in all_unicodes)

    print(f"[*] Сабсеттим — оставляем только Regional Indicators + флаговые лигатуры...")

    options = subset.Options()
    options.layout_features = ["*"]       # все фичи включая GSUB лигатуры
    options.glyph_names = True
    options.legacy_cmap = True
    options.notdef_glyph = True
    options.notdef_outline = True
    options.recommended_glyphs = False
    options.name_IDs = [1, 2, 4, 6]       # минимальные name записи
    options.drop_tables = []
    options.passthrough_tables = False

    font = subset.load_font(input_path, options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=all_unicodes)
    subsetter.subset(font)

    subset.save_font(font, output_ttf, options)
    print(f"[+] Сохранён TTF: {output_ttf} ({os.path.getsize(output_ttf) // 1024} KB)")

    print(f"[*] Конвертируем в WOFF2...")
    with open(output_ttf, "rb") as f_in, open(output_woff2, "wb") as f_out:
        compress(f_in, f_out)
    print(f"[+] Сохранён WOFF2: {output_woff2} ({os.path.getsize(output_woff2) // 1024} KB)")

    generate_html(output_woff2)

def generate_html(woff2_path):
    """Генерируем HTML страницу для теста всех флагов"""
    
    # Все ISO 3166-1 alpha-2 коды стран
    country_codes = [
        ("AC","Остров Вознесения"), ("AD","Андорра"), ("AE","ОАЭ"), ("AF","Афганистан"),
        ("AG","Антигуа и Барбуда"), ("AI","Ангилья"), ("AL","Албания"), ("AM","Армения"),
        ("AO","Ангола"), ("AQ","Антарктида"), ("AR","Аргентина"), ("AS","Американское Самоа"),
        ("AT","Австрия"), ("AU","Австралия"), ("AW","Аруба"), ("AX","Аландские острова"),
        ("AZ","Азербайджан"), ("BA","Босния и Герцеговина"), ("BB","Барбадос"), ("BD","Бангладеш"),
        ("BE","Бельгия"), ("BF","Буркина-Фасо"), ("BG","Болгария"), ("BH","Бахрейн"),
        ("BI","Бурунди"), ("BJ","Бенин"), ("BL","Сен-Бартелеми"), ("BM","Бермуды"),
        ("BN","Бруней"), ("BO","Боливия"), ("BQ","Карибские Нидерланды"), ("BR","Бразилия"),
        ("BS","Багамы"), ("BT","Бутан"), ("BV","Остров Буве"), ("BW","Ботсвана"),
        ("BY","Беларусь"), ("BZ","Белиз"), ("CA","Канада"), ("CC","Кокосовые острова"),
        ("CD","ДР Конго"), ("CF","ЦАР"), ("CG","Конго"), ("CH","Швейцария"),
        ("CI","Кот-д'Ивуар"), ("CK","Острова Кука"), ("CL","Чили"), ("CM","Камерун"),
        ("CN","Китай"), ("CO","Колумбия"), ("CP","Остров Клиппертон"), ("CR","Коста-Рика"),
        ("CU","Куба"), ("CV","Кабо-Верде"), ("CW","Кюрасао"), ("CX","Остров Рождества"),
        ("CY","Кипр"), ("CZ","Чехия"), ("DE","Германия"), ("DG","Диего-Гарсия"),
        ("DJ","Джибути"), ("DK","Дания"), ("DM","Доминика"), ("DO","Доминиканская Республика"),
        ("DZ","Алжир"), ("EA","Сеута и Мелилья"), ("EC","Эквадор"), ("EE","Эстония"),
        ("EG","Египет"), ("EH","Западная Сахара"), ("ER","Эритрея"), ("ES","Испания"),
        ("ET","Эфиопия"), ("EU","Европейский союз"), ("FI","Финляндия"), ("FJ","Фиджи"),
        ("FK","Фолклендские острова"), ("FM","Микронезия"), ("FO","Фарерские острова"),
        ("FR","Франция"), ("GA","Габон"), ("GB","Великобритания"), ("GD","Гренада"),
        ("GE","Грузия"), ("GF","Французская Гвиана"), ("GG","Гернси"), ("GH","Гана"),
        ("GI","Гибралтар"), ("GL","Гренландия"), ("GM","Гамбия"), ("GN","Гвинея"),
        ("GP","Гваделупа"), ("GQ","Экваториальная Гвинея"), ("GR","Греция"),
        ("GS","Южная Георгия"), ("GT","Гватемала"), ("GU","Гуам"), ("GW","Гвинея-Бисау"),
        ("GY","Гайана"), ("HK","Гонконг"), ("HM","Острова Херд и Макдональд"),
        ("HN","Гондурас"), ("HR","Хорватия"), ("HT","Гаити"), ("HU","Венгрия"),
        ("IC","Канарские острова"), ("ID","Индонезия"), ("IE","Ирландия"), ("IL","Израиль"),
        ("IM","Остров Мэн"), ("IN","Индия"), ("IO","Британская территория в Индийском океане"),
        ("IQ","Ирак"), ("IR","Иран"), ("IS","Исландия"), ("IT","Италия"),
        ("JE","Джерси"), ("JM","Ямайка"), ("JO","Иордания"), ("JP","Япония"),
        ("KE","Кения"), ("KG","Киргизия"), ("KH","Камбоджа"), ("KI","Кирибати"),
        ("KM","Коморы"), ("KN","Сент-Китс и Невис"), ("KP","Северная Корея"),
        ("KR","Южная Корея"), ("KW","Кувейт"), ("KY","Острова Кайман"), ("KZ","Казахстан"),
        ("LA","Лаос"), ("LB","Ливан"), ("LC","Сент-Люсия"), ("LI","Лихтенштейн"),
        ("LK","Шри-Ланка"), ("LR","Либерия"), ("LS","Лесото"), ("LT","Литва"),
        ("LU","Люксембург"), ("LV","Латвия"), ("LY","Ливия"), ("MA","Марокко"),
        ("MC","Монако"), ("MD","Молдова"), ("ME","Черногория"), ("MF","Сен-Мартен"),
        ("MG","Мадагаскар"), ("MH","Маршалловы острова"), ("MK","Северная Македония"),
        ("ML","Мали"), ("MM","Мьянма"), ("MN","Монголия"), ("MO","Макао"),
        ("MP","Северные Марианские острова"), ("MQ","Мартиника"), ("MR","Мавритания"),
        ("MS","Монтсеррат"), ("MT","Мальта"), ("MU","Маврикий"), ("MV","Мальдивы"),
        ("MW","Малави"), ("MX","Мексика"), ("MY","Малайзия"), ("MZ","Мозамбик"),
        ("NA","Намибия"), ("NC","Новая Каледония"), ("NE","Нигер"), ("NF","Остров Норфолк"),
        ("NG","Нигерия"), ("NI","Никарагуа"), ("NL","Нидерланды"), ("NO","Норвегия"),
        ("NP","Непал"), ("NR","Науру"), ("NU","Ниуэ"), ("NZ","Новая Зеландия"),
        ("OM","Оман"), ("PA","Панама"), ("PE","Перу"), ("PF","Французская Полинезия"),
        ("PG","Папуа — Новая Гвинея"), ("PH","Филиппины"), ("PK","Пакистан"), ("PL","Польша"),
        ("PM","Сен-Пьер и Микелон"), ("PN","Острова Питкэрн"), ("PR","Пуэрто-Рико"),
        ("PS","Палестина"), ("PT","Португалия"), ("PW","Палау"), ("PY","Парагвай"),
        ("QA","Катар"), ("RE","Реюньон"), ("RO","Румыния"), ("RS","Сербия"),
        ("RU","Россия"), ("RW","Руанда"), ("SA","Саудовская Аравия"), ("SB","Соломоновы острова"),
        ("SC","Сейшелы"), ("SD","Судан"), ("SE","Швеция"), ("SG","Сингапур"),
        ("SH","Острова Святой Елены"), ("SI","Словения"), ("SJ","Шпицберген"),
        ("SK","Словакия"), ("SL","Сьерра-Леоне"), ("SM","Сан-Марино"), ("SN","Сенегал"),
        ("SO","Сомали"), ("SR","Суринам"), ("SS","Южный Судан"), ("ST","Сан-Томе и Принсипи"),
        ("SV","Сальвадор"), ("SX","Синт-Мартен"), ("SY","Сирия"), ("SZ","Эсватини"),
        ("TA","Тристан-да-Кунья"), ("TC","Острова Теркс и Кайкос"), ("TD","Чад"),
        ("TF","Французские южные территории"), ("TG","Того"), ("TH","Таиланд"),
        ("TJ","Таджикистан"), ("TK","Токелау"), ("TL","Восточный Тимор"), ("TM","Туркменистан"),
        ("TN","Тунис"), ("TO","Тонга"), ("TR","Турция"), ("TT","Тринидад и Тобаго"),
        ("TV","Тувалу"), ("TW","Тайвань"), ("TZ","Танзания"), ("UA","Украина"),
        ("UG","Уганда"), ("UM","Внешние малые острова США"), ("UN","ООН"),
        ("US","США"), ("UY","Уругвай"), ("UZ","Узбекистан"), ("VA","Ватикан"),
        ("VC","Сент-Винсент и Гренадины"), ("VE","Венесуэла"), ("VG","Британские Виргинские острова"),
        ("VI","Виргинские острова США"), ("VN","Вьетнам"), ("VU","Вануату"),
        ("WF","Уоллис и Футуна"), ("WS","Самоа"), ("XK","Косово"), ("YE","Йемен"),
        ("YT","Майотта"), ("ZA","ЮАР"), ("ZM","Замбия"), ("ZW","Зимбабве"),
    ]

    def code_to_emoji(code):
        base = 0x1F1E6 - ord('A')
        return chr(base + ord(code[0])) + chr(base + ord(code[1]))

    rows = ""
    for code, name in country_codes:
        emoji = code_to_emoji(code)
        rows += f'<div class="flag-item"><span class="flag">{emoji}</span><span class="code">{code}</span><span class="name">{name}</span></div>\n'

    woff2_filename = os.path.basename(woff2_path)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ww_flags Flags Test</title>
<style>
  @font-face {{
    font-family: 'ww_flagsFlags';
    src: url('{woff2_filename}') format('woff2');
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Segoe UI', sans-serif;
    background: #1a1a2e;
    color: #eee;
    padding: 24px;
  }}

  h1 {{
    text-align: center;
    margin-bottom: 8px;
    font-size: 1.4em;
    color: #a0c4ff;
  }}

  .subtitle {{
    text-align: center;
    color: #888;
    font-size: 0.85em;
    margin-bottom: 24px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 8px;
  }}

  .flag-item {{
    background: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    padding: 10px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    transition: background 0.2s;
  }}

  .flag-item:hover {{
    background: #0f3460;
  }}

  .flag {{
    font-family: 'ww_flagsFlags', 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif;
    font-size: 2em;
    line-height: 1;
  }}

  .code {{
    font-size: 0.75em;
    color: #a0c4ff;
    font-weight: bold;
    letter-spacing: 1px;
  }}

  .name {{
    font-size: 0.65em;
    color: #888;
    text-align: center;
    line-height: 1.3;
  }}

  .stats {{
    text-align: center;
    margin-top: 20px;
    color: #555;
    font-size: 0.8em;
  }}
</style>
</head>
<body>
<h1>🏳 ww_flags Flags — тест шрифта</h1>
<p class="subtitle">Шрифт: {woff2_filename} | {len(country_codes)} флагов</p>
<div class="grid">
{rows}
</div>
<p class="stats">Если флаги отображаются корректно — шрифт работает ✓</p>
</body>
</html>"""

    html_path = os.path.join(os.path.dirname(woff2_path), "flags_test.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] HTML тест: {html_path}")
    print(f"\n[✓] Готово! Открой flags_test.html в браузере.")
    print(f"    HTML и WOFF2 должны лежать в одной папке.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python convert_flags.py ww_flags.ttf")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Файл не найден: {input_file}")
        sys.exit(1)
    
    subset_font(input_file)
