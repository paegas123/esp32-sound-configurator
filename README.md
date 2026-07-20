# TankSound Configurator

Nástroj, který ti pomůže nastavit a nahrát originální projekt
[TheDIYGuy999/Rc_Engine_Sound_ESP32](https://github.com/TheDIYGuy999/Rc_Engine_Sound_ESP32),
aniž bys musel ručně editovat kód. Dvě varianty:

- **`cli.py`** - terminálová verze (fáze 1), plně funkční a otestovaná.
- **`gui.py`** - grafická (webová) verze (fáze 3), běží v prohlížeči,
  ovládá se posuvníky/zaškrtávátky/rozbalovacími seznamy, umí přehrát
  zvuky a sledovat živý výpis z modulu.

## Co je potřeba

- Python 3.9+ (obě varianty používají jen vestavěné knihovny Pythonu -
  žádné `pip install` navíc)
- PlatformIO Core nainstalované a dostupné v terminálu jako `pio`
- Internetové připojení aspoň při prvním spuštění (stažení originálu z GitHubu)

## Jak spustit grafickou verzi (doporučeno)

**Nejjednodušší (Mac):** dvojklik na `Spustit.command` ve složce. Otevře
se na chvíli Terminál (ukazuje, co se děje - to je normální, nic
nemusíš psát) a pak se sám otevře prohlížeč. Poprvé možná macOS zeptá
na potvrzení bezpečnosti (Nastavení -> Soukromí a zabezpečení -> "Přesto
otevřít").

**Nebo ručně:**
```bash
cd tanksound_configurator
python3 gui.py
```

Automaticky se otevře výchozí prohlížeč na správné adrese (funguje
stejně na Windows i Macu). Při prvním spuštění se zeptá na jazyk.

Ovládání:
- Nahoře vyber vozidlo a typ desky.
- Tlačítko **"Co modul právě dělá"** kdykoliv otevře živý výpis toho, co
  modul posílá po USB - funguje nezávisle na zbytku programu.
- Parametry jsou seskupené do kategorií, které se rozbalují jednotlivě
  (klikni na název kategorie) - nemusíš se prokousávat všemi najednou.
- U výběru zvuku můžeš kliknout na "Přehrát" a rovnou si ho poslechnout,
  než se rozhodneš.
- **Uložit změny** zapíše úpravy do pracovního projektu.
- **Nahrát do desky** spustí `pio run --target upload` a průběžně
  ukazuje výstup.

## Jak získat skutečnou aplikaci (.app pro Mac / .exe pro Windows)

V balíčku je připravené vše potřebné (`esp32_sound_configurator.spec`,
`.github/workflows/build.yml`), aby GitHub sám na dálku (na skutečném
Macu i Windows serveru, zdarma) sestavil pořádnou dvojklikovou aplikaci
- žádné okno Terminálu, žádný Python netřeba mít nainstalovaný.

1. Na [github.com](https://github.com) vytvoř nové **prázdné** úložiště
   (New repository) - stačí veřejné, klidně pojmenuj třeba
   `esp32-sound-configurator`.
2. Nahraj do něj celý obsah tohodle balíčku (buď přetažením souborů na
   webu GitHubu přes "Add file → Upload files", nebo přes `git push`,
   pokud jsi zvyklý).
3. Jakmile se soubory nahrají do větve `main`, GitHub sám spustí
   sestavení (záložka **Actions** nahoře na stránce úložiště). Trvá to
   pár minut.
4. Až běh doběhne (zelené zaškrtnutí), klikni na něj a dole najdeš
   **Artifacts**: `ESP32-Sound-Configurator-Mac` a
   `ESP32-Sound-Configurator-Windows` - stáhni si ten pro svůj počítač.
5. Rozbal stažený ZIP - uvnitř bude buď `ESP32 Sound Configurator.app`
   (Mac), nebo `ESP32 Sound Configurator.exe` (Windows). Přetáhni si to
   třeba do Aplikací / na plochu a spouštěj normálním dvojklikem.

**Mac napoprvé:** macOS se zeptá, jestli aplikaci opravdu chceš spustit
(není podepsaná placeným Apple certifikátem) - klikni pravým tlačítkem
na appku → Otevřít → potvrdit. Stačí udělat jen jednou.

## Jak spustit terminálovou verzi

```bash
cd tanksound_configurator
python3 cli.py
```

## Co program dělá automaticky (bez zásahu uživatele) - platí pro obě verze

- Stáhne originál z GitHubu a kontroluje aktualizace.
- **Připne kompatibilní verzi ESP32 platformy** (`espressif32 @ 6.0.1`) v
  `platformio.ini` pracovní kopie - nejnovější verze totiž odstranila
  starší funkce (`ledcSetup`, `ledcAttachPin`), na kterých staví některé
  knihovny použité tímto projektem, takže by kompilace jinak vždy spadla.
- **Doinstaluje chybějící Python balíčky, které PlatformIO potřebuje**
  pro nejnovější verze ESP32 platforem (`littlefs-python`, `fatfs-ng`,
  `pyyaml`) - přímo do toho Python interpretu, pod kterým `pio` reálně
  běží (zjištěno automaticky ze shebang řádku spustitelného souboru `pio`).
- Pokud i přesto během `pio run --target upload` narazí na chybu typu
  `ModuleNotFoundError: No module named 'xxx'`, program tento balíček
  sám doinstaluje a nahrávání automaticky zopakuje (až 5 pokusů).

Uživatel tedy nemusí sám spouštět žádný `pip install` příkaz ani ručně
upravovat `platformio.ini`.

## Co program (zatím) nevyřeší sám

- **Fyzické problémy s USB připojením** (deska nereaguje, port zabraný
  jiným programem, potřeba podržet tlačítko BOOT při nahrávání apod.) -
  to je hardwarová/ovladačová záležitost mimo dosah Python skriptu.

## Aktuální stav překladů

Kompletní český/anglický/německý překlad názvů a vysvětlivek parametrů
pokrývá **všech 82 originálních vozidel** (93 parametrů + 39 kategorií).
Pokud by autor originálu časem přidal nové vozidlo s úplně novým
parametrem, program u něj zobrazí jako vysvětlivku originální anglický
komentář z kódu - takže nikdy nezůstaneš bez informace, co daná hodnota
znamená.

## Ověřeno v praxi

- **Terminálová verze**: celý běh otestován na reálném Macu i reálné
  ESP32 desce, od stažení originálu až po úspěšné nahrání firmwaru
  (`[SUCCESS]`, RAM 15 %, Flash 36,5 %).
- **Grafická verze**: backend a API otestované end-to-end (výběr
  vozidla, úprava parametru, uložení do souboru, přehrání zvuku jako
  platný .wav, zapnutí/vypnutí desky, spuštění úloh na pozadí s
  průběžným výpisem) - zatím ne na reálném Macu s prohlížečem, to je
  další krok.

