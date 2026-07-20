"""
Překlady a vysvětlivky pro parametry vozidel.

Princip: klíčem je přesný název proměnné/define v originálním kódu (např.
"startVolumePercentage"), protože ten je napříč vozidly velmi konzistentní
(TheDIYGuy999 používá stejné názvy proměnných ve všech presetech vozidel).
Pokud pro daný parametr překlad chybí (u vozidel mimo pilotní IS3 se to
u méně obvyklých parametrů může stát), program automaticky spadne zpět
na originální anglický komentář z kódu - nikdy nezůstane bez vysvětlení.

Podobně CATEGORY_TRANSLATIONS překládá nadpisy sekcí. Pokud konkrétní
nadpis neznáme, zobrazí se v angličtině tak, jak je v originále.
"""

# name -> {"cs": ..., "en": ..., "de": ...}
PARAM_TRANSLATIONS: dict[str, dict[str, str]] = {
    "startVolumePercentage": {
        "cs": "Hlasitost zvuku startu motoru (v % základní hlasitosti nahrávky)",
        "en": "Volume of the engine start sound (in % of the recording's base volume)",
        "de": "Lautstärke des Motorstart-Sounds (in % der Grundlautstärke der Aufnahme)",
    },
    "idleVolumePercentage": {
        "cs": "Celková hlasitost zvuku volnoběhu",
        "en": "Overall volume of the idle sound",
        "de": "Gesamtlautstärke des Standgas-Sounds",
    },
    "engineIdleVolumePercentage": {
        "cs": "Hlasitost volnoběhu závislá na otevření plynu (motorová složka)",
        "en": "Throttle-dependent idle volume (engine component)",
        "de": "Gasabhängige Standgaslautstärke (Motoranteil)",
    },
    "fullThrottleVolumePercentage": {
        "cs": "Hlasitost při plném plynu (týká se volnoběhu i vysokých otáček)",
        "en": "Volume at full throttle (applies to idle and rev sound)",
        "de": "Lautstärke bei Vollgas (betrifft Standgas- und Drehzahlsound)",
    },
    "REV_SOUND": {
        "cs": "Používat samostatný zvuk pro vysoké otáčky motoru (odděleně od volnoběhu)",
        "en": "Use a separate sound for high engine revs (independent of idle)",
        "de": "Separaten Sound für hohe Motordrehzahl verwenden (unabhängig vom Standgas)",
    },
    "revVolumePercentage": {
        "cs": "Celková hlasitost zvuku vysokých otáček",
        "en": "Overall volume of the rev sound",
        "de": "Gesamtlautstärke des Drehzahl-Sounds",
    },
    "engineRevVolumePercentage": {
        "cs": "Hlasitost vysokých otáček závislá na plynu (motorová složka)",
        "en": "Throttle-dependent rev volume (engine component)",
        "de": "Gasabhängige Drehzahllautstärke (Motoranteil)",
    },
    "revSwitchPoint": {
        "cs": "Práh otáček, nad kterým se přehrává zvuk vysokých otáček místo volnoběhu",
        "en": "RPM threshold above which the rev sound plays instead of idle",
        "de": "Drehzahlschwelle, ab der statt Standgas der Drehzahlsound abgespielt wird",
    },
    "idleEndPoint": {
        "cs": "Práh otáček, nad kterým zní zvuk už jen na 100 % vysokých otáček (0 % volnoběhu)",
        "en": "RPM threshold above which the sound is 100% rev (0% idle)",
        "de": "Drehzahlschwelle, ab der der Sound zu 100% Drehzahl (0% Standgas) ist",
    },
    "idleVolumeProportionPercentage": {
        "cs": "Podíl volnoběhu ve zvukové směsi pod prahovou hodnotou (zbytek je vysoké otáčky)",
        "en": "Proportion of idle sound in the mix below the threshold (rest is rev sound)",
        "de": "Anteil des Standgas-Sounds unterhalb der Schwelle (Rest ist Drehzahlsound)",
    },
    "JAKE_BRAKE_SOUND": {
        "cs": "Používat zvuk motorové brzdy (Jake Brake)",
        "en": "Use the engine (Jake) brake sound",
        "de": "Motorbremsen-Sound (Jake Brake) verwenden",
    },
    "jakeBrakeVolumePercentage": {
        "cs": "Maximální hlasitost motorové brzdy",
        "en": "Maximum volume of the engine brake sound",
        "de": "Maximale Lautstärke der Motorbremse",
    },
    "jakeBrakeIdleVolumePercentage": {
        "cs": "Minimální (klidová) hlasitost motorové brzdy",
        "en": "Minimum (idle) volume of the engine brake sound",
        "de": "Minimale (Leerlauf-)Lautstärke der Motorbremse",
    },
    "jakeBrakeMinRpm": {
        "cs": "Minimální otáčky, od kterých motorová brzda může znít",
        "en": "Minimum RPM above which the engine brake can sound",
        "de": "Mindestdrehzahl, ab der die Motorbremse hörbar sein kann",
    },
    "dieselKnockVolumePercentage": {
        "cs": "Hlasitost dieselového 'klepání' (typický zvuk vznětového motoru)",
        "en": "Volume of the diesel 'knock' sound (typical diesel engine sound)",
        "de": "Lautstärke des Diesel-'Klopfens' (typischer Dieselmotor-Sound)",
    },
    "dieselKnockIdleVolumePercentage": {
        "cs": "Hlasitost dieselového klepání při volnoběhu",
        "en": "Diesel knock volume while idling",
        "de": "Diesel-Klopfen-Lautstärke im Leerlauf",
    },
    "dieselKnockInterval": {
        "cs": "Interval klepání (menší číslo = častější klepání)",
        "en": "Knock interval (smaller number = more frequent knocking)",
        "de": "Klopfintervall (kleinere Zahl = häufigeres Klopfen)",
    },
    "dieselKnockStartPoint": {
        "cs": "Práh otáček, nad kterým začíná hlasitost klepání narůstat",
        "en": "RPM threshold above which knock volume starts to rise",
        "de": "Drehzahlschwelle, ab der die Klopflautstärke ansteigt",
    },
    "V8": {
        "cs": "Motor typu V8 (sudé pulzy klepání budou hlasitější, typické pro V8)",
        "en": "V8-type engine (even knock pulses will be louder, typical for V8)",
        "de": "V8-Motor (gerade Klopfimpulse werden lauter, typisch für V8)",
    },
    "V2": {
        "cs": "Motor typu V2 (dvouválec, např. Harley) - jiné rozložení klepání",
        "en": "V2-type engine (two-cylinder, e.g. Harley) - different knock pattern",
        "de": "V2-Motor (Zweizylinder, z.B. Harley) - anderes Klopfmuster",
    },
    "dieselKnockAdaptiveVolumePercentage": {
        "cs": "Hlasitost ostatních (ne-prvních) klepnutí v rámci jednoho cyklu motoru",
        "en": "Volume of the other (non-first) knocks within one engine cycle",
        "de": "Lautstärke der übrigen (nicht ersten) Klopfimpulse pro Motorzyklus",
    },
    "turboVolumePercentage": {
        "cs": "Hlasitost zvuku turba (0 = turbo zvuk vypnutý)",
        "en": "Volume of the turbo sound (0 = turbo sound disabled)",
        "de": "Lautstärke des Turbo-Sounds (0 = Turbo-Sound deaktiviert)",
    },
    "turboIdleVolumePercentage": {
        "cs": "Hlasitost turba při volnoběhu (roste s otáčkami)",
        "en": "Turbo volume while idling (increases with RPM)",
        "de": "Turbo-Lautstärke im Leerlauf (steigt mit der Drehzahl)",
    },
    "chargerVolumePercentage": {
        "cs": "Hlasitost zvuku kompresoru (0 = vypnuto)",
        "en": "Volume of the supercharger sound (0 = disabled)",
        "de": "Lautstärke des Kompressor-Sounds (0 = deaktiviert)",
    },
    "chargerIdleVolumePercentage": {
        "cs": "Hlasitost kompresoru při volnoběhu",
        "en": "Supercharger volume while idling",
        "de": "Kompressor-Lautstärke im Leerlauf",
    },
    "chargerStartPoint": {
        "cs": "Práh otáček, od kterého hlasitost kompresoru narůstá",
        "en": "RPM threshold above which supercharger volume rises",
        "de": "Drehzahlschwelle, ab der die Kompressorlautstärke steigt",
    },
    "wastegateVolumePercentage": {
        "cs": "Hlasitost zvuku odpouštěcího ventilu turba (0 = vypnuto)",
        "en": "Volume of the turbo wastegate/blowoff sound (0 = disabled)",
        "de": "Lautstärke des Turbo-Wastegate-Sounds (0 = deaktiviert)",
    },
    "wastegateIdleVolumePercentage": {
        "cs": "Hlasitost odpouštěcího ventilu po prudkém uvolnění plynu",
        "en": "Wastegate volume after a rapid throttle release",
        "de": "Wastegate-Lautstärke nach plötzlichem Gaswegnehmen",
    },
    "fanVolumePercentage": {
        "cs": "Hlasitost zvuku chladicího ventilátoru (0 = vypnuto)",
        "en": "Volume of the cooling fan sound (0 = disabled)",
        "de": "Lautstärke des Kühlgebläse-Sounds (0 = deaktiviert)",
    },
    "fanIdleVolumePercentage": {
        "cs": "Hlasitost ventilátoru při volnoběhu",
        "en": "Fan volume while idling",
        "de": "Lüfterlautstärke im Leerlauf",
    },
    "fanStartPoint": {
        "cs": "Práh otáček, od kterého hlasitost ventilátoru narůstá",
        "en": "RPM threshold above which fan volume rises",
        "de": "Drehzahlschwelle, ab der die Lüfterlautstärke steigt",
    },
    "GEARBOX_WHINING": {
        "cs": "Simulovat kvílení převodovky v neutrálu pomocí zvuku ventilátoru",
        "en": "Simulate gearbox whining in neutral using the fan sound",
        "de": "Getriebeheulen im Leerlauf mit dem Lüftersound simulieren",
    },
    "hornVolumePercentage": {
        "cs": "Hlasitost klaksonu",
        "en": "Horn volume",
        "de": "Hupenlautstärke",
    },
    "sirenVolumePercentage": {
        "cs": "Hlasitost sirény / doplňkového houkání",
        "en": "Volume of the siren / additional horn",
        "de": "Lautstärke der Sirene / zusätzlichen Hupe",
    },
    "brakeVolumePercentage": {
        "cs": "Hlasitost uvolnění vzduchové brzdy",
        "en": "Volume of the air brake release sound",
        "de": "Lautstärke des Druckluftbremsen-Sounds",
    },
    "parkingBrakeVolumePercentage": {
        "cs": "Hlasitost zapnutí parkovací brzdy",
        "en": "Volume of the parking brake engaging sound",
        "de": "Lautstärke des Feststellbremsen-Sounds",
    },
    "shiftingVolumePercentage": {
        "cs": "Hlasitost řazení převodů",
        "en": "Volume of the gear shifting sound",
        "de": "Lautstärke des Schaltgeräuschs",
    },
    "sound1VolumePercentage": {
        "cs": "Hlasitost doplňkového zvuku 1 (např. zvuk zbraně, zvonek, melodie)",
        "en": "Volume of additional sound 1 (e.g. weapon sound, bell, melody)",
        "de": "Lautstärke des zusätzlichen Sounds 1 (z.B. Waffensound, Glocke, Melodie)",
    },
    "reversingVolumePercentage": {
        "cs": "Hlasitost pípání při couvání",
        "en": "Volume of the reversing beep sound",
        "de": "Lautstärke des Rückwärtsfahr-Piepsers",
    },
    "indicatorVolumePercentage": {
        "cs": "Hlasitost blinkru (0 = vypnuto)",
        "en": "Indicator/turn signal volume (0 = disabled)",
        "de": "Blinkerlautstärke (0 = deaktiviert)",
    },
    "indicatorOn": {
        "cs": "Práh natočení řízení, nad kterým se blinkr automaticky zapne",
        "en": "Steering threshold above which the indicator switches on automatically",
        "de": "Lenkschwelle, ab der der Blinker automatisch aktiviert wird",
    },
    "INDICATOR_DIR": {
        "cs": "Směr vyhodnocení blinkru (true/false - pokud blinká na špatnou stranu, přepni)",
        "en": "Indicator direction logic (true/false - flip if it blinks the wrong side)",
        "de": "Blinkerrichtungslogik (true/false - umschalten, falls die falsche Seite blinkt)",
    },
    "XENON_LIGHTS": {
        "cs": "Simulovat záblesk xenonové výbojky při rozsvícení světel",
        "en": "Simulate a xenon bulb ignition flash when lights turn on",
        "de": "Xenon-Zündblitz beim Einschalten des Lichts simulieren",
    },
    "doubleFlashBlueLight": {
        "cs": "Modrý maják: true = dvojité bliknutí, false = rotující maják",
        "en": "Blue light: true = double flash, false = rotating beacon",
        "de": "Blaulicht: true = Doppelblitz, false = Rundumleuchte",
    },
    "escRampTimeFirstGear": {
        "cs": "Rychlost náběhu zrychlení/zpomalení v 1. rychlostním stupni (menší = pomalejší)",
        "en": "Acceleration/deceleration ramp speed in 1st gear (lower = slower)",
        "de": "Beschleunigungs-/Verzögerungsrampe im 1. Gang (niedriger = langsamer)",
    },
    "escRampTimeSecondGear": {
        "cs": "Rychlost náběhu zrychlení/zpomalení ve 2. stupni (u automatu se používá vždy)",
        "en": "Acceleration/deceleration ramp speed in 2nd gear (always used with automatic transmission)",
        "de": "Beschleunigungs-/Verzögerungsrampe im 2. Gang (bei Automatik immer verwendet)",
    },
    "escRampTimeThirdGear": {
        "cs": "Rychlost náběhu zrychlení/zpomalení ve 3. stupni",
        "en": "Acceleration/deceleration ramp speed in 3rd gear",
        "de": "Beschleunigungs-/Verzögerungsrampe im 3. Gang",
    },
    "escBrakeSteps": {
        "cs": "Jak rychle dokáže ESC brzdit (větší = rychlejší brzdění)",
        "en": "How fast the ESC can brake down (higher = faster braking)",
        "de": "Wie schnell das ESC bremsen kann (höher = schnelleres Bremsen)",
    },
    "escAccelerationSteps": {
        "cs": "Jak rychle dokáže ESC zrychlovat (větší = rychlejší zrychlení)",
        "en": "How fast the ESC can accelerate (higher = faster acceleration)",
        "de": "Wie schnell das ESC beschleunigen kann (höher = schnellere Beschleunigung)",
    },
    "automatic": {
        "cs": "true = simulace automatické převodovky s měničem, false = lineární křivka otáček",
        "en": "true = simulated automatic transmission with torque converter, false = linear RPM curve",
        "de": "true = simulierte Automatikgetriebe mit Wandler, false = lineare Drehzahlkurve",
    },
    "NumberOfAutomaticGears": {
        "cs": "Počet rychlostí simulované automatické převodovky (3, 4 nebo 6)",
        "en": "Number of gears for the simulated automatic transmission (3, 4 or 6)",
        "de": "Anzahl der Gänge des simulierten Automatikgetriebes (3, 4 oder 6)",
    },
    "doubleClutch": {
        "cs": "Simulace dvouspojkové převodovky (nepoužívat zároveň s 'automatic')",
        "en": "Simulate a double-clutch transmission (do not combine with 'automatic')",
        "de": "Doppelkupplungsgetriebe simulieren (nicht gleichzeitig mit 'automatic' verwenden)",
    },
    "shiftingAutoThrottle": {
        "cs": "Automatická úprava plynu při řazení (pro Tamiya 3-stupňovou převodovku)",
        "en": "Automatic throttle adjustment while shifting (for Tamiya 3-speed transmission)",
        "de": "Automatische Gasanpassung beim Schalten (für Tamiya 3-Gang-Getriebe)",
    },
    "clutchEngagingPoint": {
        "cs": "Práh otáček, nad kterým se 'zabírá' spojka (zvuk motoru se sesynchronizuje s výkonem)",
        "en": "RPM threshold above which the 'clutch' engages (engine sound syncs with power)",
        "de": "Drehzahlschwelle, ab der die 'Kupplung' greift (Motorsound synchronisiert mit Leistung)",
    },
    "MAX_RPM_PERCENTAGE": {
        "cs": "Maximální otáčky motoru v % otáček volnoběhu (cca 200 % pro velké diesely, 400 % pro rychloběžné motory)",
        "en": "Max engine RPM as % of idle RPM (about 200% for big diesels, 400% for fast-revving engines)",
        "de": "Maximale Motordrehzahl in % der Leerlaufdrehzahl (ca. 200% für große Diesel, 400% für hochdrehende Motoren)",
    },
    "SUPER_SLOW": {
        "cs": "Velmi pomalá reakce otáček - pro těžké motory (např. lokomotivy)",
        "en": "Very slow RPM response - for heavy engines (e.g. locomotives)",
        "de": "Sehr träge Drehzahlreaktion - für schwere Motoren (z.B. Lokomotiven)",
    },
    "acc": {
        "cs": "Krok zrychlení otáček motoru (1 = pomalé/lokomotiva, 9 = rychlé/trophy truck)",
        "en": "Engine RPM acceleration step (1 = slow/locomotive, 9 = fast/trophy truck)",
        "de": "Beschleunigungsschritt der Motordrehzahl (1 = langsam/Lokomotive, 9 = schnell/Trophy-Truck)",
    },
    "dec": {
        "cs": "Krok zpomalení otáček motoru (1 = pomalé/lokomotiva, 5 = rychlé/trophy truck)",
        "en": "Engine RPM deceleration step (1 = slow/locomotive, 5 = fast/trophy truck)",
        "de": "Verzögerungsschritt der Motordrehzahl (1 = langsam/Lokomotive, 5 = schnell/Trophy-Truck)",
    },
    "TRACKED_MODE": {
        "cs": "Režim pásového vozidla (tank, rypadlo) - dvě nezávislé páky plynu na kanálech 2 a 3",
        "en": "Tracked vehicle mode (tank, digger) - two independent throttle inputs on channels 2 and 3",
        "de": "Kettenfahrzeug-Modus (Panzer, Bagger) - zwei unabhängige Gaseingänge auf Kanal 2 und 3",
    },

    # --- Doplněno ve fázi 2 (parametry z ostatních 81 vozidel) ---

    "COUPLING_SOUND": {
        "cs": "Používat zvuk připojení/odpojení přívěsu",
        "en": "Use the trailer coupling & uncoupling sounds",
        "de": "Sound für An-/Abkuppeln des Anhängers verwenden",
    },
    "couplingVolumePercentage": {
        "cs": "Hlasitost zvuku připojení/odpojení přívěsu",
        "en": "Volume of the trailer coupling/uncoupling sound",
        "de": "Lautstärke des An-/Abkuppel-Sounds",
    },
    "RPM_DEPENDENT_KNOCK": {
        "cs": "Hlasitost dieselového klepání závislá i na otáčkách motoru (ne jen na plynu)",
        "en": "Knock volume also depends on engine RPM (not just throttle)",
        "de": "Klopflautstärke hängt zusätzlich von der Motordrehzahl ab (nicht nur vom Gas)",
    },
    "minKnockVolumePercentage": {
        "cs": "Minimální hlasitost klepání při startovních otáčkách klepání (cca 5-80 %)",
        "en": "Minimum knock volume at the knock start RPM (about 5-80%)",
        "de": "Minimale Klopflautstärke bei der Klopf-Startdrehzahl (ca. 5-80%)",
    },
    "knockStartRpm": {
        "cs": "Otáčky, od kterých začíná klepání (cca 50-400)",
        "en": "RPM at which the knock effect starts (about 50-400)",
        "de": "Drehzahl, ab der der Klopfeffekt beginnt (ca. 50-400)",
    },
    "R6": {
        "cs": "Motor typu R6 (řadový šestiválec) - 6. klepnutí bude hlasitější",
        "en": "R6-type engine (inline six-cylinder) - the 6th knock pulse will be louder",
        "de": "R6-Motor (Reihensechszylinder) - der 6. Klopfimpuls wird lauter",
    },
    "R6_2": {
        "cs": "Motor typu R6 (varianta) - 6. i 3. klepnutí bude hlasitější",
        "en": "R6-type engine (variant) - both the 6th and 3rd knock pulses will be louder",
        "de": "R6-Motor (Variante) - der 6. und der 3. Klopfimpuls werden lauter",
    },
    "SEPARATE_FULL_BEAM": {
        "cs": "Dálková světla jsou samostatná žárovka připojená na pin střešních světel (v tom případě připoj střešní světla na piny bočních světel)",
        "en": "High beam is a separate bulb connected to the roof lights pin (in that case, connect roof lights to the side lights pins)",
        "de": "Fernlicht ist eine separate Lampe am Dachlicht-Pin (in diesem Fall Dachlicht an die Seitenlicht-Pins anschließen)",
    },
    "trackRattleVolumePercentage": {
        "cs": "Hlasitost chrastění pásů",
        "en": "Volume of the track rattle sound",
        "de": "Lautstärke des Kettenrasselns",
    },
    "hydraulicPumpVolumePercentage": {
        "cs": "Hlasitost hydraulického čerpadla",
        "en": "Volume of the hydraulic pump sound",
        "de": "Lautstärke der Hydraulikpumpe",
    },
    "hydraulicFlowVolumePercentage": {
        "cs": "Hlasitost proudění hydraulické kapaliny",
        "en": "Volume of the hydraulic fluid flow sound",
        "de": "Lautstärke des Hydraulikflüssigkeitsstroms",
    },
    "bucketRattleVolumePercentage": {
        "cs": "Hlasitost chrastění lopaty (rypadlo)",
        "en": "Volume of the excavator bucket rattle sound",
        "de": "Lautstärke des Schaufelrasselns (Bagger)",
    },
    "V8_468": {
        "cs": "Motor typu V8 468 (konkrétní varianta klepání pro tento motor)",
        "en": "V8 468 engine (specific knock variant for this engine)",
        "de": "V8-468-Motor (spezifische Klopfvariante für diesen Motor)",
    },
    "LED_INDICATORS": {
        "cs": "LED blinkry se rozsvítí/zhasnou okamžitě (bez postupného náběhu/dohasínání jako u klasických žárovek)",
        "en": "LED-based indicators switch on and off immediately (no gradual fade like bulbs)",
        "de": "LED-Blinker schalten sofort ein/aus (kein allmähliches Auf-/Abblenden wie bei Glühlampen)",
    },
    "EXCAVATOR_MODE": {
        "cs": "Zvukový modul běží v režimu rypadla",
        "en": "The sound controller is running in excavator mode",
        "de": "Das Soundmodul läuft im Bagger-Modus",
    },
    "INDICATOR_SIDE_MARKERS": {
        "cs": "Blinkry se používají zároveň i jako boční obrysová světla",
        "en": "The indicators are also used as side marker lights",
        "de": "Die Blinker werden auch als seitliche Positionsleuchten verwendet",
    },
    "LOADER_MODE": {
        "cs": "Zvukový modul běží v režimu kolového nakladače",
        "en": "The sound controller is running in loader mode",
        "de": "Das Soundmodul läuft im Lader-Modus",
    },
    "DUMP_BED": {
        "cs": "Vozidlo má hydraulickou sklápěcí korbu (např. CAT 730)",
        "en": "Vehicle with a hydraulic dump bed (e.g. CAT 730)",
        "de": "Fahrzeug mit hydraulischer Kippmulde (z.B. CAT 730)",
    },
    "TRACK_RATTLE_2": {
        "cs": "Používat i druhý zvuk chrastění pásů (přehraje se s malým zpožděním po prvním, pro realističtější efekt)",
        "en": "Use a second track rattle sound (played with a slight delay after the first, for a more realistic effect)",
        "de": "Zweiten Kettenrasseln-Sound verwenden (mit leichter Verzögerung nach dem ersten, für einen realistischeren Effekt)",
    },
    "trackRattle2VolumePercentage": {
        "cs": "Hlasitost druhého zvuku chrastění pásů",
        "en": "Volume of the second track rattle sound",
        "de": "Lautstärke des zweiten Kettenrasseln-Sounds",
    },
    "pwmStrokeChainDriveTopSpeed": {
        "cs": "Rozsah PWM signálu pro maximální rychlost pásového pohonu (u ESC Hobbywing 1060 typicky 1500 ± 300)",
        "en": "PWM signal range for max. track drive speed (for a Hobbywing 1060 ESC, typically 1500 ± 300)",
        "de": "PWM-Signalbereich für maximale Kettenantriebsgeschwindigkeit (bei Hobbywing 1060 ESC typischerweise 1500 ± 300)",
    },
    "pwmStrokeChainDriveStartRotation": {
        "cs": "Práh PWM signálu, od kterého se pásový pohon začne pohybovat (nad hodnotou 1500 + tohle číslo)",
        "en": "PWM signal threshold at which the track drive starts moving (above 1500 + this value)",
        "de": "PWM-Signalschwelle, ab der sich der Kettenantrieb zu bewegen beginnt (über 1500 + diesem Wert)",
    },
    "trackRattleIntervalMin": {
        "cs": "Minimální interval mezi zvuky chrastění pásů při nejvyšší rychlosti (nesmí být kratší než délka nahrávky)",
        "en": "Minimum interval between track rattle sounds at top speed (must not be shorter than the sample length)",
        "de": "Minimales Intervall zwischen Kettenrasseln-Sounds bei Höchstgeschwindigkeit (darf nicht kürzer als die Sample-Länge sein)",
    },
    "trackRattleIntervalMax": {
        "cs": "Maximální interval mezi zvuky chrastění pásů při nízké rychlosti",
        "en": "Maximum interval between track rattle sounds at low speed",
        "de": "Maximales Intervall zwischen Kettenrasseln-Sounds bei niedriger Geschwindigkeit",
    },
    "JAKEBRAKE_ENGINE_SLOWDOWN": {
        "cs": "Používat motorovou brzdu ke zpomalení motoru při uvolnění plynu v neutrálu nebo při podřazování s přidaným plynem",
        "en": "Use the engine (Jake) brake to slow the engine when releasing throttle in neutral or during upshifting with throttle applied",
        "de": "Motorbremse verwenden, um den Motor beim Gaswegnehmen im Leerlauf oder beim Hochschalten mit Gas zu verlangsamen",
    },
    "TIRE_SQUEAL": {
        "cs": "Používat zvuk kvílení pneumatik",
        "en": "Use the tire squealing sound",
        "de": "Reifenquietsch-Sound verwenden",
    },
    "tireSquealVolumePercentage": {
        "cs": "Hlasitost kvílení pneumatik",
        "en": "Volume of the tire squealing sound",
        "de": "Lautstärke des Reifenquietschens",
    },
    "HYDROSTATIC_TRACK_MOTORS": {
        "cs": "Vozidlo má hydrostatické pásové motory (zvuk hydrauliky a pokles otáček budou záviset na rychlosti)",
        "en": "Vehicle has hydrostatic track motors (hydraulic pump sound and RPM drop will be speed-dependent)",
        "de": "Fahrzeug hat hydrostatische Kettenmotoren (Hydrauliksound und Drehzahlabfall sind geschwindigkeitsabhängig)",
    },
    "CRANE_MODE": {
        "cs": "Zvukový modul běží v režimu jeřábu",
        "en": "The sound controller is running in crane mode",
        "de": "Das Soundmodul läuft im Kran-Modus",
    },
    "engineManualOnOff": {
        "cs": "Zapnout funkci ručního zapnutí/vypnutí motoru (pro použití s přijímačem 'Micro RC' od TheDIYGuy999 - v tom případě odpadá automatická kalibrace nulového pulzu)",
        "en": "Enable manual engine on/off functionality (for use with the 'Micro RC' receiver from TheDIYGuy999 - disables automatic pulse-zero calibration in this case)",
        "de": "Manuelle Motor-Ein/Aus-Funktion aktivieren (für den 'Micro RC'-Empfänger von TheDIYGuy999 - in diesem Fall entfällt die automatische Nullpuls-Kalibrierung)",
    },
    "pwmSoundTrigger": {
        "cs": "Klakson/zvuk je spouštěný přímo RC PWM signálem místo trvalé vysoké úrovně signálu",
        "en": "Sound is triggered directly by the RC PWM signal instead of a constant high signal level",
        "de": "Sound wird direkt durch das RC-PWM-Signal ausgelöst, statt durch ein dauerhaftes High-Signal",
    },
    "V8_MEDIUM": {
        "cs": "Motor V8 se 'středně hlasitými' klepnutími (experimentální, autor uvádí, že výsledky nejsou dobré)",
        "en": "V8 with 'medium loud' knocks (experimental - the author notes the results aren't good)",
        "de": "V8 mit 'mittellauten' Klopfgeräuschen (experimentell - laut Autor keine guten Ergebnisse)",
    },
    "STEAM_LOCOMOTIVE_MODE": {
        "cs": "Zvukový modul běží v režimu parní lokomotivy",
        "en": "The sound controller is running in steam locomotive mode",
        "de": "Das Soundmodul läuft im Dampflokomotiv-Modus",
    },
    "AIRPLANE_MODE": {
        "cs": "Režim pro letadla (rozsah plynu vždy 1000-2000, volnoběh na 1000, bez simulace spojky)",
        "en": "Mode for airplanes (throttle range always 1000-2000, idle at 1000, no clutch simulation)",
        "de": "Modus für Flugzeuge (Gasbereich immer 1000-2000, Leerlauf bei 1000, keine Kupplungssimulation)",
    },

    # --- Doplněno pro rozšířené karty (ESC, převodovka, světla, zvuk,
    #     dashboard, přívěs, dálkové ovládání, servo výstupy, shaker) ---

    "WEMOS_D1_MINI_ESP32": {"cs": "Software běží na desce Wemos D1 Mini ESP32 (jiné rozmístění světelných pinů)", "en": "Software runs on a Wemos D1 Mini ESP32 board (different light pin layout)", "de": "Software läuft auf einem Wemos D1 Mini ESP32 Board (andere Licht-Pin-Belegung)"},
    "DEBUG": {"cs": "Obecné ladicí zprávy do sériové linky - zpomaluje běh, jen pro vývojáře", "en": "General debug messages over serial - slows things down, developer only", "de": "Allgemeine Debug-Meldungen über die serielle Schnittstelle - verlangsamt den Betrieb, nur für Entwickler"},
    "CHANNEL_DEBUG": {"cs": "Ladicí výpis hodnot přijímaných kanálů", "en": "Debug output of received channel values", "de": "Debug-Ausgabe der empfangenen Kanalwerte"},
    "ESC_DEBUG": {"cs": "Ladicí výpis chování ESC regulátoru", "en": "Debug output of ESC behavior", "de": "Debug-Ausgabe des ESC-Verhaltens"},
    "AUTO_TRANS_DEBUG": {"cs": "Ladicí výpis automatické převodovky", "en": "Debug output of automatic transmission", "de": "Debug-Ausgabe des Automatikgetriebes"},
    "MANUAL_TRANS_DEBUG": {"cs": "Ladicí výpis manuální/poloautomatické převodovky", "en": "Debug output of manual/semi-automatic transmission", "de": "Debug-Ausgabe des manuellen/Halbautomatikgetriebes"},
    "TRACKED_DEBUG": {"cs": "Ladicí výpis pásového (tank) režimu", "en": "Debug output of tracked (tank) mode", "de": "Debug-Ausgabe des Kettenmodus (Panzer)"},
    "SERVO_DEBUG": {"cs": "Ladicí výpis serv", "en": "Debug output of servos", "de": "Debug-Ausgabe der Servos"},
    "ESPNOW_DEBUG": {"cs": "Ladicí výpis bezdrátové komunikace ESP-NOW (přívěs)", "en": "Debug output of ESP-NOW wireless communication (trailer)", "de": "Debug-Ausgabe der ESP-NOW-Funkkommunikation (Anhänger)"},
    "CORE_DEBUG": {"cs": "Hloubkový ladicí výpis jádra systému - NIKDY nepoužívat, jen pro vývoj samotného firmwaru", "en": "Deep core system debug - NEVER use, only for firmware development itself", "de": "Tiefgehendes Kern-Debug - NIEMALS verwenden, nur für die Firmware-Entwicklung selbst"},
    "eeprom_id": {"cs": "Interní identifikátor uložené konfigurace - změna vynutí obnovení výchozích hodnot", "en": "Internal ID of the stored configuration - changing it forces a reset to defaults", "de": "Interne ID der gespeicherten Konfiguration - Änderung erzwingt Rücksetzung auf Standardwerte"},
    "ERASE_EEPROM_ON_BOOT": {"cs": "Smaže veškerou uloženou konfiguraci při každém startu - NIKDY nezapínat, vozidlo nebude fungovat", "en": "Erases all stored configuration on every boot - NEVER enable, vehicle will not work", "de": "Löscht bei jedem Start die gesamte gespeicherte Konfiguration - NIEMALS aktivieren, Fahrzeug funktioniert sonst nicht"},
    "ENABLE_WIRELESS": {"cs": "Povolí WiFi konfigurační web a/nebo bezdrátovou komunikaci s přívěsem", "en": "Enables the WiFi configuration website and/or wireless trailer communication", "de": "Aktiviert die WLAN-Konfigurationswebsite und/oder die drahtlose Anhängerkommunikation"},
    "USE_CSS": {"cs": "Použije stylovaný vzhled na starší konfigurační webové stránce", "en": "Uses styled appearance on the legacy configuration website", "de": "Verwendet ein gestyltes Aussehen auf der alten Konfigurationswebsite"},
    "MODERN_CSS": {"cs": "Modernější varianta vzhledu starší konfigurační webové stránky", "en": "More modern variant of the legacy configuration website's look", "de": "Modernere Variante des Erscheinungsbilds der alten Konfigurationswebsite"},
    "default_ssid": {"cs": "Výchozí název WiFi sítě, kterou modul vytvoří pro připojení mobilem/počítačem", "en": "Default name of the WiFi network the module creates for connecting via phone/computer", "de": "Standardname des WLAN-Netzwerks, das das Modul für die Verbindung per Handy/PC erstellt"},
    "default_password": {"cs": "Výchozí heslo k té WiFi síti", "en": "Default password for that WiFi network", "de": "Standardpasswort für dieses WLAN-Netzwerk"},

    "QUICRUN_FUSION": {"cs": "Kompenzace linearity pro ESC Hobbywing Quicrun Fusion - nutné odkomentovat, pokud tento regulátor používáš", "en": "Linearity compensation for the Hobbywing Quicrun Fusion ESC - must be uncommented if you use this ESC", "de": "Linearitätskompensation für den Hobbywing Quicrun Fusion ESC - muss aktiviert werden, wenn du diesen Regler verwendest"},
    "QUICRUN_16BL30": {"cs": "Kompenzace linearity pro ESC Hobbywing Quicrun 16BL30 (experimentální, nedoporučeno)", "en": "Linearity compensation for the Hobbywing Quicrun 16BL30 ESC (experimental, not recommended)", "de": "Linearitätskompensation für den Hobbywing Quicrun 16BL30 ESC (experimentell, nicht empfohlen)"},
    "ESC_DIR": {"cs": "Otočí směr otáčení ESC, pokud motor jede opačně, než má", "en": "Reverses ESC direction if the motor spins the wrong way", "de": "Kehrt die ESC-Richtung um, falls der Motor falsch herum dreht"},
    "HYDROSTATIC_MODE": {"cs": "Zapni, pokud má vozidlo hydrostatický pohon (plynulá regulace bez řazení)", "en": "Enable if the vehicle has a hydrostatic drive (smooth control without gear shifts)", "de": "Aktivieren, wenn das Fahrzeug einen Hydrostatikantrieb hat (stufenlose Regelung ohne Schalten)"},
    "directionChangeLimit": {"cs": "Omezení výkonu při rychlé změně směru (typicky kolem 80)", "en": "Power limit during a rapid direction change (typically around 80)", "de": "Leistungsbegrenzung bei schnellem Richtungswechsel (typischerweise um 80)"},
    "RZ7886_DRIVER_MODE": {"cs": "Použít budič motoru RZ7886 místo standardního ESC", "en": "Use the RZ7886 motor driver instead of a standard ESC", "de": "RZ7886-Motortreiber statt Standard-ESC verwenden"},
    "RZ7886_FREQUENCY": {"cs": "PWM frekvence budiče RZ7886 (doporučeno 500 Hz)", "en": "PWM frequency of the RZ7886 driver (500 Hz recommended)", "de": "PWM-Frequenz des RZ7886-Treibers (500 Hz empfohlen)"},
    "RZ7886_DRAGBRAKE_DUTY": {"cs": "Síla brzdného účinku budiče RZ7886 (doporučeno 100 %)", "en": "Drag brake strength of the RZ7886 driver (100% recommended)", "de": "Bremsleistung des RZ7886-Treibers (100% empfohlen)"},
    "brakeMargin": {"cs": "Experimentální rezerva při brzdění - POZOR, nikdy nedávat víc než 20, vozidlo by se nemuselo umět zastavit", "en": "Experimental braking margin - WARNING, never set above 20, vehicle may fail to stop", "de": "Experimentelle Bremsreserve - WARNUNG, nie über 20 einstellen, Fahrzeug könnte nicht mehr bremsen können"},
    "escPulseSpan": {"cs": "Rozsah signálu pro ESC (500 = plný výkon, 1000 = poloviční výkon)", "en": "ESC signal range (500 = full power available, 1000 = half power available)", "de": "ESC-Signalbereich (500 = volle Leistung, 1000 = halbe Leistung verfügbar)"},
    "escTakeoffPunch": {"cs": "Krátký impuls navíc při rozjezdu, aby se model nezasekl", "en": "Extra short power punch at takeoff so the model doesn't get stuck", "de": "Kurzer zusätzlicher Leistungsimpuls beim Anfahren, damit das Modell nicht stecken bleibt"},
    "escReversePlus": {"cs": "Přídavný výkon při couvání (couvání bývá slabší)", "en": "Extra power while reversing (reverse is usually weaker)", "de": "Zusätzliche Leistung beim Rückwärtsfahren (Rückwärtsgang ist meist schwächer)"},
    "crawlerEscRampTime": {"cs": "Rychlost náběhu ESC v crawler režimu", "en": "ESC ramp-up speed in crawler mode", "de": "ESC-Rampengeschwindigkeit im Crawler-Modus"},
    "globalAccelerationPercentage": {"cs": "Experimentální celkové omezení zrychlení - může narušit řazení automatické převodovky", "en": "Experimental overall acceleration limit - may interfere with automatic gearbox shifting", "de": "Experimentelle globale Beschleunigungsbegrenzung - kann das Schalten des Automatikgetriebes stören"},
    "BATTERY_PROTECTION": {"cs": "Zapne ochranu baterie proti hlubokému vybití", "en": "Enables battery protection against deep discharge", "de": "Aktiviert Akkuschutz gegen Tiefentladung"},
    "CUTOFF_VOLTAGE": {"cs": "Napětí, při kterém se vozidlo pro ochranu baterie vypne - NIKDY neméně než 3.2V na článek", "en": "Voltage at which the vehicle shuts down to protect the battery - NEVER below 3.2V per cell", "de": "Spannung, bei der sich das Fahrzeug zum Akkuschutz abschaltet - NIEMALS unter 3.2V pro Zelle"},
    "FULLY_CHARGED_VOLTAGE": {"cs": "Napětí odpovídající plně nabité baterii", "en": "Voltage corresponding to a fully charged battery", "de": "Spannung eines voll geladenen Akkus"},
    "RECOVERY_HYSTERESIS": {"cs": "O kolik voltů musí napětí stoupnout zpět, než se vozidlo znovu 'odemkne'", "en": "How many volts the voltage must recover before the vehicle 'unlocks' again", "de": "Um wie viele Volt die Spannung sich erholen muss, bevor sich das Fahrzeug wieder 'entsperrt'"},
    "RESISTOR_TO_BATTTERY_PLUS": {"cs": "Hodnota odporu k plusovému pólu baterie pro měření napětí - POZOR, špatná hodnota může trvale poškodit řízení", "en": "Resistor value to battery plus for voltage sensing - WARNING, a wrong value can permanently damage the controller", "de": "Widerstandswert zum Akku-Plus für die Spannungsmessung - WARNUNG, ein falscher Wert kann die Steuerung dauerhaft beschädigen"},
    "RESISTOR_TO_GND": {"cs": "Hodnota odporu k zemi (GND) pro měření napětí - POZOR, špatná hodnota může trvale poškodit řízení", "en": "Resistor value to ground for voltage sensing - WARNING, a wrong value can permanently damage the controller", "de": "Widerstandswert zur Masse für die Spannungsmessung - WARNUNG, ein falscher Wert kann die Steuerung dauerhaft beschädigen"},
    "DIODE_DROP": {"cs": "Úbytek napětí na diodě v obvodu měření baterie (typicky kolem 0.3V)", "en": "Voltage drop across the diode in the battery sensing circuit (typically around 0.3V)", "de": "Spannungsabfall an der Diode im Akku-Messkreis (typischerweise um 0.3V)"},
    "outOfFuelVolumePercentage": {"cs": "Hlasitost hlášky 'došlo palivo', vybíráš i jazyk hlášky níže", "en": "Volume of the 'out of fuel' message, you also choose the message language below", "de": "Lautstärke der 'Kraftstoff leer'-Meldung, die Sprache wählst du unten"},

    "VIRTUAL_3_SPEED": {"cs": "Simuluje 3rychlostní automatickou převodovku", "en": "Simulates a 3-speed automatic transmission", "de": "Simuliert ein 3-Gang-Automatikgetriebe"},
    "VIRTUAL_16_SPEED_SEQUENTIAL": {"cs": "Stále experimentální, nefunguje pořádně - nepoužívat", "en": "Still experimental, not working properly - don't use", "de": "Noch experimentell, funktioniert nicht richtig - nicht verwenden"},
    "OVERDRIVE": {"cs": "Přidá rychloběžný převodový stupeň (nekombinovat s dvouspojkovou převodovkou)", "en": "Adds an overdrive gear (don't combine with double-clutch transmission)", "de": "Fügt einen Overdrive-Gang hinzu (nicht mit Doppelkupplungsgetriebe kombinieren)"},
    "automaticReverseAccelerationPercentage": {"cs": "Zrychlení při couvání s automatickou převodovkou", "en": "Acceleration while reversing with automatic transmission", "de": "Beschleunigung beim Rückwärtsfahren mit Automatikgetriebe"},
    "lowRangePercentage": {"cs": "Redukční převod pro terénní/nízký rozsah (příklad pro WPL: konkrétní poměr uveden v komentáři)", "en": "Reduction ratio for the low/off-road range (example for WPL gearboxes given in the comment)", "de": "Untersetzungsverhältnis für den Geländegang (Beispiel für WPL-Getriebe im Kommentar)"},
    "SEMI_AUTOMATIC": {"cs": "Simuluje poloautomatickou převodovku - řadí se tlačítkem, ale bez spojkového pedálu", "en": "Simulates a semi-automatic transmission - shift by button, no clutch pedal", "de": "Simuliert ein Halbautomatikgetriebe - Schalten per Knopf, ohne Kupplungspedal"},
    "MODE1_SHIFTING": {"cs": "Řazení ovládané přepínačem MODE1 (typicky u vozidel WPL)", "en": "Shifting controlled by the MODE1 switch (typically on WPL vehicles)", "de": "Schalten über den MODE1-Schalter gesteuert (typisch bei WPL-Fahrzeugen)"},
    "TRANSMISSION_NEUTRAL": {"cs": "Umožní zařadit neutrál", "en": "Allows shifting into neutral", "de": "Ermöglicht das Einlegen des Leerlaufs"},
    "maxClutchSlippingRpm": {"cs": "Maximální otáčky prokluzu spojky - liší se podle typu vozidla", "en": "Maximum clutch slipping RPM - varies by vehicle type", "de": "Maximale Kupplungsschlupfdrehzahl - variiert je nach Fahrzeugtyp"},
    "DOUBLE_CLUTCH": {"cs": "Simuluje dvouspojkovou převodovku (přibližně 90 pro manuál, 10 pro automat)", "en": "Simulates a double-clutch transmission (about 90 for manual, 10 for automatic)", "de": "Simuliert ein Doppelkupplungsgetriebe (ca. 90 für manuell, 10 für automatisch)"},
    "HIGH_SLIPPINGPOINT": {"cs": "Vyšší bod prokluzu spojky - u těžkých vozidel raději vypnout", "en": "Higher clutch slipping point - better disabled for heavy vehicles", "de": "Höherer Kupplungsschlupfpunkt - bei schweren Fahrzeugen besser deaktivieren"},

    "NEOPIXEL_ENABLED": {"cs": "Zapne podporu adresovatelného LED pásku (Neopixel/WS2812)", "en": "Enables support for an addressable LED strip (Neopixel/WS2812)", "de": "Aktiviert Unterstützung für einen adressierbaren LED-Streifen (Neopixel/WS2812)"},
    "NEOPIXEL_ON_CH4": {"cs": "Neopixel je připojený na kanál 4 místo výchozího pinu", "en": "Neopixel is connected on channel 4 instead of the default pin", "de": "Neopixel ist an Kanal 4 statt am Standard-Pin angeschlossen"},
    "NEOPIXEL_COUNT": {"cs": "Kolik LED je na pásku zapojeno - musí sedět s reálným počtem", "en": "How many LEDs are on the strip - must match the real count", "de": "Wie viele LEDs am Streifen angeschlossen sind - muss der realen Anzahl entsprechen"},
    "NEOPIXEL_BRIGHTNESS": {"cs": "Jas LED pásku podle vlastního vkusu", "en": "LED strip brightness, to your taste", "de": "Helligkeit des LED-Streifens nach Geschmack"},
    "MAX_POWER_MILLIAMPS": {"cs": "Maximální proudový odběr LED pásku v mA - závisí na tvém 5V zdroji (doporučeno 100)", "en": "Maximum LED strip current draw in mA - depends on your 5V supply (100 recommended)", "de": "Maximale Stromaufnahme des LED-Streifens in mA - abhängig von deiner 5V-Versorgung (100 empfohlen)"},
    "NEOPIXEL_HIGHBEAM": {"cs": "Použít Neopixel i jako dálková světla", "en": "Also use Neopixel as high beam", "de": "Neopixel auch als Fernlicht verwenden"},
    "neopixelMode": {"cs": "Styl animace LED pásku podle vlastního vkusu", "en": "LED strip animation style, to your taste", "de": "Animationsstil des LED-Streifens nach Geschmack"},
    "THIRD_BRAKELIGHT": {"cs": "Zapni, pokud má vozidlo třetí (horní) brzdové světlo", "en": "Enable if the vehicle has a third (top) brake light", "de": "Aktivieren, wenn das Fahrzeug ein drittes (oberes) Bremslicht hat"},
    "ROTATINGBEACON_ON_B1": {"cs": "Rotující maják je zapojený na výstupu B1", "en": "Rotating beacon is wired to output B1", "de": "Rundumleuchte ist an Ausgang B1 angeschlossen"},
    "INDICATOR_TOGGLING_MODE": {"cs": "Přepínací (ne stisknout-a-držet) způsob ovládání blinkrů - typicky u nakladačů", "en": "Toggle-style (not press-and-hold) indicator control - typically on loaders", "de": "Umschalt- statt Halte-Steuerung der Blinker - typisch bei Ladern"},
    "noCabLights": {"cs": "Vozidlo nemá světla v kabině", "en": "Vehicle has no cab lights", "de": "Fahrzeug hat keine Kabinenbeleuchtung"},
    "noFogLights": {"cs": "Vozidlo nemá mlhová světla", "en": "Vehicle has no fog lights", "de": "Fahrzeug hat keine Nebelscheinwerfer"},
    "xenonLights": {"cs": "Simuluje záblesk při rozsvícení, jako mají xenonové výbojky", "en": "Simulates the ignition flash of xenon bulbs when lights turn on", "de": "Simuliert den Zündblitz von Xenonlampen beim Einschalten"},
    "flickeringWileCranking": {"cs": "Světla poblikávají při startování motoru (efekt slabé baterie)", "en": "Lights flicker while cranking the engine (weak battery effect)", "de": "Licht flackert beim Anlassen des Motors (Effekt schwacher Batterie)"},
    "ledIndicators": {"cs": "Blinkry se rozsvítí/zhasnou okamžitě, bez postupného náběhu jako u žárovek", "en": "Indicators switch on/off instantly, without the gradual fade of bulbs", "de": "Blinker schalten sofort ein/aus, ohne das allmähliche Auf-/Abblenden von Glühlampen"},
    "swap_L_R_indicators": {"cs": "Prohodí levý a pravý blinkr, pokud blikají obráceně", "en": "Swaps left and right indicators if they blink the wrong way round", "de": "Vertauscht linken und rechten Blinker, falls sie falsch herum blinken"},
    "indicatorsAsSidemarkers": {"cs": "Blinkry slouží zároveň jako boční obrysová světla ('americký' styl)", "en": "Indicators also serve as side marker lights ('US style')", "de": "Blinker dienen zusätzlich als seitliche Positionsleuchten ('US-Stil')"},
    "separateFullBeam": {"cs": "Dálková světla jsou samostatná žárovka na pinu střešních světel - v tom případě přepoj střešní světla na piny bočních světel", "en": "High beam is a separate bulb on the roof lights pin - in that case wire roof lights to the side lights pins instead", "de": "Fernlicht ist eine separate Lampe am Dachlicht-Pin - in diesem Fall Dachlicht stattdessen an die Seitenlicht-Pins anschließen"},
    "flashingBlueLight": {"cs": "Modrý maják bliká místo rotace", "en": "Blue light flashes instead of rotating", "de": "Blaulicht blinkt statt zu rotieren"},
    "hazardsWhile5thWheelUnlocked": {"cs": "Výstražná světla se automaticky zapnou při odjištění točnice (5th wheel)", "en": "Hazard lights turn on automatically when the 5th wheel is unlocked", "de": "Warnblinker schaltet sich automatisch ein, wenn die Sattelkupplung entriegelt ist"},
    "cabLightsBrightness": {"cs": "Jas světel v kabině podle vlastního vkusu", "en": "Cab lights brightness, to your taste", "de": "Helligkeit der Kabinenbeleuchtung nach Geschmack"},
    "sideLightsBrightness": {"cs": "Jas obrysových světel podle vlastního vkusu", "en": "Side lights brightness, to your taste", "de": "Helligkeit des Seitenlichts nach Geschmack"},
    "rearlightDimmedBrightness": {"cs": "Jas zadních světel v tlumeném (obrysovém) režimu", "en": "Rear lights brightness in dimmed (parking) mode", "de": "Helligkeit des Rücklichts im gedimmten (Standlicht-)Modus"},
    "rearlightParkingBrightness": {"cs": "Jas zadních světel v parkovacím režimu", "en": "Rear lights brightness in parking mode", "de": "Helligkeit des Rücklichts im Parklicht-Modus"},
    "headlightParkingBrightness": {"cs": "Jas předních světel v parkovacím režimu", "en": "Headlight brightness in parking mode", "de": "Helligkeit des Frontlichts im Parklicht-Modus"},
    "reversingLightBrightness": {"cs": "Jas couvacích světel podle vlastního vkusu", "en": "Reversing light brightness, to your taste", "de": "Helligkeit des Rückfahrlichts nach Geschmack"},
    "fogLightBrightness": {"cs": "Jas mlhových světel podle vlastního vkusu", "en": "Fog light brightness, to your taste", "de": "Helligkeit der Nebelscheinwerfer nach Geschmack"},

    "NO_SIREN": {"cs": "Vypne sirénu úplně", "en": "Disables the siren entirely", "de": "Deaktiviert die Sirene vollständig"},
    "NO_INDICATOR_SOUND": {"cs": "Vypne cvakací zvuk blinkru", "en": "Disables the indicator clicking sound", "de": "Deaktiviert das Blinker-Klickgeräusch"},
    "numberOfVolumeSteps": {"cs": "Kolik úrovní celkové hlasitosti je k dispozici (vázáno na seznam hodnot níže)", "en": "How many overall volume steps are available (tied to the value list below)", "de": "Wie viele Gesamtlautstärke-Stufen verfügbar sind (an die Werteliste unten gekoppelt)"},
    "masterVolumeCrawlerThreshold": {"cs": "Práh přepnutí na tišší 'crawler' hlasitost", "en": "Threshold for switching to quieter 'crawler' volume", "de": "Schwelle für den Wechsel zur leiseren 'Crawler'-Lautstärke"},
    "masterVolumePercentage": {"cs": "Seznam dostupných úrovní celkové hlasitosti (přepínáš je tlačítkem za jízdy)", "en": "List of available overall volume levels (switch between them with a button while driving)", "de": "Liste der verfügbaren Gesamtlautstärke-Stufen (per Taste während der Fahrt umschaltbar)"},

    "SPI_DASHBOARD": {"cs": "Zapni, pokud používáš SPI palubní desku s displejem", "en": "Enable if you use an SPI dashboard display", "de": "Aktivieren, wenn du ein SPI-Armaturenbrett-Display verwendest"},
    "FREVIC_DASHBOARD": {"cs": "Zapni, pokud používáš palubní desku Frevic", "en": "Enable if you use a Frevic dashboard", "de": "Aktivieren, wenn du ein Frevic-Armaturenbrett verwendest"},
    "dashRotation": {"cs": "Natočení displeje palubní desky podle skutečné montáže", "en": "Dashboard display rotation to match the physical mounting", "de": "Ausrichtung des Armaturenbrett-Displays passend zur tatsächlichen Montage"},
    "MAX_REAL_SPEED": {"cs": "Maximální reálná rychlost, kterou budík zobrazuje", "en": "Maximum real speed the gauge displays", "de": "Maximale reale Geschwindigkeit, die der Tacho anzeigt"},
    "RPM_MAX": {"cs": "Maximální otáčky na budíku - pevná hodnota, obvykle 500, neměnit", "en": "Maximum RPM on the gauge - fixed value, usually 500, don't change", "de": "Maximale Drehzahl am Zähler - fester Wert, üblicherweise 500, nicht ändern"},
    "manualGearRatios": {"cs": "Převodové poměry jednotlivých rychlostí - musí sedět s reálnou převodovkou", "en": "Gear ratios for each speed - must match the real gearbox", "de": "Übersetzungsverhältnisse der einzelnen Gänge - müssen zum realen Getriebe passen"},

    "TRAILER_LIGHTS_TRAILER_PRESENCE_SWITCH_DEPENDENT": {"cs": "Světla přívěsu se řídí podle toho, jestli je přívěs fyzicky připojený (přepínač přítomnosti)", "en": "Trailer lights depend on whether the trailer is physically connected (presence switch)", "de": "Anhängerlicht richtet sich danach, ob der Anhänger physisch angeschlossen ist (Anwesenheitsschalter)"},
    "defaultUseTrailer1": {"cs": "Používat přívěs 1 ve výchozím nastavení", "en": "Use trailer 1 by default", "de": "Anhänger 1 standardmäßig verwenden"},
    "defaultUseTrailer2": {"cs": "Používat přívěs 2 ve výchozím nastavení", "en": "Use trailer 2 by default", "de": "Anhänger 2 standardmäßig verwenden"},
    "defaultUseTrailer3": {"cs": "Používat přívěs 3 ve výchozím nastavení", "en": "Use trailer 3 by default", "de": "Anhänger 3 standardmäßig verwenden"},
    "defaultBroadcastAddress1": {"cs": "MAC adresa modulu na přívěsu 1 pro bezdrátové párování (ESP-NOW)", "en": "MAC address of the module on trailer 1 for wireless pairing (ESP-NOW)", "de": "MAC-Adresse des Moduls an Anhänger 1 für die drahtlose Kopplung (ESP-NOW)"},
    "defaultBroadcastAddress2": {"cs": "MAC adresa modulu na přívěsu 2 pro bezdrátové párování (ESP-NOW)", "en": "MAC address of the module on trailer 2 for wireless pairing (ESP-NOW)", "de": "MAC-Adresse des Moduls an Anhänger 2 für die drahtlose Kopplung (ESP-NOW)"},
    "defaultBroadcastAddress3": {"cs": "MAC adresa modulu na přívěsu 3 pro bezdrátové párování (ESP-NOW)", "en": "MAC address of the module on trailer 3 for wireless pairing (ESP-NOW)", "de": "MAC-Adresse des Moduls an Anhänger 3 für die drahtlose Kopplung (ESP-NOW)"},

    "PROTOTYPE_36": {"cs": "Přepínač pro 36pinovou variantu desky - NIKDY neodkomentovávat, způsobí problémy se spuštěním", "en": "Switch for the 36-pin board variant - NEVER uncomment, causes boot issues", "de": "Schalter für die 36-Pin-Board-Variante - NIEMALS aktivieren, verursacht Startprobleme"},
    "sbusBaud": {"cs": "Rychlost SBUS komunikace - standard je 100000, zkus snížit při nestabilním signálu (funkční rozsah cca 96000-104000)", "en": "SBUS communication speed - standard is 100000, try lowering if signal is unstable (working range about 96000-104000)", "de": "SBUS-Kommunikationsgeschwindigkeit - Standard ist 100000, bei instabilem Signal verringern (Arbeitsbereich ca. 96000-104000)"},
    "EMBEDDED_SBUS": {"cs": "Použije vestavěný SBUS kód místo externí knihovny (doporučeno, neměnit)", "en": "Uses embedded SBUS code instead of an external library (recommended, don't change)", "de": "Verwendet eingebetteten SBUS-Code statt einer externen Bibliothek (empfohlen, nicht ändern)"},
    "sbusFailsafeTimeout": {"cs": "Po kolika milisekundách bez signálu se spustí nouzový režim (obvykle kolem 100)", "en": "After how many milliseconds without signal failsafe triggers (usually around 100)", "de": "Nach wie vielen Millisekunden ohne Signal der Failsafe-Modus ausgelöst wird (üblicherweise um 100)"},
    "channelAutoZero": {"cs": "Automaticky dorovnat neutrál kanálu při startu - NEpoužívat u kanálů bez pružinou vystředěné neutrální polohy (přepínače, nevyužité kanály)", "en": "Automatically zero the channel's neutral at startup - do NOT use for channels without a spring-centered neutral (switches, unused channels)", "de": "Neutralstellung des Kanals beim Start automatisch nullen - NICHT verwenden bei Kanälen ohne federzentrierte Neutralstellung (Schalter, ungenutzte Kanäle)"},
    "channelReversed": {"cs": "Invertovat směr tohoto kanálu (pokud reaguje obráceně)", "en": "Reverse this channel's direction (if it responds the wrong way)", "de": "Richtung dieses Kanals umkehren (falls er falsch herum reagiert)"},
    "EXPONENTIAL_THROTTLE": {"cs": "Plynulejší náběh plynu kolem středu páky (exponenciální křivka)", "en": "Smoother throttle response near stick center (exponential curve)", "de": "Sanftere Gasreaktion um die Knüppelmitte (exponentielle Kurve)"},
    "EXPONENTIAL_STEERING": {"cs": "Plynulejší náběh řízení kolem středu páky (exponenciální křivka)", "en": "Smoother steering response near stick center (exponential curve)", "de": "Sanftere Lenkreaktion um die Knüppelmitte (exponentielle Kurve)"},
    "CHANNEL_AVERAGING": {"cs": "Vyhlazuje hodnoty kanálů průměrováním - potlačí cukání, ale přidá malé zpoždění", "en": "Smooths channel values by averaging - reduces jitter but adds slight delay", "de": "Glättet Kanalwerte durch Mittelwertbildung - reduziert Ruckeln, fügt aber leichte Verzögerung hinzu"},
    "sbusInverted": {"cs": "Jestli je potřeba invertovat SBUS signál - nastavuje se v jednotlivých profilech vysílačky", "en": "Whether the SBUS signal needs inverting - set within each remote profile", "de": "Ob das SBUS-Signal invertiert werden muss - wird in den einzelnen Senderprofilen eingestellt"},
    "pulseNeutral": {"cs": "Šířka neutrálního pásma kolem středu signálu (obvykle kolem 30)", "en": "Width of the neutral deadband around the signal center (usually around 30)", "de": "Breite der neutralen Totzone um die Signalmitte (üblicherweise um 30)"},
    "pulseSpan": {"cs": "Rozsah signálu od středu na obě strany (teoreticky 500, obvykle kolem 480)", "en": "Signal range from center in each direction (theoretically 500, usually about 480)", "de": "Signalbereich von der Mitte in beide Richtungen (theoretisch 500, üblicherweise etwa 480)"},
    "AUTO_ENGINE_ON_OFF": {"cs": "Motor se zapíná/vypíná automaticky pákou plynu a časovačem, nebo ručně kanálem 5", "en": "Engine switches on/off automatically via throttle stick and timer, or manually via channel 5", "de": "Motor schaltet sich automatisch über Gasknüppel und Timer ein/aus, oder manuell über Kanal 5"},
    "AUTO_INDICATORS": {"cs": "Blinkry se spouští automaticky podle úhlu řízení, nebo ručně kanálem 6", "en": "Indicators trigger automatically based on steering angle, or manually via channel 6", "de": "Blinker werden automatisch je nach Lenkwinkel ausgelöst, oder manuell über Kanal 6"},
    "AUTO_LIGHTS": {"cs": "Světla se řídí podle stavu motoru, nebo ručně kanálem 5", "en": "Lights are controlled by engine state, or manually via channel 5", "de": "Licht wird durch den Motorzustand gesteuert, oder manuell über Kanal 5"},

    "STEERING": {"cs": "Který kanál vysílačky ovládá řízení", "en": "Which transmitter channel controls steering", "de": "Welcher Senderkanal die Lenkung steuert"},
    "GEARBOX": {"cs": "Který kanál ovládá 3polohový přepínač převodovky (v pásovém režimu levá páka)", "en": "Which channel controls the 3-position gearbox switch (left stick in tracked mode)", "de": "Welcher Kanal den 3-Stufen-Getriebeschalter steuert (im Kettenmodus linker Knüppel)"},
    "THROTTLE": {"cs": "Který kanál ovládá plyn a brzdu (v pásovém režimu pravá páka)", "en": "Which channel controls throttle & brake (right stick in tracked mode)", "de": "Welcher Kanal Gas & Bremse steuert (im Kettenmodus rechter Knüppel)"},
    "HORN": {"cs": "Který kanál ovládá klakson a modrý maják/sirénu", "en": "Which channel controls the horn and blue light/siren", "de": "Welcher Kanal Hupe und Blaulicht/Sirene steuert"},
    "POT2": {"cs": "Který kanál je přiřazený druhému potenciometru", "en": "Which channel is assigned to the second potentiometer", "de": "Welcher Kanal dem zweiten Potentiometer zugeordnet ist"},
    "MODE1": {"cs": "Který kanál je přepínač Mode 1", "en": "Which channel is the Mode 1 switch", "de": "Welcher Kanal der Mode-1-Schalter ist"},
    "MODE2": {"cs": "Který kanál je přepínač Mode 2", "en": "Which channel is the Mode 2 switch", "de": "Welcher Kanal der Mode-2-Schalter ist"},
    "MOMENTARY1": {"cs": "Který kanál je tlačítko bez aretace (momentary) 1", "en": "Which channel is momentary button 1", "de": "Welcher Kanal der Taster (momentary) 1 ist"},
    "HAZARDS": {"cs": "Který kanál ovládá výstražná světla", "en": "Which channel controls hazard lights", "de": "Welcher Kanal die Warnblinkanlage steuert"},
    "INDICATOR_LEFT": {"cs": "Který kanál ovládá levý blinkr", "en": "Which channel controls the left indicator", "de": "Welcher Kanal den linken Blinker steuert"},
    "INDICATOR_RIGHT": {"cs": "Který kanál ovládá pravý blinkr", "en": "Which channel controls the right indicator", "de": "Welcher Kanal den rechten Blinker steuert"},
    "CH_14": {"cs": "Přiřazení kanálu 14", "en": "Channel 14 assignment", "de": "Zuordnung Kanal 14"},
    "CH_15": {"cs": "Přiřazení kanálu 15", "en": "Channel 15 assignment", "de": "Zuordnung Kanal 15"},
    "CH_16": {"cs": "Přiřazení kanálu 16", "en": "Channel 16 assignment", "de": "Zuordnung Kanal 16"},
    "FUNCTION_L": {"cs": "Kanál pro přístup k doplňkovým funkcím na levé ose (dočasně omezí rozsah osy na 75 %)", "en": "Channel for accessing secondary functions on the left axis (temporarily limits its range to 75%)", "de": "Kanal für den Zugriff auf Zusatzfunktionen auf der linken Achse (begrenzt deren Bereich vorübergehend auf 75%)"},
    "FUNCTION_R": {"cs": "Kanál pro přístup k doplňkovým funkcím na pravé ose (dočasně omezí rozsah osy na 75 %)", "en": "Channel for accessing secondary functions on the right axis (temporarily limits its range to 75%)", "de": "Kanal für den Zugriff auf Zusatzfunktionen auf der rechten Achse (begrenzt deren Bereich vorübergehend auf 75%)"},

    "CH1L": {"cs": "Koncová poloha serva kanálu 1 vlevo (typicky řízení)", "en": "Channel 1 servo end position, left (typically steering)", "de": "Servo-Endposition Kanal 1 links (typischerweise Lenkung)"},
    "CH1C": {"cs": "Střední (neutrální) poloha serva kanálu 1", "en": "Channel 1 servo center (neutral) position", "de": "Servo-Mittelstellung (neutral) Kanal 1"},
    "CH1R": {"cs": "Koncová poloha serva kanálu 1 vpravo", "en": "Channel 1 servo end position, right", "de": "Servo-Endposition Kanal 1 rechts"},
    "CH1_RAMP_TIME": {"cs": "Jak rychle se servo kanálu 1 pohybuje mezi polohami", "en": "How fast the channel 1 servo moves between positions", "de": "Wie schnell sich das Servo von Kanal 1 zwischen den Positionen bewegt"},
    "CH2L": {"cs": "Koncová poloha serva kanálu 2 vlevo", "en": "Channel 2 servo end position, left", "de": "Servo-Endposition Kanal 2 links"},
    "CH2C": {"cs": "Střední (neutrální) poloha serva kanálu 2", "en": "Channel 2 servo center (neutral) position", "de": "Servo-Mittelstellung (neutral) Kanal 2"},
    "CH2R": {"cs": "Koncová poloha serva kanálu 2 vpravo", "en": "Channel 2 servo end position, right", "de": "Servo-Endposition Kanal 2 rechts"},
    "CH2_RAMP_TIME": {"cs": "Jak rychle se servo kanálu 2 pohybuje mezi polohami", "en": "How fast the channel 2 servo moves between positions", "de": "Wie schnell sich das Servo von Kanal 2 zwischen den Positionen bewegt"},
    "CH3L": {"cs": "Koncová poloha serva kanálu 3 vlevo", "en": "Channel 3 servo end position, left", "de": "Servo-Endposition Kanal 3 links"},
    "CH3C": {"cs": "Střední (neutrální) poloha serva kanálu 3", "en": "Channel 3 servo center (neutral) position", "de": "Servo-Mittelstellung (neutral) Kanal 3"},
    "CH3R": {"cs": "Koncová poloha serva kanálu 3 vpravo", "en": "Channel 3 servo end position, right", "de": "Servo-Endposition Kanal 3 rechts"},
    "CH3_RAMP_TIME": {"cs": "Jak rychle se servo kanálu 3 pohybuje mezi polohami", "en": "How fast the channel 3 servo moves between positions", "de": "Wie schnell sich das Servo von Kanal 3 zwischen den Positionen bewegt"},
    "CH3_BEACON": {"cs": "Na kanálu 3 je zapojený maják místo serva", "en": "A beacon is wired to channel 3 instead of a servo", "de": "An Kanal 3 ist ein Blinklicht statt eines Servos angeschlossen"},
    "CH4L": {"cs": "Koncová poloha serva kanálu 4 vlevo", "en": "Channel 4 servo end position, left", "de": "Servo-Endposition Kanal 4 links"},
    "CH4C": {"cs": "Střední (neutrální) poloha serva kanálu 4", "en": "Channel 4 servo center (neutral) position", "de": "Servo-Mittelstellung (neutral) Kanal 4"},
    "CH4R": {"cs": "Koncová poloha serva kanálu 4 vpravo", "en": "Channel 4 servo end position, right", "de": "Servo-Endposition Kanal 4 rechts"},
    "CH4_RAMP_TIME": {"cs": "Jak rychle se servo kanálu 4 pohybuje mezi polohami", "en": "How fast the channel 4 servo moves between positions", "de": "Wie schnell sich das Servo von Kanal 4 zwischen den Positionen bewegt"},
    "ESC_L": {"cs": "Koncová hodnota ESC signálu vlevo (couvání)", "en": "ESC signal end value, left (reverse)", "de": "ESC-Signal-Endwert links (Rückwärts)"},
    "ESC_C": {"cs": "Střední (neutrální) hodnota ESC signálu", "en": "ESC signal center (neutral) value", "de": "ESC-Signal-Mittelwert (neutral)"},
    "ESC_R": {"cs": "Koncová hodnota ESC signálu vpravo (vpřed)", "en": "ESC signal end value, right (forward)", "de": "ESC-Signal-Endwert rechts (vorwärts)"},
    "ESC_MIN": {"cs": "Minimální hodnota ESC signálu", "en": "Minimum ESC signal value", "de": "Minimaler ESC-Signalwert"},
    "ESC_MAX": {"cs": "Maximální hodnota ESC signálu", "en": "Maximum ESC signal value", "de": "Maximaler ESC-Signalwert"},
    "MODE2_HYDRAULIC": {"cs": "Přepínač Mode 2 ovládá hydraulické funkce", "en": "Mode 2 switch controls hydraulic functions", "de": "Mode-2-Schalter steuert Hydraulikfunktionen"},
    "MODE2_TRAILER_UNLOCKING": {"cs": "Přepínač Mode 2 ovládá odjištění přívěsu", "en": "Mode 2 switch controls trailer unlocking", "de": "Mode-2-Schalter steuert die Anhänger-Entriegelung"},
    "MODE2_WINCH": {"cs": "Přepínač Mode 2 ovládá naviják", "en": "Mode 2 switch controls the winch", "de": "Mode-2-Schalter steuert die Seilwinde"},
    "NO_WINCH_DELAY": {"cs": "Naviják reaguje okamžitě, bez zpoždění", "en": "Winch reacts instantly, without delay", "de": "Seilwinde reagiert sofort, ohne Verzögerung"},
    "PINGON_MODE": {"cs": "Speciální řídicí režim Pingon pro konkrétní hardware", "en": "Special Pingon control mode for specific hardware", "de": "Spezieller Pingon-Steuerungsmodus für bestimmte Hardware"},
    "SERVO_FREQUENCY": {"cs": "Frekvence PWM signálu pro serva (obvykle 50 Hz)", "en": "PWM signal frequency for servos (usually 50 Hz)", "de": "PWM-Signalfrequenz für Servos (üblicherweise 50 Hz)"},
    "STEERING_RAMP_TIME": {"cs": "Jak rychle se servo řízení pohybuje mezi polohami", "en": "How fast the steering servo moves between positions", "de": "Wie schnell sich das Lenkservo zwischen den Positionen bewegt"},
    "boomDownwardsHydraulic": {"cs": "Hydraulický pohyb výložníku směrem dolů (rypadlo)", "en": "Hydraulic boom movement downward (excavator)", "de": "Hydraulische Auslegerbewegung nach unten (Bagger)"},
    "reverseBoomSoundDirection": {"cs": "Obrátí, který směr pohybu výložníku odpovídá kterému zvuku", "en": "Reverses which boom movement direction matches which sound", "de": "Kehrt um, welche Auslegerbewegungsrichtung zu welchem Sound passt"},

    "shakerStart": {"cs": "Síla otřesů (vibrací) při startu motoru (max. 255)", "en": "Shaker (vibration) power while starting the engine (max. 255)", "de": "Vibrationsstärke beim Motorstart (max. 255)"},
    "shakerIdle": {"cs": "Síla otřesů při volnoběhu (max. 255)", "en": "Shaker power while idling (max. 255)", "de": "Vibrationsstärke im Leerlauf (max. 255)"},
    "shakerFullThrottle": {"cs": "Síla otřesů při plném plynu (max. 255)", "en": "Shaker power at full throttle (max. 255)", "de": "Vibrationsstärke bei Vollgas (max. 255)"},
    "shakerStop": {"cs": "Síla otřesů při vypnutí motoru (max. 255)", "en": "Shaker power while stopping the engine (max. 255)", "de": "Vibrationsstärke beim Abstellen des Motors (max. 255)"},
}

