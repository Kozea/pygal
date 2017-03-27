French map
----------

Installing
~~~~~~~~~~

The french map plugin can be installed by doing a:

.. code-block:: bash

  pip install pygal_maps_fr


Department
~~~~~~~~~~

Then you will have access to the ``pygal.maps.fr`` module.

You can now plot departments (see below for the list):

.. pygal-code::

  fr_chart = pygal.maps.fr.Departments()
  fr_chart.title = 'Some departments'
  fr_chart.add('Métropole', ['69', '92', '13'])
  fr_chart.add('Corse', ['2A', '2B'])
  fr_chart.add('DOM COM', ['971', '972', '973', '974'])

Or specify an number for a department:

.. pygal-code::

  fr_chart = pygal.maps.fr.Departments(human_readable=True)
  fr_chart.title = 'Population by department'
  fr_chart.add('In 2011', {
    '01': 603827, '02': 541302, '03': 342729, '04': 160959, '05': 138605, '06': 1081244, '07': 317277, '08': 283110, '09': 152286, '10': 303997, '11': 359967, '12': 275813, '13': 1975896, '14': 685262, '15': 147577, '16': 352705, '17': 625682, '18': 311694, '19': 242454, '2A': 145846, '2B': 168640, '21': 525931, '22': 594375, '23': 122560, '24': 415168, '25': 529103, '26': 487993, '27': 588111, '28': 430416, '29': 899870, '30': 718357, '31': 1260226, '32': 188893, '33': 1463662, '34': 1062036, '35': 996439, '36': 230175, '37': 593683, '38': 1215212, '39': 261294, '40': 387929, '41': 331280, '42': 749053, '43': 224907, '44': 1296364, '45': 659587, '46': 174754, '47': 330866, '48': 77156, '49': 790343, '50': 499531, '51': 566571, '52': 182375, '53': 307031, '54': 733124, '55': 193557, '56': 727083, '57': 1045146, '58': 218341, '59': 2579208, '60': 805642, '61': 290891, '62': 1462807, '63': 635469, '64': 656608, '65': 229228, '66': 452530, '67': 1099269, '68': 753056, '69': 1744236, '70': 239695, '71': 555999, '72': 565718, '73': 418949, '74': 746994, '75': 2249975, '76': 1251282, '77': 1338427, '78': 1413635, '79': 370939, '80': 571211, '81': 377675, '82': 244545, '83': 1012735, '84': 546630, '85': 641657, '86': 428447, '87': 376058, '88': 378830, '89': 342463, '90': 143348, '91': 1225191, '92': 1581628, '93': 1529928, '94': 1333702, '95': 1180365, '971': 404635, '972': 392291, '973': 237549, '974': 828581, '976': 212645
  })


Regions
~~~~~~~

You can do the same with regions:


.. pygal-code::

  fr_chart = pygal.maps.fr.Regions()
  fr_chart.title = 'Some regions'
  fr_chart.add('Métropole', ['82', '11', '93'])
  fr_chart.add('Corse', ['94'])
  fr_chart.add('DOM COM', ['01', '02', '03', '04'])


You can also specify a number for a region and use a department to region aggregation:


.. pygal-code::

  from pygal.maps.fr import aggregate_regions
  fr_chart = pygal.maps.fr.Regions(human_readable=True)
  fr_chart.title = 'Population by region'
  fr_chart.add('In 2011', aggregate_regions({
    '01': 603827, '02': 541302, '03': 342729, '04': 160959, '05': 138605, '06': 1081244, '07': 317277, '08': 283110, '09': 152286, '10': 303997, '11': 359967, '12': 275813, '13': 1975896, '14': 685262, '15': 147577, '16': 352705, '17': 625682, '18': 311694, '19': 242454, '2A': 145846, '2B': 168640, '21': 525931, '22': 594375, '23': 122560, '24': 415168, '25': 529103, '26': 487993, '27': 588111, '28': 430416, '29': 899870, '30': 718357, '31': 1260226, '32': 188893, '33': 1463662, '34': 1062036, '35': 996439, '36': 230175, '37': 593683, '38': 1215212, '39': 261294, '40': 387929, '41': 331280, '42': 749053, '43': 224907, '44': 1296364, '45': 659587, '46': 174754, '47': 330866, '48': 77156, '49': 790343, '50': 499531, '51': 566571, '52': 182375, '53': 307031, '54': 733124, '55': 193557, '56': 727083, '57': 1045146, '58': 218341, '59': 2579208, '60': 805642, '61': 290891, '62': 1462807, '63': 635469, '64': 656608, '65': 229228, '66': 452530, '67': 1099269, '68': 753056, '69': 1744236, '70': 239695, '71': 555999, '72': 565718, '73': 418949, '74': 746994, '75': 2249975, '76': 1251282, '77': 1338427, '78': 1413635, '79': 370939, '80': 571211, '81': 377675, '82': 244545, '83': 1012735, '84': 546630, '85': 641657, '86': 428447, '87': 376058, '88': 378830, '89': 342463, '90': 143348, '91': 1225191, '92': 1581628, '93': 1529928, '94': 1333702, '95': 1180365, '971': 404635, '972': 392291, '973': 237549, '974': 828581, '976': 212645
  }))


