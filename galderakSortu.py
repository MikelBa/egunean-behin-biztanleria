import math
import random

import pywikibot
from pywikibot import pagegenerators as pg


# Kontsultako emaitzetatik erantzun posible guztiak lortu, ondoren erantzun oker bezala erabili ahal izateko
def getPopulazioa(item):
    populazioa = int(item['claims']['P1082'][-1].getTarget().amount)
    if populazioa < 1000:
        beheko_muga = math.floor(populazioa / 10 ** 2) * 10 ** 2
        goiko_muga = beheko_muga + 10 ** 2
    else:
        n = math.floor(math.log(populazioa,10))
        beheko_muga = math.floor(populazioa / 10 ** (n - 1)) * 10 ** (n - 1)
        goiko_muga = beheko_muga + 10 ** (n - 1)
    erantzuna = f"{beheko_muga:,.0f} - {goiko_muga:,.0f}".replace(",",".")
    return erantzuna,populazioa,beheko_muga,goiko_muga


# Elementuaren euskarazko etiketa edo titulua hartu
def getEuskarazkoIzena(item):
    return item['labels']['eu']


# Elementuaren irudi nabarmendua hartu
def getIrudia(item):
    return item['claims']['P18'][0].getTarget().fileUrl()


# Elementuaren Wikipediako artikulurako esteka hartu
def getArtikuluEsteka(herria):
    site = pywikibot.Site("eu","wikipedia")
    return pywikibot.Page(site,herria).full_url()


def getOkerrak(zuzena,beheko_muga,goiko_muga):
    oker1_beh,oker2_beh = beheko_muga,beheko_muga
    oker1_goi,oker2_goi = goiko_muga,goiko_muga
    while beheko_muga in {oker1_beh,oker1_goi,oker2_beh,oker2_goi} or \
            goiko_muga in {oker1_beh,oker1_goi,oker2_beh,oker2_goi} or \
            oker1_beh in {oker2_beh,oker2_goi} or \
            oker1_goi in {oker2_beh,oker2_goi}:
        if zuzena < 1000:
            oker1_beh = round(random.randint(1,9) * 10 ** round(random.gauss(1.5,1)),-2)
            oker2_beh = round(random.randint(1,9) * 10 ** round(random.gauss(1.5,1)),-2)
        else:
            n = math.floor(math.log(zuzena,10))
            oker1_beh = round(random.randint(1,9) * 10 ** round(random.gauss(n,1)),-2)
            oker2_beh = round(random.randint(1,9) * 10 ** round(random.gauss(n,1)),-2)

        if oker1_beh < 1000:
            oker1_goi = oker1_beh + 100
        else:
            n = math.floor(math.log(oker1_beh,10))
            oker1_goi = oker1_beh + 10 ** (n - 1)

        if oker2_beh < 1000:
            oker2_goi = oker2_beh + 100
        else:
            n = math.floor(math.log(oker2_beh,10))
            oker2_goi = oker2_beh + 10 ** (n - 1)

    oker1 = f"{oker1_beh:,.0f} - {oker1_goi:,.0f}".replace(",",".")
    oker2 = f"{oker2_beh:,.0f} - {oker2_goi:,.0f}".replace(",",".")
    return oker1, oker2


# Elementua eta erantzun posible guztiak pasata, lortu honi buruzko galdera bat
def getGaldera(item,herria):
    try:
        mota = 'Biztanleria'  # Galdera mota
        iturria = 'Wikipedia'  # Galderaren jatorria edo iturria
        galdera = 'Zenbat biztanle ditu ' + herria + ' udalerriak?'  # Testuzko galdera
        irudia = getIrudia(item)
        erantzuna,zuzena,beheko_muga,goiko_muga = getPopulazioa(item)
        link = getArtikuluEsteka(herria)
        oker1,oker2 = getOkerrak(zuzena,beheko_muga,goiko_muga)
        galdera_osoa = "%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
            mota,galdera,irudia,erantzuna,oker1,oker2,iturria,link,"MikelBa")  # galdera osatu csv formaturako prestatuz
    except:
        galdera_osoa = ''

    return galdera_osoa


def generateGalderak(kontsulta,irteera):
    f = open(irteera,'w')
    with open(kontsulta,'r') as query_file:
        QUERY = query_file.read()
    wikidata_site = pywikibot.Site("wikidata","wikidata")
    print("#### hasi da prozesua ####")
    generator = pg.WikidataSPARQLPageGenerator(QUERY,site=wikidata_site)
    f.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
        'Mota','Galdera','Irudia','Zuzena','Oker1','Oker2','Jatorria','Esteka','Egilea',
        '\n'))  # csv fitxategian idatzi goiburua
    print("#### galderak sortzen ####")
    for page in generator:
        try:
            item = page.get()
            herria = getEuskarazkoIzena(item)
            galdera_osoa = getGaldera(item,herria)  # Elementuarekin erlazionatutako galdera lortu
            if galdera_osoa != '':
                print('.')
                f.write("%s;%s" % (galdera_osoa,'\n'))  # csv fitxategian idatzi galdera
        except:
            pass
    print('\nEginda!')
    f.close()


def main():
    generateGalderak('kontsulta.rq','galderak.csv')


if __name__ == '__main__':
    main()
