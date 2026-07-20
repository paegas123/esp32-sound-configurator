# TankSound Configurator - Roadmap

Tento soubor slouží jako trvalá "paměť" projektu napříč konverzacemi -
kdykoliv se ke konfigurátoru vrátíme, stačí ho nahrát a víme přesně, kde
jsme skončili a co je v plánu.

## Fáze 1 - terminálová verze (HOTOVO, ověřeno end-to-end)

Otestováno na reálném Macu i reálné ESP32 desce, výsledek: `[SUCCESS]`,
firmware úspěšně nahrán.

Co fáze 1 umí:
- [x] Automatické stažení originálu z GitHubu + kontrola aktualizací
      (`updater.py`)
- [x] Volba jazyka (cs/en/de) při prvním spuštění, uloží se natrvalo
      (`settings.py`, `i18n.py`, `lang/*.json`)
- [x] Výběr desky (Wemos D1 Mini ESP32 / standardní ESP32 Dev)
- [x] Výběr vozidla ze seznamu (82 originálních presetů)
- [x] Zobrazení a úprava parametrů vozidla v mateřském jazyce s
      vysvětlivkami (`vehicle_parser.py`, `param_translations.py`)
- [x] Zápis změn zpět do pracovní kopie projektu, beze změny čehokoliv
      jiného v souborech
- [x] Automatické připnutí kompatibilní verze ESP32 platformy
      (`espressif32 @ 6.0.1`) v `platformio.ini` - nejnovější verze
      odstranila `ledcSetup`/`ledcAttachPin`, na kterých staví knihovna
      `statusLED` (`platformio_ini.py`)
- [x] Automatické doinstalování chybějících Python balíčků, které
      PlatformIO potřebuje (`littlefs-python`, `fatfs-ng`, `pyyaml`),
      přímo do správného Python interpretu, i automatický retry při
      dalších podobných chybách (`pio_runner.py`)
- [x] Spuštění `pio run --target upload`

Známé drobnosti k doladění (nekritické):
- Jedna kategorie parametrů u IS-3 (kolem `dieselKnockVolumePercentage`)
  má "napůl uspokojivý" název kategorie, protože originální komentář
  v kódu nemá standardní formát nadpisu - kosmetická věc.

## Fáze 2 - rozšíření pokrytí (HOTOVO)

Cíl: rozšířit `param_translations.py` (překlady + vysvětlivky) z jednoho
vozidla (IS-3) na co nejvíc z 82 originálních presetů.

Výsledek: **100% pokrytí u všech 82 vozidel** (ověřeno automatickou
kontrolou - žádný parametr ani kategorie u žádného vozidla už nespadá
na anglický fallback komentář z kódu). Celkem 93 přeložených parametrů
a 39 přeložených kategorií (cs/en/de), díky tomu, že autor napříč
vozidly opakuje stejné názvy proměnných - stačilo doplnit 34 unikátních
parametrů a 16 kategorií, které chyběly po fázi 1 (kde byl plně
přeložený jen IS-3).

## Fáze 3 - GUI a distribuce (PROBÍHÁ)

Hotovo a otestováno end-to-end (backend i API, běží proti reálnému
staženému projektu):
- [x] **Konverze zvuků pro přehrávání** (`sound_convert.py`) - viz výše,
      otestováno na všech 562 zvukových souborech, 0 chyb.
- [x] **Lokální webserver + JSON API** (`web_server.py`) - jen vestavěné
      knihovny Pythonu (`http.server`), žádné externí závislosti.
      Otestované endpointy: jazyk, kontrola/stažení aktualizace, seznam
      vozidel, výběr vozidla + parsování parametrů, úprava parametru,
      uložení do souboru, přehrání zvuku (vrací platný .wav), zapnutí/
      vypnutí desky, spuštění nahrávání na pozadí s průběžným pollingem
      logu, spuštění/zastavení "sériového monitoru" (`pio device
      monitor`) na pozadí - včetně ověření, že se chybové stavy (např.
      chybějící `pio`) hlásí srozumitelně a neshazují server.
