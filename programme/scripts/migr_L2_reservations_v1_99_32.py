#!/usr/bin/env python3
"""Migration L2_Reservations -> 16 colonnes (V1.99.32), par chirurgie ZIP.
Idempotent : ne fait rien si les colonnes existent deja. Ne passe JAMAIS par
openpyxl.save (preserve dessins/formules). Usage : python migr_L2_reservations_v1_99_32.py <classeur.xlsx>"""
import sys, re, zipfile, os

NEW = [("K2","Seance liee (ID session A3)"),("L2","Filiere"),("M2","Niveau"),
       ("N2","Matiere"),("O2","Matricule ens."),("P2","Enseignant")]

def attrs(t): return dict(re.findall(r'(\w+(?::\w+)?)="([^"]*)"', t))
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def migrer(path):
    z = zipfile.ZipFile(path)
    wb = z.read("xl/workbook.xml").decode("utf-8")
    n2r = {attrs(s)["name"]: attrs(s).get("r:id") for s in re.findall(r'<sheet\b[^>]*/?>', wb) if "name" in attrs(s)}
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    r2t = {attrs(r)["Id"]: attrs(r)["Target"] for r in re.findall(r'<Relationship\b[^>]*/?>', rels) if "Id" in attrs(r)}
    tgt = r2t[n2r["L2_Reservations"]]
    sheet = tgt.lstrip("/") if tgt.startswith("/") else "xl/"+tgt
    xml = z.read(sheet).decode("utf-8")
    if 'r="K2"' in xml:
        print("Deja a jour (rien a faire) :", os.path.basename(path)); return
    s = (re.search(r'<c r="A2" s="(\d+)"', xml) or [None,"0"])[1]
    cells = "".join(f'<c r="{r}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{esc(t)}</t></is></c>' for r,t in NEW)
    m = re.search(r'(<row r="2"[^>]*>.*?)(</row>)', xml, re.S)
    xml = xml[:m.start()]+m.group(1)+cells+m.group(2)+xml[m.end():]
    xml = re.sub(r'(<dimension ref="A1:)[A-Z]+(2")', r'\1P\2', xml)
    zin = zipfile.ZipFile(path); zout = zipfile.ZipFile(path+".tmp","w",zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        d = zin.read(it.filename)
        if it.filename == sheet: d = xml.encode("utf-8")
        zi = zipfile.ZipInfo(it.filename, date_time=it.date_time)
        zi.compress_type = it.compress_type; zi.external_attr = it.external_attr
        zout.writestr(zi, d)
    zout.close(); zin.close(); os.replace(path+".tmp", path)
    print("Migre (16 colonnes) :", os.path.basename(path))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python migr_L2_reservations_v1_99_32.py <classeur.xlsx>"); sys.exit(1)
    migrer(sys.argv[1])
