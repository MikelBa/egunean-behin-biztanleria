import random
import math
import pywikibot
from pywikibot import pagegenerators as pg

#Kontsultako emaitzetatik erantzun posible guztiak lortu, ondoren erantzun oker bezala erabili ahal izateko
def getPopulazioa(item):
    #TODO tarteak bueltatu
    return int(item['claims']['P1082'][-1].getTarget().amount)

#Elementuaren euskarazko etiketa edo titulua hartu
def getEuskarazkoIzena(item):
    return item['labels']['eu']

#Elementuaren irudi nabarmendua hartu
def getIrudia(item):
    return item['claims']['P18'][0].getTarget().fileUrl()

#Elementuaren Wikipediako artikulurako esteka hartu
def getArtikuluEsteka(herria):
    site = pywikibot.Site("eu", "wikipedia")
    return pywikibot.Page(site, herria).full_url()

def getOkerrak(zuzena):
    #TODO tarteak bueltatu
    oker1, oker2 = zuzena, zuzena
    while oker1 == zuzena or oker2 == zuzena or oker1 == oker2:
        if zuzena < 100:
            oker1 = round(10**random.randint(1,4) * random.random())
            oker2 = round(10**random.randint(1,4) * random.random())
        else:
            n = math.floor(math.log(zuzena,10))
            oker1 = round(10**random.randint(n,n+2) * random.random())
            oker2 = round(10**random.randint(n,n+2) * random.random())
    return oker1, oker2

#Elementua eta erantzun posible guztiak pasata, lortu honi buruzko galdera bat
def getGaldera(item,herria):
    try:
        mota = 'Biztanleria' #Galdera mota
        iturria = 'Wikipedia' #Galderaren jatorria edo iturria
        galdera = 'Zenbat biztanle ditu ' + herria + ' udalerriak?' #Testuzko galdera
        irudia = getIrudia(item)
        zuzena = getPopulazioa(item)
        link = getArtikuluEsteka(herria)
        oker1, oker2 = getOkerrak(zuzena)
        galdera_osoa = "%s;%s;%s;%s;%s;%s;%s;%s;%s" % (mota,galdera,irudia,zuzena,oker1,oker2,iturria,link,'MikelBa') #galdera osatu csv formaturako prestatuz
    except:
        galdera_osoa=''

    return galdera_osoa

def generateGalderak(kontsulta,irteera):
    f = open(irteera, 'w')
    with open(kontsulta, 'r') as query_file:
        QUERY = query_file.read()
    wikidata_site = pywikibot.Site("wikidata", "wikidata")
    print("#### hasi da prozesua ####")
    generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)
    f.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % ('Mota','Galdera','Irudia','Zuzena','Oker1','Oker2','Jatorria','Esteka','Egilea','\n')) #csv fitxategian idatzi goiburua
    print("#### galderak sortzen ####")
    for page in generator:
        try:
            item = page.get()
            herria = getEuskarazkoIzena(item)
            galdera_osoa = getGaldera(item,herria) #Elementuarekin erlazionatutako galdera lortu
            if galdera_osoa!='':
                print('.')
                f.write("%s;%s" % (galdera_osoa,'\n')) #csv fitxategian idatzi galdera
        except:
            pass
    print('\nEginda!')
    f.close()

def main():
    generateGalderak('kontsulta.rq','galderak.csv')

if __name__ == '__main__':
    main()