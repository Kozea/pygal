Worldmap charts
---------------

Basic
~~~~~

Highlight some countries:

.. pygal-code::

  worldmap_chart = pygal.Worldmap()
  worldmap_chart.title = 'Some countries'
  worldmap_chart.add('F countries', ['fr', 'fi'])
  worldmap_chart.add('M countries', ['ma', 'mc', 'md', 'me', 'mg',
                                     'mk', 'ml', 'mm', 'mn', 'mo',
                                     'mr', 'mt', 'mu', 'mv', 'mw',
                                     'mx', 'my', 'mz'])
  worldmap_chart.add('U countries', ['ua', 'ug', 'us', 'uy', 'uz'])


You can also specify an number for a country:

.. pygal-code::

  worldmap_chart = pygal.Worldmap()
  worldmap_chart.title = 'Minimum deaths by capital punishement (source: Amnesty International)'
  worldmap_chart.add('In 2012', {
    'af': 14,
    'bd': 1,
    'by': 3,
    'cn': 1000,
    'gm': 9,
    'in': 1,
    'ir': 314,
    'iq': 129,
    'jp': 7,
    'kp': 6,
    'pk': 1,
    'ps': 6,
    'sa': 79,
    'so': 6,
    'sd': 5,
    'tw': 6,
    'ae': 1,
    'us': 43,
    'ye': 28
  })


The following countries are supported:

    - `ad`: Andorra
    - `ae`: United Arab Emirates
    - `af`: Afghanistan
    - `al`: Albania
    - `am`: Armenia
    - `ao`: Angola
    - `aq`: Antarctica
    - `ar`: Argentina
    - `at`: Austria
    - `au`: Australia
    - `az`: Azerbaijan
    - `ba`: Bosnia and Herzegovina
    - `bd`: Bangladesh
    - `be`: Belgium
    - `bf`: Burkina Faso
    - `bg`: Bulgaria
    - `bh`: Bahrain
    - `bi`: Burundi
    - `bj`: Benin
    - `bn`: Brunei Darussalam
    - `bo`: Bolivia, Plurinational State of
    - `br`: Brazil
    - `bt`: Bhutan
    - `bw`: Botswana
    - `by`: Belarus
    - `bz`: Belize
    - `ca`: Canada
    - `cd`: Congo, the Democratic Republic of the
    - `cf`: Central African Republic
    - `cg`: Congo
    - `ch`: Switzerland
    - `ci`: Cote d'Ivoire
    - `cl`: Chile
    - `cm`: Cameroon
    - `cn`: China
    - `co`: Colombia
    - `cr`: Costa Rica
    - `cu`: Cuba
    - `cv`: Cape Verde
    - `cy`: Cyprus
    - `cz`: Czech Republic
    - `de`: Germany
    - `dj`: Djibouti
    - `dk`: Denmark
    - `do`: Dominican Republic
    - `dz`: Algeria
    - `ec`: Ecuador
    - `ee`: Estonia
    - `eg`: Egypt
    - `eh`: Western Sahara
    - `er`: Eritrea
    - `es`: Spain
    - `et`: Ethiopia
    - `fi`: Finland
    - `fr`: France
    - `ga`: Gabon
    - `gb`: United Kingdom
    - `ge`: Georgia
    - `gf`: French Guiana
    - `gh`: Ghana
    - `gl`: Greenland
    - `gm`: Gambia
    - `gn`: Guinea
    - `gq`: Equatorial Guinea
    - `gr`: Greece
    - `gt`: Guatemala
    - `gu`: Guam
    - `gw`: Guinea-Bissau
    - `gy`: Guyana
    - `hk`: Hong Kong
    - `hn`: Honduras
    - `hr`: Croatia
    - `ht`: Haiti
    - `hu`: Hungary
    - `id`: Indonesia
    - `ie`: Ireland
    - `il`: Israel
    - `in`: India
    - `iq`: Iraq
    - `ir`: Iran, Islamic Republic of
    - `is`: Iceland
    - `it`: Italy
    - `jm`: Jamaica
    - `jo`: Jordan
    - `jp`: Japan
    - `ke`: Kenya
    - `kg`: Kyrgyzstan
    - `kh`: Cambodia
    - `kp`: Korea, Democratic People's Republic of
    - `kr`: Korea, Republic of
    - `kw`: Kuwait
    - `kz`: Kazakhstan
    - `la`: Lao People's Democratic Republic
    - `lb`: Lebanon
    - `li`: Liechtenstein
    - `lk`: Sri Lanka
    - `lr`: Liberia
    - `ls`: Lesotho
    - `lt`: Lithuania
    - `lu`: Luxembourg
    - `lv`: Latvia
    - `ly`: Libyan Arab Jamahiriya
    - `ma`: Morocco
    - `mc`: Monaco
    - `md`: Moldova, Republic of
    - `me`: Montenegro
    - `mg`: Madagascar
    - `mk`: Macedonia, the former Yugoslav Republic of
    - `ml`: Mali
    - `mm`: Myanmar
    - `mn`: Mongolia
    - `mo`: Macao
    - `mr`: Mauritania
    - `mt`: Malta
    - `mu`: Mauritius
    - `mv`: Maldives
    - `mw`: Malawi
    - `mx`: Mexico
    - `my`: Malaysia
    - `mz`: Mozambique
    - `na`: Namibia
    - `ne`: Niger
    - `ng`: Nigeria
    - `ni`: Nicaragua
    - `nl`: Netherlands
    - `no`: Norway
    - `np`: Nepal
    - `nz`: New Zealand
    - `om`: Oman
    - `pa`: Panama
    - `pe`: Peru
    - `pg`: Papua New Guinea
    - `ph`: Philippines
    - `pk`: Pakistan
    - `pl`: Poland
    - `pr`: Puerto Rico
    - `ps`: Palestine, State of
    - `pt`: Portugal
    - `py`: Paraguay
    - `re`: Reunion
    - `ro`: Romania
    - `rs`: Serbia
    - `ru`: Russian Federation
    - `rw`: Rwanda
    - `sa`: Saudi Arabia
    - `sc`: Seychelles
    - `sd`: Sudan
    - `se`: Sweden
    - `sg`: Singapore
    - `sh`: Saint Helena, Ascension and Tristan da Cunha
    - `si`: Slovenia
    - `sk`: Slovakia
    - `sl`: Sierra Leone
    - `sm`: San Marino
    - `sn`: Senegal
    - `so`: Somalia
    - `sr`: Suriname
    - `st`: Sao Tome and Principe
    - `sv`: El Salvador
    - `sy`: Syrian Arab Republic
    - `sz`: Swaziland
    - `td`: Chad
    - `tg`: Togo
    - `th`: Thailand
    - `tj`: Tajikistan
    - `tl`: Timor-Leste
    - `tm`: Turkmenistan
    - `tn`: Tunisia
    - `tr`: Turkey
    - `tw`: Taiwan, Province of China
    - `tz`: Tanzania, United Republic of
    - `ua`: Ukraine
    - `ug`: Uganda
    - `us`: United States
    - `uy`: Uruguay
    - `uz`: Uzbekistan
    - `va`: Holy See (Vatican City State)
    - `ve`: Venezuela, Bolivarian Republic of
    - `vn`: Viet Nam
    - `ye`: Yemen
    - `yt`: Mayotte
    - `za`: South Africa
    - `zm`: Zambia
    - `zw`: Zimbabwe


