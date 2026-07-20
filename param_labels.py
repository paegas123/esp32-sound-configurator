"""
Krátké přeložené názvy (labely) parametrů - na rozdíl od dlouhých
vysvětlivek v param_translations.py jde o pár slov, které se zobrazí
jako hlavní název řádku v GUI (to, co dřív bylo jen syrové anglické
jméno proměnné jako "escPulseSpan").

Stejný princip jako param_translations.py: klíčem je přesný název
proměnné/define z originálního kódu. Pokud pro daný parametr label
chybí, GUI spadne zpátky na syrové jméno proměnné - nikdy to nespadne.
"""

PARAM_LABELS: dict[str, dict[str, str]] = {
    # ============================================================
    # Vozidla (fáze 1/2) - krátké názvy k už existujícím vysvětlivkám
    # ============================================================
    "startVolumePercentage": {"cs": "Hlasitost startu", "en": "Start volume", "de": "Startlautstärke"},
    "idleVolumePercentage": {"cs": "Hlasitost volnoběhu", "en": "Idle volume", "de": "Standgaslautstärke"},
    "engineIdleVolumePercentage": {"cs": "Hlasitost volnoběhu (motor)", "en": "Idle volume (engine)", "de": "Standgaslautstärke (Motor)"},
    "fullThrottleVolumePercentage": {"cs": "Hlasitost při plném plynu", "en": "Full throttle volume", "de": "Vollgas-Lautstärke"},
    "REV_SOUND": {"cs": "Samostatný zvuk otáček", "en": "Separate rev sound", "de": "Separater Drehzahlsound"},
    "revVolumePercentage": {"cs": "Hlasitost vysokých otáček", "en": "Rev volume", "de": "Drehzahllautstärke"},
    "engineRevVolumePercentage": {"cs": "Hlasitost otáček (motor)", "en": "Rev volume (engine)", "de": "Drehzahllautstärke (Motor)"},
    "revSwitchPoint": {"cs": "Práh přepnutí na vysoké otáčky", "en": "Rev switch point", "de": "Umschaltpunkt Drehzahl"},
    "idleEndPoint": {"cs": "Konec volnoběhu", "en": "Idle end point", "de": "Standgas-Endpunkt"},
    "idleVolumeProportionPercentage": {"cs": "Podíl volnoběhu ve směsi", "en": "Idle mix proportion", "de": "Standgas-Mischanteil"},
    "JAKE_BRAKE_SOUND": {"cs": "Zvuk motorové brzdy", "en": "Jake brake sound", "de": "Motorbremsen-Sound"},
    "jakeBrakeVolumePercentage": {"cs": "Hlasitost motorové brzdy (max)", "en": "Jake brake volume (max)", "de": "Motorbremse Lautstärke (max)"},
    "jakeBrakeIdleVolumePercentage": {"cs": "Hlasitost motorové brzdy (klid)", "en": "Jake brake volume (idle)", "de": "Motorbremse Lautstärke (Standgas)"},
    "jakeBrakeMinRpm": {"cs": "Min. otáčky pro motorovou brzdu", "en": "Jake brake min. RPM", "de": "Motorbremse Mindestdrehzahl"},
    "dieselKnockVolumePercentage": {"cs": "Hlasitost dieselového klepání", "en": "Diesel knock volume", "de": "Diesel-Klopfen Lautstärke"},
    "dieselKnockIdleVolumePercentage": {"cs": "Klepání při volnoběhu", "en": "Knock volume at idle", "de": "Klopfen im Leerlauf"},
    "dieselKnockInterval": {"cs": "Interval klepání", "en": "Knock interval", "de": "Klopfintervall"},
    "dieselKnockStartPoint": {"cs": "Práh klepání", "en": "Knock start point", "de": "Klopf-Startpunkt"},
    "V8": {"cs": "Motor V8", "en": "V8 engine", "de": "V8-Motor"},
    "V2": {"cs": "Motor V2", "en": "V2 engine", "de": "V2-Motor"},
    "dieselKnockAdaptiveVolumePercentage": {"cs": "Hlasitost ostatních klepnutí", "en": "Other knocks volume", "de": "Lautstärke weiterer Klopfimpulse"},
    "turboVolumePercentage": {"cs": "Hlasitost turba", "en": "Turbo volume", "de": "Turbo-Lautstärke"},
    "turboIdleVolumePercentage": {"cs": "Turbo při volnoběhu", "en": "Turbo volume at idle", "de": "Turbo im Leerlauf"},
    "chargerVolumePercentage": {"cs": "Hlasitost kompresoru", "en": "Supercharger volume", "de": "Kompressor-Lautstärke"},
    "chargerIdleVolumePercentage": {"cs": "Kompresor při volnoběhu", "en": "Supercharger volume at idle", "de": "Kompressor im Leerlauf"},
    "chargerStartPoint": {"cs": "Práh kompresoru", "en": "Supercharger start point", "de": "Kompressor-Startpunkt"},
    "wastegateVolumePercentage": {"cs": "Hlasitost wastegate", "en": "Wastegate volume", "de": "Wastegate-Lautstärke"},
    "wastegateIdleVolumePercentage": {"cs": "Wastegate po uvolnění plynu", "en": "Wastegate after throttle release", "de": "Wastegate nach Gaswegnahme"},
    "fanVolumePercentage": {"cs": "Hlasitost ventilátoru", "en": "Fan volume", "de": "Lüfter-Lautstärke"},
    "fanIdleVolumePercentage": {"cs": "Ventilátor při volnoběhu", "en": "Fan volume at idle", "de": "Lüfter im Leerlauf"},
    "fanStartPoint": {"cs": "Práh ventilátoru", "en": "Fan start point", "de": "Lüfter-Startpunkt"},
    "GEARBOX_WHINING": {"cs": "Kvílení převodovky", "en": "Gearbox whining", "de": "Getriebeheulen"},
    "hornVolumePercentage": {"cs": "Hlasitost klaksonu", "en": "Horn volume", "de": "Hupenlautstärke"},
    "sirenVolumePercentage": {"cs": "Hlasitost sirény", "en": "Siren volume", "de": "Sirenenlautstärke"},
    "brakeVolumePercentage": {"cs": "Hlasitost brzdy", "en": "Brake volume", "de": "Bremsen-Lautstärke"},
    "parkingBrakeVolumePercentage": {"cs": "Hlasitost parkovací brzdy", "en": "Parking brake volume", "de": "Feststellbremse Lautstärke"},
    "shiftingVolumePercentage": {"cs": "Hlasitost řazení", "en": "Shifting volume", "de": "Schaltgeräusch-Lautstärke"},
    "sound1VolumePercentage": {"cs": "Hlasitost doplňkového zvuku", "en": "Additional sound volume", "de": "Lautstärke Zusatzsound"},
    "reversingVolumePercentage": {"cs": "Hlasitost couvání", "en": "Reversing volume", "de": "Rückwärtsfahr-Lautstärke"},
    "indicatorVolumePercentage": {"cs": "Hlasitost blinkru", "en": "Indicator volume", "de": "Blinker-Lautstärke"},
    "indicatorOn": {"cs": "Práh zapnutí blinkru", "en": "Indicator on threshold", "de": "Blinker-Einschaltschwelle"},
    "INDICATOR_DIR": {"cs": "Směr blinkru", "en": "Indicator direction", "de": "Blinkerrichtung"},
    "XENON_LIGHTS": {"cs": "Xenonový záblesk", "en": "Xenon flash", "de": "Xenon-Blitz"},
    "doubleFlashBlueLight": {"cs": "Typ blikání majáku", "en": "Blue light flash type", "de": "Blaulicht-Blinkmodus"},
    "escRampTimeFirstGear": {"cs": "Náběh v 1. rychlosti", "en": "Ramp time, 1st gear", "de": "Rampenzeit 1. Gang"},
    "escRampTimeSecondGear": {"cs": "Náběh ve 2. rychlosti", "en": "Ramp time, 2nd gear", "de": "Rampenzeit 2. Gang"},
    "escRampTimeThirdGear": {"cs": "Náběh ve 3. rychlosti", "en": "Ramp time, 3rd gear", "de": "Rampenzeit 3. Gang"},
    "escBrakeSteps": {"cs": "Rychlost brzdění ESC", "en": "ESC braking speed", "de": "ESC-Bremsgeschwindigkeit"},
    "escAccelerationSteps": {"cs": "Rychlost zrychlení ESC", "en": "ESC acceleration speed", "de": "ESC-Beschleunigungsgeschwindigkeit"},
    "automatic": {"cs": "Automatická převodovka", "en": "Automatic transmission", "de": "Automatikgetriebe"},
    "NumberOfAutomaticGears": {"cs": "Počet rychlostí", "en": "Number of gears", "de": "Anzahl der Gänge"},
    "doubleClutch": {"cs": "Dvouspojková převodovka", "en": "Double-clutch transmission", "de": "Doppelkupplungsgetriebe"},
    "shiftingAutoThrottle": {"cs": "Automatický plyn při řazení", "en": "Auto throttle while shifting", "de": "Automatisches Gas beim Schalten"},
    "clutchEngagingPoint": {"cs": "Práh zabrání spojky", "en": "Clutch engaging point", "de": "Kupplungs-Greifpunkt"},
    "MAX_RPM_PERCENTAGE": {"cs": "Maximální otáčky", "en": "Maximum RPM", "de": "Maximale Drehzahl"},
    "SUPER_SLOW": {"cs": "Velmi pomalá reakce", "en": "Very slow response", "de": "Sehr träge Reaktion"},
    "acc": {"cs": "Krok zrychlení", "en": "Acceleration step", "de": "Beschleunigungsschritt"},
    "dec": {"cs": "Krok zpomalení", "en": "Deceleration step", "de": "Verzögerungsschritt"},
    "TRACKED_MODE": {"cs": "Režim pásového vozidla", "en": "Tracked vehicle mode", "de": "Kettenfahrzeug-Modus"},
    "COUPLING_SOUND": {"cs": "Zvuk připojení přívěsu", "en": "Trailer coupling sound", "de": "Ankuppel-Sound"},
    "couplingVolumePercentage": {"cs": "Hlasitost připojení přívěsu", "en": "Coupling volume", "de": "Kuppel-Lautstärke"},
    "RPM_DEPENDENT_KNOCK": {"cs": "Klepání závislé na otáčkách", "en": "RPM-dependent knock", "de": "Drehzahlabhängiges Klopfen"},
    "minKnockVolumePercentage": {"cs": "Minimální hlasitost klepání", "en": "Minimum knock volume", "de": "Minimale Klopflautstärke"},
    "knockStartRpm": {"cs": "Otáčky startu klepání", "en": "Knock start RPM", "de": "Klopf-Startdrehzahl"},
    "R6": {"cs": "Motor R6", "en": "R6 engine", "de": "R6-Motor"},
    "R6_2": {"cs": "Motor R6 (varianta)", "en": "R6 engine (variant)", "de": "R6-Motor (Variante)"},
    "SEPARATE_FULL_BEAM": {"cs": "Dálková světla zvlášť", "en": "Separate high beam", "de": "Separates Fernlicht"},
    "trackRattleVolumePercentage": {"cs": "Hlasitost chrastění pásů", "en": "Track rattle volume", "de": "Kettenrasseln-Lautstärke"},
    "hydraulicPumpVolumePercentage": {"cs": "Hlasitost hydrauliky", "en": "Hydraulic pump volume", "de": "Hydraulikpumpen-Lautstärke"},
    "hydraulicFlowVolumePercentage": {"cs": "Hlasitost proudění kapaliny", "en": "Hydraulic flow volume", "de": "Hydraulikfluss-Lautstärke"},
    "bucketRattleVolumePercentage": {"cs": "Hlasitost chrastění lopaty", "en": "Bucket rattle volume", "de": "Schaufelrasseln-Lautstärke"},
    "V8_468": {"cs": "Motor V8 468", "en": "V8 468 engine", "de": "V8-468-Motor"},
    "LED_INDICATORS": {"cs": "LED blinkry", "en": "LED indicators", "de": "LED-Blinker"},
    "EXCAVATOR_MODE": {"cs": "Režim rypadla", "en": "Excavator mode", "de": "Bagger-Modus"},
    "INDICATOR_SIDE_MARKERS": {"cs": "Blinkry jako boční světla", "en": "Indicators as side markers", "de": "Blinker als Seitenmarkierung"},
    "LOADER_MODE": {"cs": "Režim nakladače", "en": "Loader mode", "de": "Lader-Modus"},
    "DUMP_BED": {"cs": "Sklápěcí korba", "en": "Dump bed", "de": "Kippmulde"},
    "TRACK_RATTLE_2": {"cs": "Druhý zvuk chrastění pásů", "en": "Second track rattle sound", "de": "Zweiter Kettenrasseln-Sound"},
    "trackRattle2VolumePercentage": {"cs": "Hlasitost 2. chrastění pásů", "en": "Second rattle volume", "de": "Lautstärke 2. Rasseln"},
    "pwmStrokeChainDriveTopSpeed": {"cs": "Max. rychlost pásového pohonu", "en": "Track drive top speed", "de": "Kettenantrieb Höchstgeschwindigkeit"},
    "pwmStrokeChainDriveStartRotation": {"cs": "Práh rozjezdu pásů", "en": "Track drive start threshold", "de": "Kettenantrieb Startschwelle"},
    "trackRattleIntervalMin": {"cs": "Min. interval chrastění", "en": "Min. rattle interval", "de": "Min. Rasselintervall"},
    "trackRattleIntervalMax": {"cs": "Max. interval chrastění", "en": "Max. rattle interval", "de": "Max. Rasselintervall"},
    "JAKEBRAKE_ENGINE_SLOWDOWN": {"cs": "Motorová brzda zpomaluje motor", "en": "Jake brake slows engine", "de": "Motorbremse verlangsamt Motor"},
    "TIRE_SQUEAL": {"cs": "Kvílení pneumatik", "en": "Tire squeal", "de": "Reifenquietschen"},
    "tireSquealVolumePercentage": {"cs": "Hlasitost kvílení pneumatik", "en": "Tire squeal volume", "de": "Reifenquietsch-Lautstärke"},
    "HYDROSTATIC_TRACK_MOTORS": {"cs": "Hydrostatické pásové motory", "en": "Hydrostatic track motors", "de": "Hydrostatische Kettenmotoren"},
    "CRANE_MODE": {"cs": "Režim jeřábu", "en": "Crane mode", "de": "Kran-Modus"},
    "engineManualOnOff": {"cs": "Ruční zapnutí/vypnutí motoru", "en": "Manual engine on/off", "de": "Manuelles Motor Ein/Aus"},
    "pwmSoundTrigger": {"cs": "Spouštění zvuku PWM signálem", "en": "PWM sound trigger", "de": "PWM-Sound-Auslösung"},
    "V8_MEDIUM": {"cs": "V8 středně hlasité klepání", "en": "V8 medium loud knock", "de": "V8 mittellautes Klopfen"},
    "STEAM_LOCOMOTIVE_MODE": {"cs": "Režim parní lokomotivy", "en": "Steam locomotive mode", "de": "Dampflokomotiv-Modus"},
    "AIRPLANE_MODE": {"cs": "Režim letadla", "en": "Airplane mode", "de": "Flugzeug-Modus"},

    # ============================================================
    # 0_generalSettings.h
    # ============================================================
    "WEMOS_D1_MINI_ESP32": {"cs": "Deska Wemos D1 Mini ESP32", "en": "Wemos D1 Mini ESP32 board", "de": "Wemos D1 Mini ESP32 Board"},
    "DEBUG": {"cs": "Ladicí výpis (obecný)", "en": "Debug output (general)", "de": "Debug-Ausgabe (allgemein)"},
    "CHANNEL_DEBUG": {"cs": "Ladicí výpis kanálů", "en": "Channel debug output", "de": "Kanal-Debug-Ausgabe"},
    "ESC_DEBUG": {"cs": "Ladicí výpis ESC", "en": "ESC debug output", "de": "ESC-Debug-Ausgabe"},
    "AUTO_TRANS_DEBUG": {"cs": "Ladicí výpis automatické převodovky", "en": "Automatic transmission debug", "de": "Debug Automatikgetriebe"},
    "MANUAL_TRANS_DEBUG": {"cs": "Ladicí výpis manuální převodovky", "en": "Manual transmission debug", "de": "Debug Schaltgetriebe"},
    "TRACKED_DEBUG": {"cs": "Ladicí výpis pásového režimu", "en": "Tracked mode debug", "de": "Debug Kettenmodus"},
    "SERVO_DEBUG": {"cs": "Ladicí výpis serv", "en": "Servo debug output", "de": "Servo-Debug-Ausgabe"},
    "ESPNOW_DEBUG": {"cs": "Ladicí výpis ESP-NOW", "en": "ESP-NOW debug output", "de": "ESP-NOW-Debug-Ausgabe"},
    "CORE_DEBUG": {"cs": "Ladicí výpis jádra (NIKDY nepoužívat)", "en": "Core debug (NEVER use)", "de": "Kern-Debug (NIEMALS verwenden)"},
    "eeprom_id": {"cs": "ID paměti EEPROM", "en": "EEPROM ID", "de": "EEPROM-ID"},
    "ERASE_EEPROM_ON_BOOT": {"cs": "Smazat paměť při startu (NEBEZPEČNÉ)", "en": "Erase EEPROM on boot (DANGEROUS)", "de": "EEPROM beim Start löschen (GEFÄHRLICH)"},
    "ENABLE_WIRELESS": {"cs": "Povolit WiFi/bezdrátové funkce", "en": "Enable WiFi/wireless features", "de": "WLAN/Funktionen aktivieren"},
    "USE_CSS": {"cs": "Použít CSS styl webu", "en": "Use website CSS styling", "de": "Website-CSS verwenden"},
    "MODERN_CSS": {"cs": "Moderní vzhled webu", "en": "Modern website look", "de": "Modernes Website-Design"},
    "default_ssid": {"cs": "Výchozí název WiFi sítě", "en": "Default WiFi name", "de": "Standard-WLAN-Name"},
    "default_password": {"cs": "Výchozí WiFi heslo", "en": "Default WiFi password", "de": "Standard-WLAN-Passwort"},

    # ============================================================
    # 3_ESC.h
    # ============================================================
    "QUICRUN_FUSION": {"cs": "ESC Hobbywing Quicrun Fusion", "en": "Hobbywing Quicrun Fusion ESC", "de": "Hobbywing Quicrun Fusion ESC"},
    "QUICRUN_16BL30": {"cs": "ESC Hobbywing Quicrun 16BL30", "en": "Hobbywing Quicrun 16BL30 ESC", "de": "Hobbywing Quicrun 16BL30 ESC"},
    "ESC_DIR": {"cs": "Otočit směr ESC", "en": "Reverse ESC direction", "de": "ESC-Richtung umkehren"},
    "HYDROSTATIC_MODE": {"cs": "Hydrostatický pohon", "en": "Hydrostatic drive mode", "de": "Hydrostatikantrieb-Modus"},
    "directionChangeLimit": {"cs": "Omezení při změně směru", "en": "Direction change limit", "de": "Richtungswechsel-Begrenzung"},
    "RZ7886_DRIVER_MODE": {"cs": "Budič motoru RZ7886", "en": "RZ7886 motor driver", "de": "RZ7886-Motortreiber"},
    "RZ7886_FREQUENCY": {"cs": "Frekvence RZ7886", "en": "RZ7886 frequency", "de": "RZ7886-Frequenz"},
    "RZ7886_DRAGBRAKE_DUTY": {"cs": "Brzdný výkon RZ7886", "en": "RZ7886 drag brake duty", "de": "RZ7886 Bremsleistung"},
    "brakeMargin": {"cs": "Brzdná rezerva (experimentální)", "en": "Brake margin (experimental)", "de": "Bremsreserve (experimentell)"},
    "escPulseSpan": {"cs": "Rozsah signálu ESC", "en": "ESC pulse span", "de": "ESC-Impulsbereich"},
    "escTakeoffPunch": {"cs": "Rozjezdový impuls ESC", "en": "ESC takeoff punch", "de": "ESC-Anfahrimpuls"},
    "escReversePlus": {"cs": "Přídavek pro couvání", "en": "Reverse power boost", "de": "Rückwärts-Leistungszugabe"},
    "crawlerEscRampTime": {"cs": "Náběh ESC (crawler)", "en": "Crawler ESC ramp time", "de": "Crawler-ESC-Rampenzeit"},
    "globalAccelerationPercentage": {"cs": "Celkové zrychlení (experimentální)", "en": "Global acceleration (experimental)", "de": "Globale Beschleunigung (experimentell)"},
    "BATTERY_PROTECTION": {"cs": "Ochrana baterie", "en": "Battery protection", "de": "Akkuschutz"},
    "CUTOFF_VOLTAGE": {"cs": "Vypínací napětí baterie", "en": "Battery cutoff voltage", "de": "Akku-Abschaltspannung"},
    "FULLY_CHARGED_VOLTAGE": {"cs": "Napětí plně nabité baterie", "en": "Fully charged voltage", "de": "Spannung bei voller Ladung"},
    "RECOVERY_HYSTERESIS": {"cs": "Hystereze obnovení", "en": "Recovery hysteresis", "de": "Erholungs-Hysterese"},
    "RESISTOR_TO_BATTTERY_PLUS": {"cs": "Odpor k plusu baterie", "en": "Resistor to battery plus", "de": "Widerstand zu Akku-Plus"},
    "RESISTOR_TO_GND": {"cs": "Odpor k zemi (GND)", "en": "Resistor to ground", "de": "Widerstand zu Masse"},
    "DIODE_DROP": {"cs": "Úbytek napětí na diodě", "en": "Diode voltage drop", "de": "Dioden-Spannungsabfall"},
    "outOfFuelVolumePercentage": {"cs": "Hlasitost hlášky 'došlo palivo'", "en": "Out-of-fuel message volume", "de": "Lautstärke 'Kraftstoff leer'"},

    # ============================================================
    # 4_Transmission.h
    # ============================================================
    "VIRTUAL_3_SPEED": {"cs": "Virtuální 3rychlostní převodovka", "en": "Virtual 3-speed gearbox", "de": "Virtuelles 3-Gang-Getriebe"},
    "VIRTUAL_16_SPEED_SEQUENTIAL": {"cs": "Virtuální 16rychlostní (nefunkční)", "en": "Virtual 16-speed (not working)", "de": "Virtuell 16-Gang (nicht funktionsfähig)"},
    "OVERDRIVE": {"cs": "Overdrive (rychloběh)", "en": "Overdrive", "de": "Overdrive"},
    "automaticReverseAccelerationPercentage": {"cs": "Zrychlení automatu při couvání", "en": "Automatic reverse acceleration", "de": "Automatik-Beschleunigung rückwärts"},
    "lowRangePercentage": {"cs": "Redukce (nízký rozsah)", "en": "Low range reduction", "de": "Geländeuntersetzung"},
    "SEMI_AUTOMATIC": {"cs": "Poloautomatická převodovka", "en": "Semi-automatic transmission", "de": "Halbautomatikgetriebe"},
    "MODE1_SHIFTING": {"cs": "Řazení přes MODE1", "en": "MODE1 shifting", "de": "MODE1-Schaltung"},
    "TRANSMISSION_NEUTRAL": {"cs": "Neutrál převodovky", "en": "Transmission neutral", "de": "Getriebe-Leerlauf"},
    "maxClutchSlippingRpm": {"cs": "Max. prokluz spojky (otáčky)", "en": "Max. clutch slipping RPM", "de": "Max. Kupplungsschlupf (Drehzahl)"},
    "DOUBLE_CLUTCH": {"cs": "Dvouspojková převodovka", "en": "Double-clutch gearbox", "de": "Doppelkupplungsgetriebe"},
    "HIGH_SLIPPINGPOINT": {"cs": "Vysoký bod prokluzu", "en": "High slipping point", "de": "Hoher Schlupfpunkt"},

    # ============================================================
    # 6_Lights.h
    # ============================================================
    "NEOPIXEL_ENABLED": {"cs": "Neopixel LED pásek", "en": "Neopixel LED strip", "de": "Neopixel-LED-Streifen"},
    "NEOPIXEL_ON_CH4": {"cs": "Neopixel na kanálu 4", "en": "Neopixel on channel 4", "de": "Neopixel auf Kanal 4"},
    "NEOPIXEL_COUNT": {"cs": "Počet LED (Neopixel)", "en": "Number of LEDs (Neopixel)", "de": "Anzahl LEDs (Neopixel)"},
    "NEOPIXEL_BRIGHTNESS": {"cs": "Jas Neopixel", "en": "Neopixel brightness", "de": "Neopixel-Helligkeit"},
    "MAX_POWER_MILLIAMPS": {"cs": "Max. proud Neopixel", "en": "Max. Neopixel current", "de": "Max. Neopixel-Strom"},
    "NEOPIXEL_HIGHBEAM": {"cs": "Neopixel jako dálková světla", "en": "Neopixel as high beam", "de": "Neopixel als Fernlicht"},
    "neopixelMode": {"cs": "Animace Neopixel", "en": "Neopixel animation mode", "de": "Neopixel-Animationsmodus"},
    "THIRD_BRAKELIGHT": {"cs": "Třetí brzdové světlo", "en": "Third brake light", "de": "Dritte Bremsleuchte"},
    "ROTATINGBEACON_ON_B1": {"cs": "Rotující maják na B1", "en": "Rotating beacon on B1", "de": "Rundumleuchte auf B1"},
    "INDICATOR_TOGGLING_MODE": {"cs": "Přepínací režim blinkrů", "en": "Indicator toggling mode", "de": "Blinker-Umschaltmodus"},
    "noCabLights": {"cs": "Bez světel v kabině", "en": "No cab lights", "de": "Keine Kabinenbeleuchtung"},
    "noFogLights": {"cs": "Bez mlhových světel", "en": "No fog lights", "de": "Keine Nebelscheinwerfer"},
    "xenonLights": {"cs": "Xenonová světla (efekt)", "en": "Xenon lights effect", "de": "Xenonlicht-Effekt"},
    "flickeringWileCranking": {"cs": "Blikání při startování", "en": "Flickering while cranking", "de": "Flackern beim Anlassen"},
    "ledIndicators": {"cs": "LED blinkry (okamžité)", "en": "LED indicators (instant)", "de": "LED-Blinker (sofort)"},
    "swap_L_R_indicators": {"cs": "Prohodit levý/pravý blinkr", "en": "Swap left/right indicators", "de": "Blinker links/rechts tauschen"},
    "indicatorsAsSidemarkers": {"cs": "Blinkry jako boční světla", "en": "Indicators as side markers", "de": "Blinker als Seitenmarkierung"},
    "separateFullBeam": {"cs": "Dálková světla zvlášť", "en": "Separate high beam", "de": "Separates Fernlicht"},
    "flashingBlueLight": {"cs": "Blikající modrý maják", "en": "Flashing blue light", "de": "Blinkendes Blaulicht"},
    "hazardsWhile5thWheelUnlocked": {"cs": "Výstražná světla při odjištění", "en": "Hazards while unlocked", "de": "Warnblinker bei entriegelter Kupplung"},
    "cabLightsBrightness": {"cs": "Jas světel v kabině", "en": "Cab lights brightness", "de": "Helligkeit Kabinenlicht"},
    "sideLightsBrightness": {"cs": "Jas obrysových světel", "en": "Side lights brightness", "de": "Helligkeit Seitenlicht"},
    "rearlightDimmedBrightness": {"cs": "Jas zadních světel (tlumený)", "en": "Rear lights brightness (dimmed)", "de": "Helligkeit Rücklicht (gedimmt)"},
    "rearlightParkingBrightness": {"cs": "Jas zadních světel (parkování)", "en": "Rear lights brightness (parking)", "de": "Helligkeit Rücklicht (Parken)"},
    "headlightParkingBrightness": {"cs": "Jas předních světel (parkování)", "en": "Headlight brightness (parking)", "de": "Helligkeit Frontlicht (Parken)"},
    "reversingLightBrightness": {"cs": "Jas couvacích světel", "en": "Reversing light brightness", "de": "Helligkeit Rückfahrlicht"},
    "fogLightBrightness": {"cs": "Jas mlhových světel", "en": "Fog light brightness", "de": "Helligkeit Nebelscheinwerfer"},

    # ============================================================
    # 8_Sound.h
    # ============================================================
    "NO_SIREN": {"cs": "Bez sirény", "en": "No siren", "de": "Keine Sirene"},
    "NO_INDICATOR_SOUND": {"cs": "Bez zvuku blinkru", "en": "No indicator sound", "de": "Kein Blinkerton"},
    "numberOfVolumeSteps": {"cs": "Počet úrovní hlasitosti", "en": "Number of volume steps", "de": "Anzahl Lautstärkestufen"},
    "masterVolumeCrawlerThreshold": {"cs": "Práh hlasitosti pro crawler", "en": "Crawler volume threshold", "de": "Lautstärkeschwelle Crawler"},
    "masterVolumePercentage": {"cs": "Úrovně celkové hlasitosti", "en": "Master volume steps", "de": "Gesamtlautstärke-Stufen"},

    # ============================================================
    # 9_Dashboard.h
    # ============================================================
    "SPI_DASHBOARD": {"cs": "SPI palubní deska", "en": "SPI dashboard", "de": "SPI-Armaturenbrett"},
    "FREVIC_DASHBOARD": {"cs": "Frevic palubní deska", "en": "Frevic dashboard", "de": "Frevic-Armaturenbrett"},
    "dashRotation": {"cs": "Natočení displeje", "en": "Display rotation", "de": "Display-Ausrichtung"},
    "MAX_REAL_SPEED": {"cs": "Max. reálná rychlost", "en": "Max. real speed", "de": "Max. reale Geschwindigkeit"},
    "RPM_MAX": {"cs": "Max. otáčky na budíku", "en": "Max. RPM on gauge", "de": "Max. Drehzahl am Zähler"},
    "manualGearRatios": {"cs": "Převodové poměry (ruční)", "en": "Manual gear ratios", "de": "Manuelle Übersetzungsverhältnisse"},

    # ============================================================
    # 10_Trailer.h
    # ============================================================
    "TRAILER_LIGHTS_TRAILER_PRESENCE_SWITCH_DEPENDENT": {"cs": "Světla přívěsu podle přítomnosti", "en": "Trailer lights by presence switch", "de": "Anhängerlicht nach Anwesenheitsschalter"},
    "defaultUseTrailer1": {"cs": "Používat přívěs 1", "en": "Use trailer 1", "de": "Anhänger 1 verwenden"},
    "defaultUseTrailer2": {"cs": "Používat přívěs 2", "en": "Use trailer 2", "de": "Anhänger 2 verwenden"},
    "defaultUseTrailer3": {"cs": "Používat přívěs 3", "en": "Use trailer 3", "de": "Anhänger 3 verwenden"},
    "defaultBroadcastAddress1": {"cs": "MAC adresa přívěsu 1", "en": "MAC address, trailer 1", "de": "MAC-Adresse Anhänger 1"},
    "defaultBroadcastAddress2": {"cs": "MAC adresa přívěsu 2", "en": "MAC address, trailer 2", "de": "MAC-Adresse Anhänger 2"},
    "defaultBroadcastAddress3": {"cs": "MAC adresa přívěsu 3", "en": "MAC address, trailer 3", "de": "MAC-Adresse Anhänger 3"},

    # ============================================================
    # 2_Remote.h - obecná nastavení
    # ============================================================
    "PROTOTYPE_36": {"cs": "36pinová deska (NEPOUŽÍVAT)", "en": "36-pin board (DO NOT USE)", "de": "36-Pin-Board (NICHT VERWENDEN)"},
    "sbusBaud": {"cs": "Rychlost SBUS (baud)", "en": "SBUS baud rate", "de": "SBUS-Baudrate"},
    "EMBEDDED_SBUS": {"cs": "Vestavěný SBUS kód", "en": "Embedded SBUS code", "de": "Eingebetteter SBUS-Code"},
    "sbusFailsafeTimeout": {"cs": "Časový limit SBUS failsafe", "en": "SBUS failsafe timeout", "de": "SBUS-Failsafe-Timeout"},
    "EXPONENTIAL_THROTTLE": {"cs": "Exponenciální plyn", "en": "Exponential throttle", "de": "Exponentielles Gas"},
    "EXPONENTIAL_STEERING": {"cs": "Exponenciální řízení", "en": "Exponential steering", "de": "Exponentielle Lenkung"},
    "CHANNEL_AVERAGING": {"cs": "Průměrování kanálů", "en": "Channel averaging", "de": "Kanal-Mittelwertbildung"},
    "sbusInverted": {"cs": "Invertovaný SBUS signál", "en": "Inverted SBUS signal", "de": "Invertiertes SBUS-Signal"},
    "pulseNeutral": {"cs": "Neutrální rozsah signálu", "en": "Neutral pulse range", "de": "Neutraler Impulsbereich"},
    "pulseSpan": {"cs": "Rozsah signálu (+/-)", "en": "Pulse span (+/-)", "de": "Impulsbereich (+/-)"},
    "AUTO_ENGINE_ON_OFF": {"cs": "Automatické zapnutí/vypnutí motoru", "en": "Automatic engine on/off", "de": "Automatisches Motor Ein/Aus"},
    "AUTO_INDICATORS": {"cs": "Automatické blinkry", "en": "Automatic indicators", "de": "Automatische Blinker"},
    "AUTO_LIGHTS": {"cs": "Automatická světla", "en": "Automatic lights", "de": "Automatisches Licht"},

    # Kanálové přiřazení (2_Remote.h, uvnitř profilů vysílačky)
    "STEERING": {"cs": "Kanál řízení", "en": "Steering channel", "de": "Lenkkanal"},
    "GEARBOX": {"cs": "Kanál přepínače převodovky", "en": "Gearbox switch channel", "de": "Getriebeschalter-Kanal"},
    "THROTTLE": {"cs": "Kanál plynu/brzdy", "en": "Throttle/brake channel", "de": "Gas-/Bremskanal"},
    "HORN": {"cs": "Kanál klaksonu/majáku", "en": "Horn/blue light channel", "de": "Hupen-/Blaulicht-Kanal"},
    "POT2": {"cs": "Kanál potenciometru 2", "en": "Potentiometer 2 channel", "de": "Potentiometer-2-Kanal"},
    "MODE1": {"cs": "Kanál přepínače Mode 1", "en": "Mode 1 switch channel", "de": "Mode-1-Schalterkanal"},
    "MODE2": {"cs": "Kanál přepínače Mode 2", "en": "Mode 2 switch channel", "de": "Mode-2-Schalterkanal"},
    "MOMENTARY1": {"cs": "Kanál tlačítka Momentary 1", "en": "Momentary 1 button channel", "de": "Momentary-1-Tasterkanal"},
    "HAZARDS": {"cs": "Kanál výstražných světel", "en": "Hazard lights channel", "de": "Warnblinker-Kanal"},
    "INDICATOR_LEFT": {"cs": "Kanál levého blinkru", "en": "Left indicator channel", "de": "Kanal linker Blinker"},
    "INDICATOR_RIGHT": {"cs": "Kanál pravého blinkru", "en": "Right indicator channel", "de": "Kanal rechter Blinker"},
    "CH_14": {"cs": "Kanál 14", "en": "Channel 14", "de": "Kanal 14"},
    "CH_15": {"cs": "Kanál 15", "en": "Channel 15", "de": "Kanal 15"},
    "CH_16": {"cs": "Kanál 16", "en": "Channel 16", "de": "Kanal 16"},
    "channelAutoZero": {"cs": "Automatické vynulování", "en": "Auto zero", "de": "Automatische Nullpunkteinstellung"},
    "channelReversed": {"cs": "Invertovaný kanál", "en": "Reversed channel", "de": "Invertierter Kanal"},
    "FUNCTION_L": {"cs": "Kanál doplňkových funkcí (levý)", "en": "Secondary function channel (left)", "de": "Zusatzfunktions-Kanal (links)"},
    "FUNCTION_R": {"cs": "Kanál doplňkových funkcí (pravý)", "en": "Secondary function channel (right)", "de": "Zusatzfunktions-Kanal (rechts)"},

    # ============================================================
    # 7_Servos.h
    # ============================================================
    "CH1L": {"cs": "Kanál 1 - vlevo", "en": "Channel 1 - left", "de": "Kanal 1 - links"},
    "CH1C": {"cs": "Kanál 1 - střed", "en": "Channel 1 - center", "de": "Kanal 1 - Mitte"},
    "CH1R": {"cs": "Kanál 1 - vpravo", "en": "Channel 1 - right", "de": "Kanal 1 - rechts"},
    "CH1_RAMP_TIME": {"cs": "Rychlost serva kanálu 1", "en": "Channel 1 servo speed", "de": "Servogeschwindigkeit Kanal 1"},
    "CH2L": {"cs": "Kanál 2 - vlevo", "en": "Channel 2 - left", "de": "Kanal 2 - links"},
    "CH2C": {"cs": "Kanál 2 - střed", "en": "Channel 2 - center", "de": "Kanal 2 - Mitte"},
    "CH2R": {"cs": "Kanál 2 - vpravo", "en": "Channel 2 - right", "de": "Kanal 2 - rechts"},
    "CH2_RAMP_TIME": {"cs": "Rychlost serva kanálu 2", "en": "Channel 2 servo speed", "de": "Servogeschwindigkeit Kanal 2"},
    "CH3L": {"cs": "Kanál 3 - vlevo", "en": "Channel 3 - left", "de": "Kanal 3 - links"},
    "CH3C": {"cs": "Kanál 3 - střed", "en": "Channel 3 - center", "de": "Kanal 3 - Mitte"},
    "CH3R": {"cs": "Kanál 3 - vpravo", "en": "Channel 3 - right", "de": "Kanal 3 - rechts"},
    "CH3_RAMP_TIME": {"cs": "Rychlost serva kanálu 3", "en": "Channel 3 servo speed", "de": "Servogeschwindigkeit Kanal 3"},
    "CH3_BEACON": {"cs": "Maják na kanálu 3", "en": "Beacon on channel 3", "de": "Blinklicht auf Kanal 3"},
    "CH4L": {"cs": "Kanál 4 - vlevo", "en": "Channel 4 - left", "de": "Kanal 4 - links"},
    "CH4C": {"cs": "Kanál 4 - střed", "en": "Channel 4 - center", "de": "Kanal 4 - Mitte"},
    "CH4R": {"cs": "Kanál 4 - vpravo", "en": "Channel 4 - right", "de": "Kanal 4 - rechts"},
    "CH4_RAMP_TIME": {"cs": "Rychlost serva kanálu 4", "en": "Channel 4 servo speed", "de": "Servogeschwindigkeit Kanal 4"},
    "ESC_L": {"cs": "ESC - vlevo", "en": "ESC - left", "de": "ESC - links"},
    "ESC_C": {"cs": "ESC - střed", "en": "ESC - center", "de": "ESC - Mitte"},
    "ESC_R": {"cs": "ESC - vpravo", "en": "ESC - right", "de": "ESC - rechts"},
    "ESC_MIN": {"cs": "ESC - minimum", "en": "ESC - minimum", "de": "ESC - Minimum"},
    "ESC_MAX": {"cs": "ESC - maximum", "en": "ESC - maximum", "de": "ESC - Maximum"},
    "MODE2_HYDRAULIC": {"cs": "Mode 2 - hydraulika", "en": "Mode 2 - hydraulic", "de": "Mode 2 - Hydraulik"},
    "MODE2_TRAILER_UNLOCKING": {"cs": "Mode 2 - odjištění přívěsu", "en": "Mode 2 - trailer unlocking", "de": "Mode 2 - Anhänger entriegeln"},
    "MODE2_WINCH": {"cs": "Mode 2 - naviják", "en": "Mode 2 - winch", "de": "Mode 2 - Seilwinde"},
    "NO_WINCH_DELAY": {"cs": "Bez zpoždění navijáku", "en": "No winch delay", "de": "Keine Seilwinden-Verzögerung"},
    "PINGON_MODE": {"cs": "Režim Pingon", "en": "Pingon mode", "de": "Pingon-Modus"},
    "SERVO_FREQUENCY": {"cs": "Frekvence serva", "en": "Servo frequency", "de": "Servofrequenz"},
    "STEERING_RAMP_TIME": {"cs": "Rychlost serva řízení", "en": "Steering servo speed", "de": "Lenkservo-Geschwindigkeit"},
    "boomDownwardsHydraulic": {"cs": "Hydraulika výložníku dolů", "en": "Boom downward hydraulic", "de": "Hydraulik Ausleger abwärts"},
    "reverseBoomSoundDirection": {"cs": "Obrátit směr zvuku výložníku", "en": "Reverse boom sound direction", "de": "Auslegersound-Richtung umkehren"},

    # ============================================================
    # 5_Shaker.h
    # ============================================================
    "shakerStart": {"cs": "Otřesy při startu", "en": "Shaker power at start", "de": "Vibration beim Start"},
    "shakerIdle": {"cs": "Otřesy při volnoběhu", "en": "Shaker power at idle", "de": "Vibration im Leerlauf"},
    "shakerFullThrottle": {"cs": "Otřesy při plném plynu", "en": "Shaker power at full throttle", "de": "Vibration bei Vollgas"},
    "shakerStop": {"cs": "Otřesy při vypnutí motoru", "en": "Shaker power at engine stop", "de": "Vibration beim Motorstopp"},
}