- [x] **Frontend** (`web/index.html`, `web/app.js`, `web/style.css`) -
      dle odsouhlaseného návrhu s uživatelem:
      - Harmonika (accordion) s kategoriemi místo 70 parametrů na jedné
        obrazovce - každá kategorie se rozbaluje samostatně pod sebou.
      - Klidná pastelová paleta barev (teplé krémové pozadí místo bílé,
        tlumené modrá/zelená/fialová/tyrkysová pro kategorie) - podloženo
        rešerší barevné psychologie (chladné tóny snižují kortizol,
        zelená šetří oči), s poznámkou, že jde o obecný, ne univerzální
        efekt.
      - Tlačítko **"Co modul právě dělá"** (žádný technický žargon) -
        funguje kdykoliv, nezávisle na zbytku programu, otevře živý
        výpis ze sériové linky.
      - Posuvník pro hlasitosti (0-300 %), zaškrtávátko pro přepínače a
        boolean hodnoty, rozbalovací seznam + tlačítko "Přehrát" pro
        výběr zvuku.
      - Samostatná tlačítka "Uložit změny" / "Nahrát do desky".
- [x] `gui.py` - spouštěcí skript, otevře výchozí prohlížeč automaticky
      (funguje stejně na Windows i Macu přes `webbrowser` modul).

- [x] **Barevné rozlišení parametrů podle důležitosti** (`param_tiers.py`)
      - 🔴 nešahat = jemné číselné doladění zvuku (hlasitosti, prahy,
        intervaly) - autor už vyladil, aby to znělo dobře dohromady.
      - 🟡 doporučeno nastavit = zapnutí/vypnutí funkce nebo výběr
        konkrétního zvukového souboru (turbo ano/ne, jaký klakson).
      - 🟢 nutno nastavit = věci vázané na fyzický hardware/ovládání
        (typ desky, PWM/PPM a ESC kalibrace, typ vozidla jako
        tank/rypadlo/jeřáb, zapojení světel) - špatná hodnota reálně
        rozbije funkčnost, ne jen zvuk.
      - Filtr nahoře stránky (3 barevné checkboxy) umožňuje jednotlivé
        úrovně schovat - nastavení se ukládá trvale (`settings.json`,
        klíč `filterVisibility`) a přežije vypnutí/zapnutí programu.
      - Otestováno na IS-3: `TRACKED_MODE`/ESC kalibrace/`MAX_RPM_PERCENTAGE`
        zelené, `REV_SOUND`/`automatic`/počet rychlostí žluté, hlasitosti
        červené - odpovídá domluvené logice. Filtr ukládá a načítá stav
        správně.

- [x] **Opravená logika barev podle zpětné vazby** — zelená teď znamená
      "tohle si má uživatel nastavit" (ne jen "je to hardwarové"), červená
      "nešahat, i experti tady varují", žlutá "volitelný styl/výběr".
      U ESC: baterie/odpory červené (autor varuje "může trvale poškodit"),
      běžná ESC/motor kalibrace zelená.
- [x] **Filtr NEOMEZUJE editaci** - i skrytá červená/žlutá položka jde
      stále upravit přes API stejně jako přes VSCode, filtr je jen
      viditelnostní pomůcka pro pohodlí, ne technické omezení.
- [x] **Univerzální parser rozšířen na dalších 7 nastavovacích souborů**
      (`0_generalSettings.h`, `3_ESC.h`, `4_Transmission.h`, `6_Lights.h`,
      `8_Sound.h`, `9_Dashboard.h`, `10_Trailer.h`) - stejný parser jako
      u vozidel, jen rozšířený o typ `float` (kvůli hodnotám baterie).
      Otestováno na všech 7 souborech, žádná chyba, žádná kolize názvů
      s vozidly.
