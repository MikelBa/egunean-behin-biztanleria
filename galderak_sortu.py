import random
import math
import pandas as pd

#TODO Nafarroa eta Ipar Euskal Herriko datuak sartu.
#TODO Desberdindu Autonomiak, probintziak, lurraldeak, hiriak eta herriak.

def getOkerrak(zuzena):
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

def getGaldera(herria,biztanleria):
    try:
        mota='Biztanleria' #Galdera mota
        iturria='Open Data Euskadi' #Galderaren jatorria edo iturria
        galdera='Zenbat biztanle ditu ' + herria + ' udalerriak?' #Testuzko galdera
        irudia = '' #TODO irudia ipintzen saiatu
        zuzena = biztanleria
        link = '' #TODO linka gehitu
        oker1, oker2 = getOkerrak(zuzena)
        galdera_osoa = "%s;%s;%s;%s;%s;%s;%s;%s;%s" % (mota,galdera,irudia,zuzena,oker1,oker2,iturria,link,'MikelBa') # galdera osatu csv formaturako prestatuz
    except:
        galdera_osoa=''

    return galdera_osoa

def generateGalderak(sarrera, irteera):
    f = open(irteera, 'w')
    print("#### hasi da prozesua ####")
    f.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % ('Mota','Galdera','Irudia','Zuzena','Oker1','Oker2','Jatorria','Esteka','Egilea','\n')) #csv fitxategian idatzi goiburua
    print("#### galderak sortzen ####")
    biztanleria = pd.read_csv(sarrera, sep=';', index_col='lurralde eremua', encoding='unicode_escape')
    for herria in biztanleria.index:
        try:
            galdera_osoa = getGaldera(herria,biztanleria.loc[herria,'2019']) #Elementuarekin erlazionatutako galdera lortu
            if galdera_osoa!='':
                print('.')
                f.write("%s;%s" % (galdera_osoa,'\n')) #csv fitxategian idatzi galdera
        except:
            pass
    print('\nEginda!')
    f.close()

def main():
    generateGalderak('biztanleria.csv', 'galderak.csv')

if __name__ == '__main__':
    main()