# original category header text (as it appears in the source file, after
# stripping the leading "// " and trailing dashes) -> translated text
CATEGORY_TRANSLATIONS: dict[str, dict[str, str]] = {
    "Choose the start sound (uncomment the one you want)": {
        "cs": "Zvuk startu motoru",
        "en": "Engine start sound",
        "de": "Motorstart-Sound",
    },
    "Choose the motor idle sound (uncomment the one you want)": {
        "cs": "Zvuk volnoběhu motoru",
        "en": "Engine idle sound",
        "de": "Motorleerlauf-Sound",
    },
    "Choose the motor revving sound (uncomment the one you want)": {
        "cs": "Zvuk vysokých otáček motoru",
        "en": "Engine revving sound",
        "de": "Motordrehzahl-Sound",
    },
    "Choose the jake brake sound (uncomment the one you want)": {
        "cs": "Zvuk motorové brzdy (Jake Brake)",
        "en": "Engine (Jake) brake sound",
        "de": "Motorbremsen-Sound (Jake Brake)",
    },
    "Adjust the additional turbo sound (set \"turboVolumePercentage\" to \"0\", if you don't want it)": {
        "cs": "Zvuk turba",
        "en": "Turbo sound",
        "de": "Turbo-Sound",
    },
    "Adjust the additional supercharger sound (set \"chargerVolumePercentage\" to \"0\", if you don't want it)": {
        "cs": "Zvuk kompresoru",
        "en": "Supercharger sound",
        "de": "Kompressor-Sound",
    },
    "Adjust the additional turbo wastegate  / blowoff valve  sound (set \"wastegateVolumePercentage\" to \"0\", if you don't want it)": {
        "cs": "Zvuk odpouštěcího ventilu turba (wastegate)",
        "en": "Turbo wastegate / blowoff sound",
        "de": "Turbo-Wastegate-/Blowoff-Sound",
    },
    "Adjust the additional cooling fan sound (set \"fanVolumePercentage\" to \"0\", if you don't want it)": {
        "cs": "Zvuk chladicího ventilátoru",
        "en": "Cooling fan sound",
        "de": "Kühlgebläse-Sound",
    },
    "Choose the horn sound (uncomment the one you want)": {
        "cs": "Klakson",
        "en": "Horn sound",
        "de": "Hupensound",
    },
    "Choose the siren / additional horn sound (uncomment the one you want)": {
        "cs": "Siréna / doplňkové houkání",
        "en": "Siren / additional horn",
        "de": "Sirene / zusätzliche Hupe",
    },
    "Choose the air brake release sound (uncomment the one you want)": {
        "cs": "Uvolnění vzduchové brzdy",
        "en": "Air brake release sound",
        "de": "Druckluftbremsen-Sound",
    },
    "Choose the parking brake engaging sound (uncomment the one you want)": {
        "cs": "Zapnutí parkovací brzdy",
        "en": "Parking brake engaging sound",
        "de": "Feststellbremsen-Sound",
    },
    "Choose the gear shifting sound (uncomment the one you want)": {
        "cs": "Řazení převodů",
        "en": "Gear shifting sound",
        "de": "Schaltgeräusch",
    },
    "Choose the additional \"sound1\" (uncomment the one you want)": {
        "cs": "Doplňkový zvuk 1 (zbraň, zvonek, melodie...)",
        "en": "Additional sound 1 (weapon, bell, melody...)",
        "de": "Zusätzlicher Sound 1 (Waffe, Glocke, Melodie...)",
    },
    "Choose the reversing beep sound": {
        "cs": "Pípání při couvání",
        "en": "Reversing beep sound",
        "de": "Rückwärtsfahr-Piepser",
    },
    "Choose the indicator / turn signal options": {
        "cs": "Blinkry / směrová světla",
        "en": "Indicator / turn signal",
        "de": "Blinker",
    },
    "Choose the light options": {
        "cs": "Světla",
        "en": "Lights",
        "de": "Beleuchtung",
    },
    "Choose the blue light options": {
        "cs": "Modrý maják",
        "en": "Blue light",
        "de": "Blaulicht",
    },
    "Acceleration & deceleration settings": {
        "cs": "Zrychlení a zpomalení (ESC)",
        "en": "Acceleration & deceleration settings",
        "de": "Beschleunigungs- und Verzögerungseinstellungen",
    },
    "Gearbox parameters (select number of automatic gears in curves.h)": {
        "cs": "Převodovka",
        "en": "Gearbox parameters",
        "de": "Getriebeparameter",
    },
    "Clutch parameters": {
        "cs": "Spojka",
        "en": "Clutch parameters",
        "de": "Kupplungsparameter",
    },
    "Engine parameters": {
        "cs": "Parametry motoru",
        "en": "Engine parameters",
        "de": "Motorparameter",
    },
    "Vehicle type": {
        "cs": "Typ vozidla",
        "en": "Vehicle type",
        "de": "Fahrzeugtyp",
    },
    "Profil vysílačky": {
        "cs": "Profil vysílačky",
        "en": "Remote profile",
        "de": "Senderprofil",
    },
    "Komunikační protokol": {
        "cs": "Komunikační protokol",
        "en": "Communication protocol",
        "de": "Kommunikationsprotokoll",
    },
    "Ostatní nastavení dálkového ovládání": {
        "cs": "Ostatní nastavení dálkového ovládání",
        "en": "Other remote control settings",
        "de": "Weitere Fernsteuerungseinstellungen",
    },

    # --- Doplněno pro rozšířené karty ---

    "Neopixel settings": {"cs": "Nastavení Neopixel LED pásku", "en": "Neopixel settings", "de": "Neopixel-Einstellungen"},
    "These light settings are adjustabale during compile time only": {"cs": "Nastavení světel (jen před nahráním)", "en": "Light settings (compile-time only)", "de": "Lichteinstellungen (nur vor dem Hochladen)"},
    "These light options are adjustable on the configuration website and stored in the EEPROM": {"cs": "Nastavení světel (uloženo v paměti)", "en": "Light settings (stored in EEPROM)", "de": "Lichteinstellungen (im EEPROM gespeichert)"},
    "IMPORTANT!! Replace the addresses below with your trailers MAC addresses!!": {"cs": "MAC adresy přívěsů", "en": "Trailer MAC addresses", "de": "Anhänger-MAC-Adressen"},

    "Profil serv": {"cs": "Profil serv", "en": "Servo profile", "de": "Servoprofil"},
    "Profil shakeru": {"cs": "Profil shakeru", "en": "Shaker profile", "de": "Shaker-Profil"},

    # 2_Remote.h - profily vysílaček
    "Flysky FS-i6X remote configuration profile": {"cs": "Profil: Flysky FS-i6X", "en": "Profile: Flysky FS-i6X", "de": "Profil: Flysky FS-i6X"},
    "Channels signal range calibration": {"cs": "Kalibrace rozsahu kanálů", "en": "Channels signal range calibration", "de": "Kalibrierung des Kanalsignalbereichs"},
    "Automatic or manual modes": {"cs": "Automatický nebo ruční režim", "en": "Automatic or manual modes", "de": "Automatischer oder manueller Modus"},
    "SBUS mode": {"cs": "Režim SBUS", "en": "SBUS mode", "de": "SBUS-Modus"},
    "Flysky FS-i6S remote configuration profile (CAT 730)": {"cs": "Profil: Flysky FS-i6S (CAT 730)", "en": "Profile: Flysky FS-i6S (CAT 730)", "de": "Profil: Flysky FS-i6S (CAT 730)"},
    "Flysky FS-i6S remote configuration profile (for excavators only)": {"cs": "Profil: Flysky FS-i6S (jen rypadla)", "en": "Profile: Flysky FS-i6S (excavators only)", "de": "Profil: Flysky FS-i6S (nur Bagger)"},
    "Flysky FS-i6S remote configuration profile (for loaders only)": {"cs": "Profil: Flysky FS-i6S (jen nakladače)", "en": "Profile: Flysky FS-i6S (loaders only)", "de": "Profil: Flysky FS-i6S (nur Lader)"},
    "Frsky Tandem XE remote configuration profile (for excavators only)": {"cs": "Profil: Frsky Tandem XE (jen rypadla)", "en": "Profile: Frsky Tandem XE (excavators only)", "de": "Profil: Frsky Tandem XE (nur Bagger)"},
    "Frsky Tandem XE remote configuration profile (for loaders only)": {"cs": "Profil: Frsky Tandem XE (jen nakladače)", "en": "Profile: Frsky Tandem XE (loaders only)", "de": "Profil: Frsky Tandem XE (nur Lader)"},
    "WB remote configuration profile (for excavators only)": {"cs": "Profil: WB (jen rypadla)", "en": "Profile: WB (excavators only)", "de": "Profil: WB (nur Bagger)"},
    "Flysky GT5 / Reely GT6 EVO / Absima CR6P remote configuration profile (thanks to BlackbirdXL1 for making this profile)": {"cs": "Profil: Flysky GT5 / Reely GT6 EVO / Absima CR6P", "en": "Profile: Flysky GT5 / Reely GT6 EVO / Absima CR6P", "de": "Profil: Flysky GT5 / Reely GT6 EVO / Absima CR6P"},
    "RGT MT-305 configuration profile (comes with EX86100)": {"cs": "Profil: RGT MT-305 (s EX86100)", "en": "Profile: RGT MT-305 (comes with EX86100)", "de": "Profil: RGT MT-305 (mit EX86100)"},
    "Graupner mz-12 PRO remote configuration profile": {"cs": "Profil: Graupner mz-12 PRO", "en": "Profile: Graupner mz-12 PRO", "de": "Profil: Graupner mz-12 PRO"},
    "\"Micro RC\" (the car style one) DIY Arduino remote configuration profile": {"cs": "Profil: Micro RC (verze auto)", "en": "Profile: Micro RC (car-style)", "de": "Profil: Micro RC (Auto-Stil)"},
    "\"Micro RC\" (The stick based one) DIY Arduino remote configuration profile": {"cs": "Profil: Micro RC (verze páka)", "en": "Profile: Micro RC (stick-based)", "de": "Profil: Micro RC (Knüppel-basiert)"},

    # 7_Servos.h - profily serv
    "Default servo configuration profile": {"cs": "Výchozí profil serv", "en": "Default servo profile", "de": "Standard-Servoprofil"},
    "MN Model 1:12 Land Rover Defender servo configuration profile": {"cs": "Profil: MN Model Land Rover Defender 1:12", "en": "Profile: MN Model Land Rover Defender 1:12", "de": "Profil: MN Model Land Rover Defender 1:12"},
    "Double Eagle 1:8 Land Rover Defender servo configuration profile": {"cs": "Profil: Double Eagle Land Rover Defender 1:8", "en": "Profile: Double Eagle Land Rover Defender 1:8", "de": "Profil: Double Eagle Land Rover Defender 1:8"},
    "WPL C34 Toyota Land Cruiser configuration profile": {"cs": "Profil: WPL C34 Toyota Land Cruiser", "en": "Profile: WPL C34 Toyota Land Cruiser", "de": "Profil: WPL C34 Toyota Land Cruiser"},
    "WPL Ural servo configuration profile": {"cs": "Profil: WPL Ural", "en": "Profile: WPL Ural", "de": "Profil: WPL Ural"},
    "RGT EX86100 servo configuration profile": {"cs": "Profil: RGT EX86100", "en": "Profile: RGT EX86100", "de": "Profil: RGT EX86100"},
    "Hercules Hobby Actros 3363": {"cs": "Profil: Hercules Hobby Actros 3363", "en": "Profile: Hercules Hobby Actros 3363", "de": "Profil: Hercules Hobby Actros 3363"},
    "TAMIYA King Hauler": {"cs": "Profil: TAMIYA King Hauler", "en": "Profile: TAMIYA King Hauler", "de": "Profil: TAMIYA King Hauler"},
    "Carson Mercedes Racing Truck": {"cs": "Profil: Carson Mercedes Racing Truck", "en": "Profile: Carson Mercedes Racing Truck", "de": "Profil: Carson Mercedes Racing Truck"},
    "Meccano 3 Ton Dumper": {"cs": "Profil: Meccano 3 Ton Dumper", "en": "Profile: Meccano 3 Ton Dumper", "de": "Profil: Meccano 3 Ton Dumper"},
    "Open RC Tractor servo configuration profile": {"cs": "Profil: Open RC Tractor", "en": "Profile: Open RC Tractor", "de": "Profil: Open RC Tractor"},
    "Electric excavator servo configuration profile": {"cs": "Profil: elektrické rypadlo", "en": "Profile: electric excavator", "de": "Profil: Elektrobagger"},
    "Electric excavator servo configuration profile for Hobbywing 1060 ESC": {"cs": "Profil: elektrické rypadlo (ESC Hobbywing 1060)", "en": "Profile: electric excavator (Hobbywing 1060 ESC)", "de": "Profil: Elektrobagger (Hobbywing 1060 ESC)"},
    "Hydraulic excavator servo configuration profile": {"cs": "Profil: hydraulické rypadlo", "en": "Profile: hydraulic excavator", "de": "Profil: Hydraulikbagger"},
    "WB excavator servo configuration profile": {"cs": "Profil: WB rypadlo", "en": "Profile: WB excavator", "de": "Profil: WB-Bagger"},
    "Mushroom3D rough terrain crane": {"cs": "Profil: Mushroom3D terénní jeřáb", "en": "Profile: Mushroom3D rough terrain crane", "de": "Profil: Mushroom3D-Geländekran"},

    # 5_Shaker.h - profily shakeru
    "GT-Power shaker with 3D printed plastic weight": {"cs": "Shaker GT-Power s 3D tištěným závažím", "en": "GT-Power shaker with 3D printed plastic weight", "de": "GT-Power-Shaker mit 3D-gedrucktem Kunststoffgewicht"},

    # 0_generalSettings.h
    "Debug settings": {"cs": "Ladicí nastavení", "en": "Debug settings", "de": "Debug-Einstellungen"},
    "EEPROM settings": {"cs": "Nastavení paměti EEPROM", "en": "EEPROM settings", "de": "EEPROM-Einstellungen"},
    "Hardware settings": {"cs": "Nastavení hardwaru", "en": "Hardware settings", "de": "Hardware-Einstellungen"},
    "Wireless settings": {"cs": "Bezdrátové nastavení", "en": "Wireless settings", "de": "Funkeinstellungen"},
    "WiFi settings (for vehicle configuration website, open 192.168.4.1 in your browser)": {"cs": "Nastavení WiFi (pro webovou konfiguraci, adresa 192.168.4.1)", "en": "WiFi settings (for the configuration website, open 192.168.4.1)", "de": "WLAN-Einstellungen (für die Konfigurationswebsite, 192.168.4.1 öffnen)"},
    "Configuration website settings": {"cs": "Nastavení konfiguračního webu", "en": "Configuration website settings", "de": "Einstellungen der Konfigurationswebsite"},

    # --- Doplněno ve fázi 2 ---

    "play around here, the results are amazing, if you hit the right combination with the idle sound!)": {
        "cs": "Zvuk dieselového klepání",
        "en": "Diesel knock sound",
        "de": "Diesel-Klopfgeräusch",
    },
    "Choose the trailer couplig & uncoupling sounds (uncomment the ones you want)": {
        "cs": "Zvuk připojení/odpojení přívěsu",
        "en": "Trailer coupling & uncoupling sounds",
        "de": "An-/Abkuppel-Sound des Anhängers",
    },
    "Gearbox parameters": {
        "cs": "Převodovka",
        "en": "Gearbox parameters",
        "de": "Getriebeparameter",
    },
    "Choose the track rattle 2 sound (uncomment the one you want)": {
        "cs": "Druhý zvuk chrastění pásů",
        "en": "Second track rattle sound",
        "de": "Zweiter Kettenrasseln-Sound",
    },
    "Choose the track rattle sound (uncomment the one you want)": {
        "cs": "Chrastění pásů",
        "en": "Track rattle sound",
        "de": "Kettenrasseln-Sound",
    },
    "Choose the hydraulic pump sound (uncomment the one you want)": {
        "cs": "Hydraulické čerpadlo",
        "en": "Hydraulic pump sound",
        "de": "Hydraulikpumpen-Sound",
    },
    "Choose the hydraulic fluid flow sound (uncomment the one you want)": {
        "cs": "Proudění hydraulické kapaliny",
        "en": "Hydraulic fluid flow sound",
        "de": "Hydraulikflüssigkeitsstrom-Sound",
    },
    "Choose the bucket rattle sound (uncomment the one you want)": {
        "cs": "Chrastění lopaty (rypadlo)",
        "en": "Excavator bucket rattle sound",
        "de": "Schaufelrasseln-Sound (Bagger)",
    },
    "Choose excavator specific options (use #ifdef FLYSKY_FS_I6S_EXCAVATOR remote profile)": {
        "cs": "Nastavení specifická pro rypadlo (vyžaduje profil vysílače FLYSKY_FS_I6S_EXCAVATOR)",
        "en": "Excavator-specific options (requires the FLYSKY_FS_I6S_EXCAVATOR remote profile)",
        "de": "Baggerspezifische Optionen (erfordert das FLYSKY_FS_I6S_EXCAVATOR-Senderprofil)",
    },
    "Choose the tire squealing sound (uncomment the ones you want)": {
        "cs": "Kvílení pneumatik",
        "en": "Tire squealing sound",
        "de": "Reifenquietsch-Sound",
    },
    "Choose the squeaky track sound (uncomment the one you want)": {
        "cs": "Vrzání pásů",
        "en": "Squeaky track sound",
        "de": "Quietschende-Ketten-Sound",
    },
    "Adjust the additional turbo wastegate valve  sound (set \"wastegateVolumePercentage\" to \"0\", if you don't want it)": {
        "cs": "Zvuk odpouštěcího ventilu turba (wastegate)",
        "en": "Turbo wastegate valve sound",
        "de": "Turbo-Wastegate-Ventil-Sound",
    },
    "Clutch parameters (about 90 for manual transmission, 10 for automatic)": {
        "cs": "Spojka (cca 90 pro manuální převodovku, 10 pro automatickou)",
        "en": "Clutch parameters (about 90 for manual transmission, 10 for automatic)",
        "de": "Kupplungsparameter (ca. 90 für Schaltgetriebe, 10 für Automatik)",
    },
    "Choose the blue light opions": {
        "cs": "Modrý maják",
        "en": "Blue light options",
        "de": "Blaulicht-Optionen",
    },
    "Horn trigger signal type (true / false)": {
        "cs": "Typ spouštěcího signálu klaksonu (true/false)",
        "en": "Horn trigger signal type (true / false)",
        "de": "Auslösesignaltyp der Hupe (true/false)",
    },
    "Choose steam locomotive specific options": {
        "cs": "Nastavení specifická pro parní lokomotivu",
        "en": "Steam locomotive specific options",
        "de": "Dampflokomotivspezifische Optionen",
    },
}


def translate_param_explanation(name: str, fallback_comment: str, lang: str) -> str:
    """Vrátí přeloženou vysvětlivku parametru, nebo originální anglický komentář
    z kódu, pokud pro daný parametr překlad ještě nemáme (jiná vozidla než IS3)."""
    entry = PARAM_TRANSLATIONS.get(name)
    if entry and lang in entry:
        return entry[lang]
    if "[" in name and name.endswith("]"):
        base = name[: name.find("[")]
        base_entry = PARAM_TRANSLATIONS.get(base)
        if base_entry and lang in base_entry:
            return base_entry[lang]
    return fallback_comment or name


def translate_category(original: str, lang: str) -> str:
    entry = CATEGORY_TRANSLATIONS.get(original)
    if entry and lang in entry:
        return entry[lang]
    return original