- [x] **Dvě reálné chyby v parseru objeveny a opraveny při rozšiřování**
      (obě ověřeny regresním testem na všech 82 vozidlech, 0 chyb, 6650
      parametrů celkem):
      - Blokové komentáře `/* ... */` (autor je používá pro "vypnuté"
        drafty, např. `KenworthCummins335.h`) se dřív omylem parsovaly
        jako živý kód.
      - Drobné duplicity v originále (např. `R6` definované 2× vedle
        sebe) se dřív zobrazovaly jako 2 řádky v GUI - teď se bere jen
        první výskyt.
- [x] **Karty nahoře stránky** (`Vozidlo`, `Obecná nastavení`, `ESC a
      baterie`, `Převodovka`, `Světla`, `Zvuk (obecné)`, `Palubní deska`,
      `Přívěs`) - přepínání mezi nimi otestováno přes API, změny na jedné
      kartě neovlivní ostatní soubory (ověřeno diffem).
- [x] Přepínač jazyka za běhu (ikonka v horní liště, ne jen napoprvé).
- [x] Výběr vozidla seskupený podle kategorií z originálu (`<optgroup>`).
- [x] **Karta "Dálkové ovládání" (`2_Remote.h`)** - nový typ ovládacího
      prvku `flag_choice` (rádiová volba z `#define`, na rozdíl od
      `sound_choice`, který vybírá z `#include` řádků):
      - Výběr profilu vysílačky (15 možností: Flysky, Frsky, Graupner,
        Micro RC...) - zelené, jak jsme se domluvili.
      - Výběr komunikačního protokolu (PWM/SBUS/IBUS/SUMD/PPM) - PWM je
        "virtuální" volba (žádný ze 4 skutečných protokolů není aktivní),
        zvolení PWM správně vypne všechny 4 zároveň. Zelené.
      - Zbylé přepínače/čísla obarveny podle komentářů autora v kódu
        (`PROTOTYPE_36`/`EMBEDDED_SBUS` mají "nešahej" varování →
        červené; `sbusBaud` je běžná troubleshooting hodnota → zelené).
      - Otestováno na reálném souboru: přepnutí profilu i protokolu
        (včetně PWM), `diff` ukázal změnu přesně na očekávaných
        řádcích, nic jiného se nedotklo.
      - **Záměrně NEpokrývá** desítky bloků `#ifdef <PROFIL> ... #endif`
        s kalibrací jednotlivých kanálů (obsahují pole, která parser
        zatím neumí) - budoucí krok.

Zbývá:

- [ ] Zabalení do instalátorů pro Windows a Mac.
- [ ] Volitelné rozšíření o druhý ESC výstup pro pásová vozidla.
- [ ] Reálné vyzkoušení rozšířeného GUI (karty, filtr) na uživatelově Macu.

## Opravy po prvním reálném testování na Macu

- [x] **Bug: okno pro změnu jazyka nešlo zavřít ani v něm nic vybrat** -
      tlačítka jazyka se propojila s funkčností jen při úplně prvním
      spuštění programu. Přidáno i tlačítko "Zavřít".
- [x] **Chybějící názvy kategorií u ESC/Převodovka/Zvuk/Dashboard/Přívěs**
      - originál tam nemá žádný nadpis sekce. Teď mají fallback název
        "Nastavení" a navíc se rovnou automaticky rozbalí (nemusí se
        na ně klikat).
- [x] **Kompletní český/anglický/německý překlad i KRÁTKÝCH NÁZVŮ**
      parametrů (dřív byl vidět jen syrový anglický název proměnné jako
      "escPulseSpan", i když popisek pod ním už byl přeložený) - nový
      soubor `param_labels.py`, pokrývá všech 252 unikátních parametrů
      v celém programu (93 z vozidel + 159 z nových karet).
