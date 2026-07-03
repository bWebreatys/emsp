#!/usr/bin/env python3
"""Migration S1_Stages -> ajout colonne 'Heures d'absence' (R8, V1.99.45),
par chirurgie ZIP. Idempotent : ne fait rien si la colonne existe deja.
Ne passe JAMAIS par openpyxl.save (preserve les 16 dessins du maitre et les
formules). A appliquer sur le maitre ET sur le runtime donnees/data/EMSP_V1.xlsx.
Usage : python migr_S1_heures_absence_v1_99_45.py <classeur.xlsx>
"""
import sys, re, zipfile, os

NEW = [("K2", "Heures d'absence (**)")]


def attrs(t):
    return dict(re.findall(r'(\w+(?::\w+)?)="([^"]*)"', t))


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def migrer(path):
    z = zipfile.ZipFile(path)
    wb = z.read("xl/workbook.xml").decode("utf-8")
    n2r = {attrs(s)["name"]: attrs(s).get("r:id")
           for s in re.findall(r'<sheet\b[^>]*/?>', wb) if "name" in attrs(s)}
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    r2t = {attrs(r)["Id"]: attrs(r)["Target"]
           for r in re.findall(r'<Relationship\b[^>]*/?>', rels) if "Id" in attrs(r)}
    tgt = r2t[n2r["S1_Stages"]]
    sheet = tgt.lstrip("/") if tgt.startswith("/") else "xl/" + tgt
    xml = z.read(sheet).decode("utf-8")
    z.close()
    if 'r="K2"' in xml:
        print("Deja a jour (rien a faire) :", os.path.basename(path)); return
    s = (re.search(r'<c r="A2" s="(\d+)"', xml) or [None, "0"])[1]
    cells = "".join('<c r="%s" s="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                    % (r, s, esc(t)) for r, t in NEW)
    m = re.search(r'(<row r="2"[^>]*>.*?)(</row>)', xml, re.S)
    xml = xml[:m.start()] + m.group(1) + cells + m.group(2) + xml[m.end():]
    # Dimension A1:<col><lignes> -> A1:K<lignes> (on remplace la lettre, on garde la ligne)
    xml = re.sub(r'(<dimension ref="A1:)[A-Z]+(\d+")', r'\1K\2', xml)
    zin = zipfile.ZipFile(path)
    zout = zipfile.ZipFile(path + ".tmp", "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        d = zin.read(it.filename)
        if it.filename == sheet:
            d = xml.encode("utf-8")
        zi = zipfile.ZipInfo(it.filename, date_time=it.date_time)
        zi.compress_type = it.compress_type
        zi.external_attr = it.external_attr
        zout.writestr(zi, d)
    zout.close(); zin.close()
    os.replace(path + ".tmp", path)
    print("Migre (colonne Heures d'absence) :", os.path.basename(path))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python migr_S1_heures_absence_v1_99_45.py <classeur.xlsx>")
        sys.exit(1)
    migrer(sys.argv[1])
