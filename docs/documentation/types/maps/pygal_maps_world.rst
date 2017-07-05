World map
---------

Installing
~~~~~~~~~~

The world map plugin can be installed by doing a:

.. code-block:: bash

  pip install pygal_maps_world


Countries
~~~~~~~~~

Then you will have acces to the ``pygal.maps.world`` module.
Now you can plot countries by specifying their code (see below for the big list of supported country codes)

.. pygal-code::

  worldmap_chart = pygal.maps.world.World()
  worldmap_chart.title = 'Some countries'
  worldmap_chart.add('F countries', ['fr', 'fi'])
  worldmap_chart.add('M countries', ['ma', 'mc', 'md', 'me', 'mg',
                                     'mk', 'ml', 'mm', 'mn', 'mo',
                                     'mr', 'mt', 'mu', 'mv', 'mw',
                                     'mx', 'my', 'mz'])
  worldmap_chart.add('U countries', ['ua', 'ug', 'us', 'uy', 'uz'])


You can also specify a value for a country:

.. pygal-code::

  worldmap_chart = pygal.maps.world.World()
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

Continents
~~~~~~~~~~

You have also access to continents:

.. pygal-code::

        supra = pygal.maps.world.SupranationalWorld()
        supra.add('Asia', [('asia', 1)])
        supra.add('Europe', [('europe', 1)])
        supra.add('Africa', [('africa', 1)])
        supra.add('North america', [('north_america', 1)])
        supra.add('South america', [('south_america', 1)])
        supra.add('Oceania', [('oceania', 1)])
        supra.add('Antartica', [('antartica', 1)])


Coutry code list
~~~~~~~~~~~~~~~~

The following countries are supported:

====   ============================================
code   Country
====   ============================================
ad     Andorra
ae     United Arab Emirates
af     Afghanistan
al     Albania
am     Armenia
ao     Angola
aq     Antarctica
ar     Argentina
at     Austria
au     Australia
az     Azerbaijan
ba     Bosnia and Herzegovina
bd     Bangladesh
be     Belgium
bf     Burkina Faso
bg     Bulgaria
bh     Bahrain
bi     Burundi
bj     Benin
bn     Brunei Darussalam
bo     Bolivia, Plurinational State of
br     Brazil
bt     Bhutan
bw     Botswana
by     Belarus
bz     Belize
ca     Canada
cd     Congo, the Democratic Republic of the
cf     Central African Republic
cg     Congo
ch     Switzerland
ci     Cote d'Ivoire
cl     Chile
cm     Cameroon
cn     China
co     Colombia
cr     Costa Rica
cu     Cuba
cv     Cape Verde
cy     Cyprus
cz     Czech Republic
de     Germany
dj     Djibouti
dk     Denmark
do     Dominican Republic
dz     Algeria
ec     Ecuador
ee     Estonia
eg     Egypt
eh     Western Sahara
er     Eritrea
es     Spain
et     Ethiopia
fi     Finland
fr     France
ga     Gabon
gb     United Kingdom
ge     Georgia
gf     French Guiana
gh     Ghana
gl     Greenland
gm     Gambia
gn     Guinea
gq     Equatorial Guinea
gr     Greece
gt     Guatemala
gu     Guam
gw     Guinea-Bissau
gy     Guyana
hk     Hong Kong
hn     Honduras
hr     Croatia
ht     Haiti
hu     Hungary
id     Indonesia
ie     Ireland
il     Israel
in     India
iq     Iraq
ir     Iran, Islamic Republic of
is     Iceland
it     Italy
jm     Jamaica
jo     Jordan
jp     Japan
ke     Kenya
kg     Kyrgyzstan
kh     Cambodia
kp     Korea, Democratic People's Republic of
kr     Korea, Republic of
kw     Kuwait
kz     Kazakhstan
la     Lao People's Democratic Republic
lb     Lebanon
li     Liechtenstein
lk     Sri Lanka
lr     Liberia
ls     Lesotho
lt     Lithuania
lu     Luxembourg
lv     Latvia
ly     Libyan Arab Jamahiriya
ma     Morocco
mc     Monaco
md     Moldova, Republic of
me     Montenegro
mg     Madagascar
mk     Macedonia, the former Yugoslav Republic of
ml     Mali
mm     Myanmar
mn     Mongolia
mo     Macao
mr     Mauritania
mt     Malta
mu     Mauritius
mv     Maldives
mw     Malawi
mx     Mexico
my     Malaysia
mz     Mozambique
na     Namibia
ne     Niger
ng     Nigeria
ni     Nicaragua
nl     Netherlands
no     Norway
np     Nepal
nz     New Zealand
om     Oman
pa     Panama
pe     Peru
pg     Papua New Guinea
ph     Philippines
pk     Pakistan
pl     Poland
pr     Puerto Rico
ps     Palestine, State of
pt     Portugal
py     Paraguay
re     Reunion
ro     Romania
rs     Serbia
ru     Russian Federation
rw     Rwanda
sa     Saudi Arabia
sc     Seychelles
sd     Sudan
se     Sweden
sg     Singapore
sh     Saint Helena, Ascension and Tristan da Cunha
si     Slovenia
sk     Slovakia
sl     Sierra Leone
sm     San Marino
sn     Senegal
so     Somalia
sr     Suriname
st     Sao Tome and Principe
sv     El Salvador
sy     Syrian Arab Republic
sz     Swaziland
td     Chad
tg     Togo
th     Thailand
tj     Tajikistan
tl     Timor-Leste
tm     Turkmenistan
tn     Tunisia
tr     Turkey
tw     Taiwan (Republic of China)
tz     Tanzania, United Republic of
ua     Ukraine
ug     Uganda
us     United States
uy     Uruguay
uz     Uzbekistan
va     Holy See (Vatican City State)
ve     Venezuela, Bolivarian Republic of
vn     Viet Nam
ye     Yemen
yt     Mayotte
za     South Africa
zm     Zambia
zw     Zimbabwe
====   ============================================


Continent list
~~~~~~~~~~~~~~

=============  =============
code           name
=============  =============
asia           Asia
europe         Europe
africa         Africa
north_america  North America
south_america  South America
oceania        Oceania
antartica      Antartica
=============  =============