Country charts
--------------

As of now, only France is available. As other country are implemented, this will be externalized in other packages.
(Please submit pull requests :))

French map
~~~~~~~~~~

Highlight some departments:


.. pygal-code::

  fr_chart = pygal.FrenchMap_Departments()
  fr_chart.title = 'Some departments'
  fr_chart.add('Métropole', ['69', '92', '13'])
  fr_chart.add('Corse', ['2A', '2B'])
  fr_chart.add('DOM COM', ['971', '972', '973', '974'])

You can also specify an number for a department:

.. pygal-code::

  fr_chart = pygal.FrenchMap_Departments(human_readable=True)
  fr_chart.title = 'Population by department'
  fr_chart.add('In 2011', {
    '01': 603827,
    '02': 541302,
    '03': 342729,
    '04': 160959,
    '05': 138605,
    '06': 1081244,
    '07': 317277,
    '08': 283110,
    '09': 152286,
    '10': 303997,
    '11': 359967,
    '12': 275813,
    '13': 1975896,
    '14': 685262,
    '15': 147577,
    '16': 352705,
    '17': 625682,
    '18': 311694,
    '19': 242454,
    '2A': 145846,
    '2B': 168640,
    '21': 525931,
    '22': 594375,
    '23': 122560,
    '24': 415168,
    '25': 529103,
    '26': 487993,
    '27': 588111,
    '28': 430416,
    '29': 899870,
    '30': 718357,
    '31': 1260226,
    '32': 188893,
    '33': 1463662,
    '34': 1062036,
    '35': 996439,
    '36': 230175,
    '37': 593683,
    '38': 1215212,
    '39': 261294,
    '40': 387929,
    '41': 331280,
    '42': 749053,
    '43': 224907,
    '44': 1296364,
    '45': 659587,
    '46': 174754,
    '47': 330866,
    '48': 77156,
    '49': 790343,
    '50': 499531,
    '51': 566571,
    '52': 182375,
    '53': 307031,
    '54': 733124,
    '55': 193557,
    '56': 727083,
    '57': 1045146,
    '58': 218341,
    '59': 2579208,
    '60': 805642,
    '61': 290891,
    '62': 1462807,
    '63': 635469,
    '64': 656608,
    '65': 229228,
    '66': 452530,
    '67': 1099269,
    '68': 753056,
    '69': 1744236,
    '70': 239695,
    '71': 555999,
    '72': 565718,
    '73': 418949,
    '74': 746994,
    '75': 2249975,
    '76': 1251282,
    '77': 1338427,
    '78': 1413635,
    '79': 370939,
    '80': 571211,
    '81': 377675,
    '82': 244545,
    '83': 1012735,
    '84': 546630,
    '85': 641657,
    '86': 428447,
    '87': 376058,
    '88': 378830,
    '89': 342463,
    '90': 143348,
    '91': 1225191,
    '92': 1581628,
    '93': 1529928,
    '94': 1333702,
    '95': 1180365,
    '971': 404635,
    '972': 392291,
    '973': 237549,
    '974': 828581,
    '976': 212645
  })