Department list
~~~~~~~~~~~~~~~

====  ========================
code  Department
====  ========================
01    Ain
02    Aisne
03    Allier
04    Alpes-de-Haute-Provence
05    Hautes-Alpes
06    Alpes-Maritimes
07    Ardèche
08    Ardennes
09    Ariège
10    Aube
11    Aude
12    Aveyron
13    Bouches-du-Rhône
14    Calvados
15    Cantal
16    Charente
17    Charente-Maritime
18    Cher
19    Corrèze
2A    Corse-du-Sud
2B    Haute-Corse
21    Côte-d'Or
22    Côtes-d'Armor
23    Creuse
24    Dordogne
25    Doubs
26    Drôme
27    Eure
28    Eure-et-Loir
29    Finistère
30    Gard
31    Haute-Garonne
32    Gers
33    Gironde
34    Hérault
35    Ille-et-Vilaine
36    Indre
37    Indre-et-Loire
38    Isère
39    Jura
40    Landes
41    Loir-et-Cher
42    Loire
43    Haute-Loire
44    Loire-Atlantique
45    Loiret
46    Lot
47    Lot-et-Garonne
48    Lozère
49    Maine-et-Loire
50    Manche
51    Marne
52    Haute-Marne
53    Mayenne
54    Meurthe-et-Moselle
55    Meuse
56    Morbihan
57    Moselle
58    Nièvre
59    Nord
60    Oise
61    Orne
62    Pas-de-Calais
63    Puy-de-Dôme
64    Pyrénées-Atlantiques
65    Hautes-Pyrénées
66    Pyrénées-Orientales
67    Bas-Rhin
68    Haut-Rhin
69    Rhône
70    Haute-Saône
71    Saône-et-Loire
72    Sarthe
73    Savoie
74    Haute-Savoie
75    Paris
76    Seine-Maritime
77    Seine-et-Marne
78    Yvelines
79    Deux-Sèvres
80    Somme
81    Tarn
82    Tarn-et-Garonne
83    Var
84    Vaucluse
85    Vendée
86    Vienne
87    Haute-Vienne
88    Vosges
89    Yonne
90    Territoire de Belfort
91    Essonne
92    Hauts-de-Seine
93    Seine-Saint-Denis
94    Val-de-Marne
95    Val-d'Oise
971   Guadeloupe
972   Martinique
973   Guyane
974   Réunion
975   Saint Pierre et Miquelon
976   Mayotte
====  ========================


Region list
~~~~~~~~~~~

====  ===================
code  Region
====  ===================
11    Île-de-France
21    Champagne-Ardenne
22    Picardie
23    Haute-Normandie
24    Centre
25    Basse-Normandie
26    Bourgogne
31    Nord-Pas-de-Calais
41    Lorraine
42    Alsace
43    Franche-Comté
52    Pays-de-la-Loire
53    Bretagne
54    Poitou-Charentes
72    Aquitaine
73    Midi-Pyrénées
74    Limousin
82    Rhône-Alpes
83    Auvergne
91    Languedoc-Roussillon
93    Provence-Alpes-Côte d'Azur
94    Corse
01    Guadeloupe
02    Martinique
03    Guyane
04    Réunion
05    Saint Pierre et Miquelon
06    Mayotte
====  ===================