- [x] Doplněny i chybějící vysvětlivky a názvy kategorií (38 kategorií
      profilů Remote/Servos/Shaker, 6 kategorií Obecných nastavení).
      Ověřeno: 100% pokrytí, žádná regrese (82 vozidel, 6650 parametrů).
- [x] **Barvy kategorií podle sémaforu** (ne cyklované) + **filtr skryje
      celou kategorii**, pokud jsou v ní všechny položky vyfiltrované.
- [x] **Výběr profilu (Remote/Servos/Shaker) teď skutečně skryje ostatní
      profily** - dřív se zobrazovaly všechny najednou. Backend sleduje,
      kterému `#ifdef` bloku patří každý parametr, a posílá jen aktuálně
      vybraný profil + obecná nastavení.
- [x] **Přepracováno: barva a viditelnost teď vždy rozhoduje SLOŽKA
      (kategorie), ne jednotlivé položky uvnitř** - žádná šedá/smíšená
      barva už neexistuje, každá složka má vždy přesně jednu ze tří
      barev. Filtr schová celou složku podle její barvy, bez ohledu na
      to, jaké barvy mají položky uvnitř. Výchozí barva složky se počítá
      rozumně automaticky (zelená > žlutá > červená - pokud je uvnitř
      cokoliv zelené, aby to beginner neminul), ale jde ručně přebít v
      ladicím režimu tečkami v záhlaví složky. Opraven i bug, kdy
      "výběr zvuku" (přehrávání) mělo natvrdo sdílený prázdný klíč a
      backend ho omylem odmítal - teď má každý výběr zvuku vlastní klíč
      podle kategorie. Export teď obsahuje dvě sekce: `params` (jen
      informativní barva položky) a `categories` (rozhoduje o
      viditelnosti). Otestováno end-to-end.
- [x] **Filtr přepracován na jediný přepínač úrovně** (dřív 3 nezávislé
      checkboxy) - Začátečník (jen zelená) / Pokročilý (zelená+žlutá) /
      Expert (úplně vše) - kumulativní, vždy jen jeden aktivní najednou.
      Uloženo trvale (`settings.json`, klíč `levelMode`).
- [x] Doplněny chybějící překlady **popisků u výběru profilu vysílačky/
      serva/shakeru a komunikačního protokolu** (`OPTION_LABELS` v
      `param_labels.py`) - dřív se po rozbalení zobrazoval anglický
      text i v češtině. Ověřeno na kartě Dálkové ovládání.
- [x] **Vizuální tabulka "kanál → funkce"** pro dálkové ovládání - vždy
      viditelná nahoře karty, nezávisle na zvolené úrovni (i v režimu
      Začátečník), aby bylo jasné, co kam z přijímače zapojit. Přepočítá
      se automaticky podle vybraného profilu vysílačky (otestováno na
      Flysky FS-i6S vs. Graupner mz-12 - stejná funkce má u každého
      jinak přiřazené číslo kanálu). Nevyužité kanály (NONE) jsou
      zobrazené přeškrtnutě/ztlumeně. Krátká poznámka vysvětluje rozdíl
      mezi PWM (číslo = fyzický pin na desce) a SBUS/IBUS/SUMD/PPM
      (číslo = pořadí kanálu v datovém toku).
- [x] **Karty nahoře stránky mají teď taky barvu semaforu** (stejný
      systém jako kategorie) - Vozidlo a Dálkové ovládání zelené (vždy
      vidět), zbytek (Servo výstupy, ESC, Převodovka, Světla...) žlutý
      podle zjištění, že originál má u nich rozumné výchozí hodnoty
      zapsané do EEPROM jen při prvním startu (viz `eepromInit()`), tzn.
      nejsou nutné dotýkat se jich hned. V režimu Začátečník se tak
      zobrazí jen karta Vozidlo a Dálkové ovládání. Jde přebít v ladicím
      režimu (tečky u každé karty), export obsahuje i sekci `tabs`.
      Otestováno end-to-end.
