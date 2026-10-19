
#!/usr/bin/env python3
import os
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

ONLINE_URL = os.environ.get(
    "ONLINE_EPG_URL",
    "https://www.open-epg.com/generate/TCBD9yXGKt.xml",
)
GITHUB_URL = os.environ.get(
    "SUPPLEMENT_EPG_URL",
    "https://raw.githubusercontent.com/hugofranco10/epg/refs/heads/main/guia_30_dias.xml",
)
OUTPUT = Path(os.environ.get("OUTPUT_FILE", "epg.xml"))
SHIFT_HOURS = int(os.environ.get("SUPPLEMENT_SHIFT_HOURS", "0"))


def download_xml(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "EPG-Merger/1.0"}
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read()

    if not data:
        raise ValueError(f"Descarga vacía: {url}")

    root = ET.fromstring(data)
    if root.tag != "tv":
        raise ValueError(f"El archivo no parece XMLTV: {url}")
    return ET.ElementTree(root)


def shift_time(value, hours):
    value = value.strip()

    # XMLTV con zona horaria: +0000, -0300, etc.
    if len(value) >= 5 and value[-5] in "+-":
        if " " in value:
            stamp, zone = value.rsplit(" ", 1)
            suffix = " " + zone
        else:
            stamp, zone = value[:-5], value[-5:]
            suffix = zone
        dt = datetime.strptime(stamp, "%Y%m%d%H%M%S")
        zone_delta = timedelta(
            hours=int(zone[1:3]),
            minutes=int(zone[3:5])
        )
        if zone[0] == "-":
            zone_delta = -zone_delta
        utc = dt - zone_delta
        shifted = utc + timedelta(hours=hours) + zone_delta
        return shifted.strftime("%Y%m%d%H%M%S") + suffix

    # Sin zona explícita: ajustar la hora indicada.
    dt = datetime.strptime(value, "%Y%m%d%H%M%S")
    return (dt + timedelta(hours=hours)).strftime("%Y%m%d%H%M%S")


def main():
    print("Descargando Open-EPG...")
    main_tree = download_xml(ONLINE_URL)
    root = main_tree.getroot()
    
    root.set("generator-info-name", "MiGeneradorEPG")
    root.attrib.pop("generator-info-url", None)
    
    main_channels = {
        e.get("id")
        for e in root.findall("channel")
        if e.get("id")
    }
    if not main_channels or not root.findall("programme"):
        raise ValueError("Open-EPG no contiene canales o programas.")

    print("Descargando guía complementaria de GitHub...")
    extra_root = download_xml(GITHUB_URL).getroot()

    # Solo canales cuyos IDs no están en Open-EPG.
    new_channels = {}
    for channel in extra_root.findall("channel"):
        channel_id = channel.get("id")
        if channel_id and channel_id not in main_channels:
            new_channels.setdefault(channel_id, channel)

    new_programmes = []
    for programme in extra_root.findall("programme"):
        channel_id = programme.get("channel")

        # Ignorar todos los programas de canales ya existentes.
        if channel_id not in new_channels:
            continue

        copy = ET.fromstring(ET.tostring(programme, encoding="utf-8"))

        for attr in ("start", "stop"):
            value = copy.get(attr)
            if not value:
                raise ValueError(
                    f"Programa sin {attr} en canal {channel_id}"
                )
            copy.set(attr, shift_time(value, SHIFT_HOURS))

        new_programmes.append(copy)

    # Insertar los canales nuevos antes del primer programa.
    first_programme = next(
        (i for i, child in enumerate(root)
         if child.tag == "programme"),
        len(root)
    )

    for channel in new_channels.values():
        root.insert(
            first_programme,
            ET.fromstring(ET.tostring(channel, encoding="utf-8"))
        )
        first_programme += 1

    # Añadir programas exclusivamente de los canales nuevos.
    root.extend(new_programmes)

    if not new_programmes:
        print("Aviso: no se encontraron programas de canales nuevos.")
    
    # Eliminar las descripciones de todos los programas
    for programme in root.findall("programme"):
        for desc in list(programme.findall("desc")):
            programme.remove(desc)
    
    # Eliminar los logos de todos los canales
    for channel in root.findall("channel"):
        for icon in list(channel.findall("icon")):
            channel.remove(icon)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=OUTPUT.parent, delete=False,
            suffix=".tmp"
        ) as tmp:
            temp_path = Path(tmp.name)
            main_tree.write(
                tmp, encoding="utf-8", xml_declaration=True
            )

        # Verificar que el resultado se pueda volver a leer.
        check = ET.parse(temp_path).getroot()
        if check.tag != "tv" or not check.findall("channel"):
            raise ValueError("Falló la validación del XML final.")

        temp_path.replace(OUTPUT)
        temp_path = None
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

    print(f"Canales principales: {len(main_channels)}")
    print(f"Canales nuevos: {len(new_channels)}")
    print(f"Programas añadidos: {len(new_programmes)}")
    print(f"Archivo generado: {OUTPUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
