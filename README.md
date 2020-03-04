# egunean-behin-biztanleria
Egunean Behin jokorako biztanleriari buruzko galderak sortzeko programa. Sortzen diren galderen 20 adibide topa daitezke `galderak.csv` dokumentuan.

## Ze galdera mota sortzen ditu progra honek?
Programa honek, Euskal Herriko udalerri desberdinen biztanleria zein den galdetzen digu. Hiru aukera eskaintzen dira erantzuteko eta bakarra da zuzena. Erantzunak ez dira zifra zehatzak, tarteak baizik.

Hurrengoko adibidearekin argi ikusten da nolakoak diren sortzen diren galderak:

|  Zenbat biztanle ditu Eltziego udalerriak? |
|:-:|
|  1.000 - 1.100 |
|  60.000 - 61.000 |
|  400 - 500 |

Kasu honetan, erantzun zuzena lehena da, 1.000-1.100 biztanle tartea.

# Nola sortzen dira galderak?

Galdera hauek sortzeko Ion Lizarazuk [Githubera](https://github.com/egunean-behin/egunean_behin_wikidata_perretxikoak) igo zuen Perretxikoen adibidea erabili da oinarri bezala. 

 Euskal Herriko udalerrietako biztanleriaren datua Wikipediatik aterata dago. Datu hori lortzeko Wikidatako Query sisteman kontsulta bat idatzi da eta kontsulta horretatik hainbat datu ateratzen ditugu: biztanleria zehatza (kasu askotan 2019 urteko datua da, baina udalerri batzuen kasuan datua zaharragoa da), udalerriaren euskarazko izena eta udalerriaren argazkiren bat (baldin badago).

 Behin biztanleriaren datu zehatza izanda, erantzun zuzena eta bi oker prestatu behar dira. Horretarako `getPopulazioa` eta `getOkerrak` funtzioak prestatu dira.

 ### getPopulazioa
 Funtzio honek kontsultatu hartzen du sarrera bezala. Hortik abiatuz, kontsutatzen ari garen udalerriaren biztanleria lortzen du eta zifra hori barnean duen tarte bat bueltatzen du. Tartearen tamaina, zifra horren tamainaren araberakoa da. Bi kasu bereiztu behar dira:

* Kontsultatu dugun udalerriaren biztanleria datua 1000 baino txikiagoa bada, soluzioa 100eko tarte bat izango da non beheko eta goiko mugak ehunen multiploak diren eta datu zehatza tartearen barnean dagoen. Hau da, biztanleria datu zehatza 76 bada, bueltatuko den tartea 0-100 da. Aldiz, erantzuna 760 bada, bueltatuko den tartea 700-800 da.
* Kontsultatu dugun udalerriaren biztanleria datuaren balioa 1.000 edo handiagokoa bada, orduan, bueltatuko dugun tartea zenbaki horren balioaren araberakoa izango da. Demagun biztanleria datu zehatza 16.784 dela, orduan bueltatuko litzatekeen tartea 16.000-17.000 izango zen. Aldiz, biztanleria datu zehatza 167.840 balitz, 160.000-170.000 tartea bultatuko luke funztioak.

### getOkerrak
Erantzun okerrak tarteak dira ere. Tarte horiek sortzeko prozesua honako hau da:

1. Erantzun okerren beheko muga lortzea da lehenengo pausua. Horretarako, berriro ere bi kasu bereizten ditugu:

    * Udalerriaren biztanle kopurua 1.000 baino txikiagokoa bada, orduan tartearen beheko muga sortzeko ondoko prozedura jarraitzen dugu:

        ```
        round(random.randint(1,9) * 10 ** round(random.gauss(1.5,1)),-2)
        ```

        Hau da, lehenik eta behin  `round(random.gauss(1.5,1))` egiterakoan lortzen dugun zenbakia [-1,4] tartean egongo da %95eko biano probabilitate handiagoaz ([Gaussen distribuzioa](https://en.wikipedia.org/wiki/Normal_distribution#/media/File:Empirical_Rule.PNG)). Orduan, `random.randint(1,9) * 10 ** round(random.gauss(1.5,1))` zenbakia (0,90.000] tartean egongo da lehengo probabilitate berdinez. Azkenik, zenbaki hori ehunekoetara borobiltzen dugu.

    * Udalerriaren biztanle  kopurua 1.000 edo gehiagokoa bada, beheko muga ondoko eran lortzen da:

        ```
        n = math.floor(math.log(zuzena,10))
        round(random.randint(1,9) * 10 ** round(random.gauss(n,1)),-2)
        ```
    
2. Behin erantzun okerraren beheko muga lortuta, goiko muga lortzeko gehiketa bat bakarrik egiten dugu. Bi kasu daude berriro ere:

    * Beheko mugaren balioa 1.000 baino txikiagoa bada, goiko muga balio horri 100 gehituz lortzen dugu.
    * Bestela, ondoko prozedura jarraitzen dugu:

        ```
        n = math.floor(math.log(oker_beh,10))
        oker_goi = oker_beh + 10 ** (n - 1)
        ```
        Horrela, gure beheko muga 16.000 bada, goiko muga 17.000 izango da.

3. Azkenik, pauso hauek errepikatzen ditugu tarte guztiak desberdinak izan arte. Hala ere, gerta litekeenez tarte bat 1.000-2.000 eta beste bat 2.000-3.000 izatea. Kasu horretan, bi aukeretan dago 2.000 zenbakia. Horrelako konfusioak ekiditzeko, behe eta goi muga guztiak desberdinak izatea eskatu diogu funtzioari.