- [x] **Poznámky v ladicím režimu** - u každé položky/kategorie/karty je
      teď v ladicím režimu i textové pole ("proč/na co změnit"), ukládá
      se nezávisle na barvě a exportuje se spolu s ní (soubor teď
      obsahuje `{"tier": ..., "note": ...}` u každého klíče).
- [x] **Nová karta "Web"** - zatím jen volba mezi původním webem autora
      a "novým" (zatím needěláno, disabled) - připraveno pro budoucí
      napojení, samotný nový web zatím neexistuje.
- [x] **Tabulka zapojení světel** (karta Světla) - stejný princip jako
      tabulka kanálů u dálkového ovládání, vždy viditelná nezávisle na
      úrovni. Piny zjištěné přímo ze zdrojového kódu (`src.ino`), včetně
      rozdílu podle typu desky (Wemos D1 Mini vs. standardní ESP32 Dev) -
      otestováno přepnutí desky, tabulka se správně přepočítá.
- [x] **Přepínač desky (Wemos D1 Mini) odstraněn z horní lišty** - zůstal
      jen jako běžný parametr v kartě Obecná nastavení (kam přirozeně
      patří), stejně jako všechno ostatní.
- [x] **Oprava: chybějící `channelAutoZero`/`channelReversed` (per-kanál)
      v `2_Remote.h`** - byla to víceřádková pole (17 hodnot, každá na
      vlastním řádku), která parser dřív vůbec neuměl číst. Parser teď
      zvládá i tenhle formát, každý kanál se zobrazí jako samostatné
      zaškrtávátko (17 na profil), zelené. `channelAutoZero` navíc má
      tlačítko "Vypnout pro všechny kanály" (hromadná akce),
      `channelReversed` záměrně ne (nedávalo by smysl). Prošel jsem
      systematicky všech 11 souborů - žádné další víceřádkové pole
      nikde jinde není. Otestováno: zápis prostředního i posledního
      prvku pole (jiný formát - poslední nemá čárku), hromadné
      vypnutí, izolace na aktivní profil - vše přes `diff` ověřeno.
      Regrese na všech 82 vozidlech i ostatních souborech čistá.
- [x] **Přejmenováno na "ESP32 Sound Configurator"** (ne "TankSound" -
      program není jen pro tanky). Podnadpis a odkaz na originální
      projekt (credit TheDIYGuy999) teď výraznější, jako barevný odkaz
      hned pod nadpisem, a mění se podle zvoleného jazyka.
- [x] **Připraveno sestavení skutečné aplikace** (`.app` pro Mac, `.exe`
      pro Windows) přes GitHub Actions - `esp32_sound_configurator.spec`
      (PyInstaller) + `.github/workflows/build.yml`. Opraveny cesty
      k přiloženým souborům (`web/`, `lang/`), aby fungovaly i po
      zabalení (nový `app_paths.py`, frozen-aware). Otestováno lokálně
      sestavením Linux verze (GitHub Actions sestaví skutečnou Mac/
      Windows verzi na dálku) - server po zabalení správně najde a
      servíruje přiložené soubory, API funguje. Datová složka
      uživatele přejmenována na `~/ESP32_Sound_Configurator`.

## Poznámky k architektuře (pro budoucí GUI)

Veškerá logika (parsování, editace, update mechanismus, řešení
závislostí) je už teď oddělená od terminálového rozhraní (`cli.py`) do
samostatných modulů (`vehicle_parser.py`, `updater.py`, `pio_runner.py`,
`platformio_ini.py`, `param_translations.py`, `settings.py`, `i18n.py`).
GUI vrstva (ať už to bude např. desktopová appka nebo webové rozhraní v
prohlížeči) by měla tyto moduly volat přímo, bez nutnosti cokoliv
přepisovat - `cli.py` je jen jeden konkrétní způsob, jak s nimi mluvit,
GUI bude jiný.
