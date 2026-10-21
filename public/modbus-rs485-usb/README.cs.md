# Sunways: přímé připojení RS485–USB do Home Assistantu

[English](README.md)

Tato složka obsahuje sdílenou konfiguraci vestavěné integrace **Modbus** v Home Assistantu. Vychází z domácího zapojení Petra Koska a ze zálohy konfigurace z 21. října 2026.

## Zapojení

`Sunways → RS485 → převodník RS485–USB (FTDI) → Home Assistant`

Home Assistant původně běžel na Raspberry Pi; nyní běží jako virtuální stroj na Proxmoxu, kam je USB převodník předaný. Měnič se čte lokálně přes **Modbus RTU**, bez cloudového účtu.

Toto je samostatná YAML konfigurace Modbus. Nejde o implementaci síťové integrace Sunways Local v nadřazeném repozitáři.

## Soubory

- [sunways-readonly.yaml](sunways-readonly.yaml): doporučený výchozí příklad pouze se čtením senzorů. Neobsahuje přepínače, automatizace ani skripty zapisující do měniče.
Úplná domácí konfigurace s řízením měniče a provozními automatizacemi zde zveřejněna není.

Z původního souboru byla odstraněna místní IP adresa a konkrétní identifikátor USB převodníku byl nahrazen zástupnou cestou. Prázdné řádky byly upraveny; původní uvedení Jana Jirouska z 25. 1. 2024 zůstalo zachováno. Zachována je mapa čtených registrů; řídicí části, šablony a provozní automatizace jsou vynechány.

## Parametry použité v této instalaci

| Parametr | Hodnota |
| --- | --- |
| Přenos | Modbus RTU přes sériový USB port |
| Rychlost | 9600 Bd |
| Datové bity | 8 |
| Parita | žádná (`N`) |
| Stop bity | 1 |
| Adresa měniče (`slave`) | 247 |
| Port v příkladu | `/dev/serial/by-id/usb-YOUR_RS485_ADAPTER-if00-port0` |

Tyto hodnoty popisují konkrétní instalaci, nikoli univerzální nastavení všech Sunways. Ověřte model, firmware, adresu a mapu registrů vlastního měniče.

## Použití varianty pouze pro čtení

1. Zálohujte konfiguraci HA. Ve výpisu hardwaru HA zjistěte skutečnou cestu USB převodníku a nahraďte zástupnou hodnotu `port`. U virtuálního stroje nejprve zajistěte předání USB do HA.
2. Máte-li už nastavené balíčky HA, vložte soubor například jako `/config/packages/sunways-readonly.yaml`. Jinak lze v `configuration.yaml` zapnout balíčky sloučením s existující sekcí:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Nevytvářejte druhou sekci `homeassistant:`. Tento soubor už obsahuje vlastní kořen `modbus:`, proto jej nevkládejte beze změny pod `modbus: !include ...`.

3. Nezavádějte duplicitní hub `sunways`, stejná `unique_id` ani více čteček stejného sériového portu.
4. Zkontrolujte konfiguraci v HA, opravte případné rozdíly schématu své verze HA a teprve potom restartujte.
5. Ověřte živé aktualizace senzorů a porovnejte hodnoty s displejem měniče. Znaménko toku do sítě nebo baterie nelze automaticky přenášet mezi instalacemi.

Jde o zveřejněný příklad ze stávající instalace, nikoli o univerzálně otestovaný instalační balíček. Některé položky původního schématu se mohou mezi verzemi HA lišit.

## Převodník RS485–TCP, například USR-DR134

Tato publikovaná konfigurace používá **USB**, nikoli USR-DR134. Obsahuje užitečnou mapu registrů, ale není hotovou ověřenou konfigurací pro tento síťový převodník.

Pro síťový převodník je potřeba ověřit jeho režim, IP adresu a port i odpovídající transport HA (Modbus TCP oproti RTU přenášenému přes TCP). Pouhá výměna sériového portu za IP adresu nestačí. Kompatibilita USR-DR134 s touto konfigurací ani se síťovou integrací Sunways Local nebyla ověřena.
