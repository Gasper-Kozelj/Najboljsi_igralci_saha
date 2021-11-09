import os
import re
import csv

mapa = 'podatki'
datoteka_html = 'igralci.html'
datoteka_csv = 'sahisti.csv'

def pretvori_datoteko_v_niz(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, encoding='utf-8') as dat:
        return dat.read()

def razbij_na_igralce(vsebina_strani):
    pattern = re.compile(r'<tr>.*?</tr>',
                         re.DOTALL)
    igralci = re.findall(pattern, vsebina_strani)
    return igralci

def slovar_od_igralca(igralec):
    pattern = re.compile(r'.+?<a href=/profile/\d*?>(?P<ime>.*?)</a>'
                         r'.*?"title">(?P<naslov>.*?)</td>'
                         r'.*?alt=".{3}">(?P<drzava>.{3}).*?</td>'
                         r'.*?"Rtg">(?P<standard_rating>.*?)</td>'
                         r'.*?"Rtg">(?P<rapid_rating>.*?)</td>'
                         r'.*?"Rtg">(?P<blitz_rating>.*?)</td>'
                         r'.*?B-Year">(?P<leto_rojstva>\d*?)</td>',
                         re.DOTALL)
    podatki = re.search(pattern, igralec)
    igralec_dict = podatki.groupdict()
    return igralec_dict

def igralci_iz_datoteke(directory, filename):
    stran = pretvori_datoteko_v_niz(directory, filename)
    igralci = razbij_na_igralce(stran)
    slovar_igralcev = [slovar_od_igralca(igralec) for igralec in igralci]
    return slovar_igralcev

def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def zapisi_igralce_v_csv(igralci, directory, filename):
    write_csv(igralci[0].keys(), igralci, directory, filename)

def main(redownload=True, reparse=True):
    igralci = igralci_iz_datoteke(mapa, datoteka_html)
    zapisi_igralce_v_csv(igralci, mapa, datoteka_csv)

main()