def get_param_label(name: str, lang: str, fallback: str) -> str:
    entry = PARAM_LABELS.get(name)
    if entry and lang in entry:
        return entry[lang]
    # Položka pole, např. "channelAutoZero[CH1]" -> zkusíme základní
    # název "channelAutoZero" + připojíme původní číslo kanálu.
    if "[" in name and name.endswith("]"):
        base, suffix = name[:-1].split("[", 1)
        base_entry = PARAM_LABELS.get(base)
        if base_entry and lang in base_entry:
            return f"{base_entry[lang]} - {suffix}"
    return fallback


OPTION_LABELS: dict[str, dict[str, str]] = {
    # --- 2_Remote.h: profily vysílačky ---
    "FLYSKY_FS_I6X": {"cs": "Flysky FS-i6X", "en": "Flysky FS-i6X", "de": "Flysky FS-i6X"},
    "FLYSKY_FS_I6S": {"cs": "Flysky FS-i6S", "en": "Flysky FS-i6S", "de": "Flysky FS-i6S"},
    "FLYSKY_FS_I6S_LOADER": {"cs": "Flysky FS-i6S pro nakladač Volvo L120H (BURNIE222) - použij protokol IBUS", "en": "Flysky FS-i6S for a Volvo L120H loader (BURNIE222) - use IBUS protocol", "de": "Flysky FS-i6S für einen Volvo L120H Lader (BURNIE222) - IBUS-Protokoll verwenden"},
    "FLYSKY_FS_I6S_DOZER": {"cs": "Flysky FS-i6S pro dozer - použij protokol IBUS", "en": "Flysky FS-i6S for a dozer - use IBUS protocol", "de": "Flysky FS-i6S für einen Dozer - IBUS-Protokoll verwenden"},
    "WB_EXCAVATOR": {"cs": "WB rypadlo - použij protokol SBUS", "en": "WB excavator - use SBUS protocol", "de": "WB-Bagger - SBUS-Protokoll verwenden"},
    "FLYSKY_FS_I6S_EXCAVATOR": {"cs": "Flysky FS-i6S pro rypadlo KABOLITE K336 - použij protokol IBUS", "en": "Flysky FS-i6S for a KABOLITE K336 excavator - use IBUS protocol", "de": "Flysky FS-i6S für einen KABOLITE K336 Bagger - IBUS-Protokoll verwenden"},
    "FRSKY_TANDEM_EXCAVATOR": {"cs": "Frsky Tandem XE pro hydraulické rypadlo - použij protokol SBUS", "en": "Frsky Tandem XE for a hydraulic excavator - use SBUS protocol", "de": "Frsky Tandem XE für einen Hydraulikbagger - SBUS-Protokoll verwenden"},
    "FRSKY_TANDEM_HARMONY_LOADER": {"cs": "Frsky Tandem XE pro Lukas Cajkar Harmony 370 - použij protokol SBUS", "en": "Frsky Tandem XE for the Lukas Cajkar Harmony 370 - use SBUS protocol", "de": "Frsky Tandem XE für den Lukas Cajkar Harmony 370 - SBUS-Protokoll verwenden"},
    "FRSKY_TANDEM_CRANE": {"cs": "Frsky Tandem XE pro terénní jeřáb Mushroom3D - použij protokol SBUS", "en": "Frsky Tandem XE for a Mushroom3D rough terrain crane - use SBUS protocol", "de": "Frsky Tandem XE für einen Mushroom3D-Geländekran - SBUS-Protokoll verwenden"},
    "FLYSKY_GT5": {"cs": "Flysky GT5 / Reely GT6 EVO / Absima CR6P", "en": "Flysky GT5 / Reely GT6 EVO / Absima CR6P", "de": "Flysky GT5 / Reely GT6 EVO / Absima CR6P"},
    "RGT_EX86100": {"cs": "MT-305 (dodáváno s crawlerem RGT EX86100) - použij protokol PWM", "en": "MT-305 (comes with the RGT EX86100 crawler) - use PWM protocol", "de": "MT-305 (im Lieferumfang des RGT EX86100 Crawlers) - PWM-Protokoll verwenden"},
    "GRAUPNER_MZ_12": {"cs": "Graupner MZ-12 PRO", "en": "Graupner MZ-12 PRO", "de": "Graupner MZ-12 PRO"},
    "MICRO_RC": {"cs": "DIY vysílačka \"Micro RC\" (verze auto) - nepoužívat se standardní vysílačkou!", "en": "DIY \"Micro RC\" remote (car-style) - don't use with a standard remote!", "de": "DIY-Sender \"Micro RC\" (Auto-Stil) - nicht mit einem Standardsender verwenden!"},
    "MICRO_RC_STICK": {"cs": "DIY vysílačka \"Micro RC\" (verze páka) - nepoužívat se standardní vysílačkou!", "en": "DIY \"Micro RC\" remote (stick-based) - don't use with a standard remote!", "de": "DIY-Sender \"Micro RC\" (Knüppel-basiert) - nicht mit einem Standardsender verwenden!"},
    "FLYSKY_FS_I6S_EXCAVATOR_TEST": {"cs": "Flysky FS-i6S pro rypadlo KABOLITE K336 (jen pro testování)", "en": "Flysky FS-i6S for a KABOLITE K336 excavator (testing only)", "de": "Flysky FS-i6S für einen KABOLITE K336 Bagger (nur zum Testen)"},

    # --- 2_Remote.h: komunikační protokol ---
    "PWM": {"cs": "Klasický PWM signál (žádný z ostatních protokolů níže není aktivní)", "en": "Classic PWM signal (none of the other protocols below are active)", "de": "Klassisches PWM-Signal (keines der anderen Protokolle unten ist aktiv)"},
    "SBUS_COMMUNICATION": {"cs": "SBUS (ovládací signály přichází přes rozhraní SBUS)", "en": "SBUS (control signals arrive via the SBUS interface)", "de": "SBUS (Steuersignale kommen über die SBUS-Schnittstelle)"},
    "IBUS_COMMUNICATION": {"cs": "IBUS (ovládací signály přichází přes rozhraní IBUS)", "en": "IBUS (control signals arrive via the IBUS interface)", "de": "IBUS (Steuersignale kommen über die IBUS-Schnittstelle)"},
    "SUMD_COMMUNICATION": {"cs": "SUMD (ovládací signály přichází přes rozhraní SUMD)", "en": "SUMD (control signals arrive via the SUMD interface)", "de": "SUMD (Steuersignale kommen über die SUMD-Schnittstelle)"},
    "PPM_COMMUNICATION": {"cs": "PPM (ovládací signály přichází přes rozhraní PPM)", "en": "PPM (control signals arrive via the PPM interface)", "de": "PPM (Steuersignale kommen über die PPM-Schnittstelle)"},

    # --- 7_Servos.h: profily serv ---
    "SERVOS_DEFAULT": {"cs": "Výchozí profil serv", "en": "Default servo profile", "de": "Standard-Servoprofil"},
    "SERVOS_LANDY_MN_MODEL": {"cs": "MN Model Land Rover Defender 1:12", "en": "MN Model Land Rover Defender 1:12", "de": "MN Model Land Rover Defender 1:12"},
    "SERVOS_LANDY_DOUBLE_EAGLE": {"cs": "Double Eagle Land Rover Defender 1:8", "en": "Double Eagle Land Rover Defender 1:8", "de": "Double Eagle Land Rover Defender 1:8"},
    "SERVOS_C34": {"cs": "WPL C34 Toyota Land Cruiser", "en": "WPL C34 Toyota Land Cruiser", "de": "WPL C34 Toyota Land Cruiser"},
    "SERVOS_URAL": {"cs": "WPL Ural", "en": "WPL Ural", "de": "WPL Ural"},
    "SERVOS_RGT_EX86100": {"cs": "RGT EX86100", "en": "RGT EX86100", "de": "RGT EX86100"},
    "SERVOS_ACTROS": {"cs": "Hercules Hobby Actros 3363", "en": "Hercules Hobby Actros 3363", "de": "Hercules Hobby Actros 3363"},
    "SERVOS_KING_HAULER": {"cs": "TAMIYA King Hauler", "en": "TAMIYA King Hauler", "de": "TAMIYA King Hauler"},
    "SERVOS_RACING_TRUCK": {"cs": "Carson Mercedes Racing Truck", "en": "Carson Mercedes Racing Truck", "de": "Carson Mercedes Racing Truck"},
    "SERVOS_MECCANO_DUMPER": {"cs": "Meccano 3 Ton Dumper", "en": "Meccano 3 Ton Dumper", "de": "Meccano 3 Ton Dumper"},
    "SERVOS_OPEN_RC_TRACTOR": {"cs": "Open RC Tractor", "en": "Open RC Tractor", "de": "Open RC Tractor"},
    "SERVOS_EXCAVATOR": {"cs": "Rypadlo s elektrickými akčními členy", "en": "Excavator with electric actuators", "de": "Bagger mit elektrischen Aktuatoren"},
    "SERVOS_EXCAVATOR_1060_ESC": {"cs": "Rypadlo s elektrickými akčními členy (ESC Hobbywing 1060)", "en": "Excavator with electric actuators (Hobbywing 1060 ESC)", "de": "Bagger mit elektrischen Aktuatoren (Hobbywing 1060 ESC)"},
    "SERVOS_HYDRAULIC_EXCAVATOR": {"cs": "Hydraulické rypadlo", "en": "Hydraulic excavator", "de": "Hydraulikbagger"},
    "SERVOS_WB_EXCAVATOR": {"cs": "WB rypadlo", "en": "WB excavator", "de": "WB-Bagger"},
    "SERVOS_CRANE": {"cs": "Terénní jeřáb Mushroom3D", "en": "Mushroom3D rough terrain crane", "de": "Mushroom3D-Geländekran"},

    # --- 5_Shaker.h: profily shakeru ---
    "GT_POWER_STOCK": {"cs": "GT-Power shaker s mosazným závažím (originál)", "en": "GT-Power shaker with brass weight (stock)", "de": "GT-Power-Shaker mit Messinggewicht (Original)"},
    "GT_POWER_PLASTIC": {"cs": "GT-Power shaker s 3D tištěným plastovým závažím", "en": "GT-Power shaker with 3D printed plastic weight", "de": "GT-Power-Shaker mit 3D-gedrucktem Kunststoffgewicht"},
}


def get_option_label(name: str, lang: str, fallback: str) -> str:
    entry = OPTION_LABELS.get(name)
    if entry and lang in entry:
        return entry[lang]
    return fallback
