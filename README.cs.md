# Sunways Local pro Home Assistant

Česky | [English](README.md)

Komunitní integrace pro Home Assistant, která čte data z měniče Sunways přímo přes místní síť a nevyžaduje cloudový účet Sunways.

## Co umí

- připojí se přímo k podporovanému měniči nebo komunikačnímu donglu;
- automaticky rozpozná možnosti zařízení dostupné prostřednictvím použité knihovny;
- dynamicky vytvoří senzory v Home Assistantu;
- podporuje české a anglické překlady;
- umožňuje nastavit interval obnovování od 10 do 3600 sekund;
- z diagnostiky odstraňuje adresu zařízení a sériové číslo.

Integrace je pouze pro čtení. Nemění pracovní režim měniče, exportní limit ani konfigurační hodnoty.

## Požadavky

- kompatibilní měnič Sunways nebo komunikační dongle dostupný z Home Assistantu;
- výchozí port `5488`, který lze změnit;
- knihovna `sunways==0.0.5`, kterou Home Assistant nainstaluje automaticky.

Kompatibilita závisí na modelu měniče, donglu a firmwaru. Úspěšné připojení samo o sobě nepotvrzuje, že znaménko výkonu sítě odpovídá konkrétnímu fyzickému elektroměru.

## Instalace

### Vlastní repozitář HACS

1. V HACS otevřete **Integrace** a přidejte tento repozitář jako vlastní repozitář typu **Integration**.
2. Nainstalujte **Sunways Local**.
3. Restartujte Home Assistant.
4. Otevřete **Nastavení → Zařízení a služby → Přidat integraci** a vyhledejte **Sunways Local**.

### Ruční instalace

Zkopírujte `custom_components/sunways_local` do `/config/custom_components/sunways_local`, restartujte Home Assistant a přidejte integraci z uživatelského rozhraní.

## Bezpečnost a soukromí

Měření zůstává v místní síti a integrace nevyžaduje přihlášení k Sunways Portal. Home Assistant a měnič umístěte do důvěryhodných síťových segmentů a port měniče nevystavujte přímo do internetu.

Projekt není oficiálně spojen se společností Sunways Technologies ani jí podporován.

## Autoři a licence

Integrace používá knihovnu [Chriss-Leo/sunways](https://github.com/Chriss-Leo/sunways) licencovanou pod MIT. Podrobnosti jsou v souboru [NOTICE](NOTICE).

Projekt je vydán pod [licencí Apache 2.0](LICENSE).

## Podpora projektu

Vývoj a údržbu můžete podpořit na [Buy Me a Coffee](https://buymeacoffee.com/kojakcio).