You can do the same with regions:


.. pygal-code::

  fr_chart = pygal.FrenchMap_Regions()
  fr_chart.title = 'Some regions'
  fr_chart.add('Métropole', ['82', '11', '93'])
  fr_chart.add('Corse', ['94'])
  fr_chart.add('DOM COM', ['01', '02', '03', '04'])


You can also specify a number for a region and use a department to region aggregation:


.. pygal-code::

  from pygal.graph.frenchmap import aggregate_regions
  fr_chart = pygal.FrenchMap_Regions(human_readable=True)
  fr_chart.title = 'Population by region'
  fr_chart.add('In 2011', aggregate_regions({
    '01': 603827,
    '02': 541302,
    '03': 342729,
    '04': 160959,
    '05': 138605,
    '06': 1081244,
    '07': 317277,
    '08': 283110,
    '09': 152286,
    '10': 303997,
    '11': 359967,
    '12': 275813,
    '13': 1975896,
    '14': 685262,
    '15': 147577,
    '16': 352705,
    '17': 625682,
    '18': 311694,
    '19': 242454,
    '2A': 145846,
    '2B': 168640,
    '21': 525931,
    '22': 594375,
    '23': 122560,
    '24': 415168,
    '25': 529103,
    '26': 487993,
    '27': 588111,
    '28': 430416,
    '29': 899870,
    '30': 718357,
    '31': 1260226,
    '32': 188893,
    '33': 1463662,
    '34': 1062036,
    '35': 996439,
    '36': 230175,
    '37': 593683,
    '38': 1215212,
    '39': 261294,
    '40': 387929,
    '41': 331280,
    '42': 749053,
    '43': 224907,
    '44': 1296364,
    '45': 659587,
    '46': 174754,
    '47': 330866,
    '48': 77156,
    '49': 790343,
    '50': 499531,
    '51': 566571,
    '52': 182375,
    '53': 307031,
    '54': 733124,
    '55': 193557,
    '56': 727083,
    '57': 1045146,
    '58': 218341,
    '59': 2579208,
    '60': 805642,
    '61': 290891,
    '62': 1462807,
    '63': 635469,
    '64': 656608,
    '65': 229228,
    '66': 452530,
    '67': 1099269,
    '68': 753056,
    '69': 1744236,
    '70': 239695,
    '71': 555999,
    '72': 565718,
    '73': 418949,
    '74': 746994,
    '75': 2249975,
    '76': 1251282,
    '77': 1338427,
    '78': 1413635,
    '79': 370939,
    '80': 571211,
    '81': 377675,
    '82': 244545,
    '83': 1012735,
    '84': 546630,
    '85': 641657,
    '86': 428447,
    '87': 376058,
    '88': 378830,
    '89': 342463,
    '90': 143348,
    '91': 1225191,
    '92': 1581628,
    '93': 1529928,
    '94': 1333702,
    '95': 1180365,
    '971': 404635,
    '972': 392291,
    '973': 237549,
    '974': 828581,
    '976': 212645
  }))

