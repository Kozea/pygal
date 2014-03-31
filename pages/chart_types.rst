===============
 Documentation
===============


Chart types
===========

pygal provides 10 kinds of charts:

.. contents::

Line charts
-----------

Basic
~~~~~

Basic simple line graph:

.. pygal-code::

  line_chart = pygal.Line()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

Stacked
~~~~~~~

Same graph but with stacked values and filled rendering:

.. pygal-code::

  stackedline_chart = pygal.StackedLine(fill=True)
  stackedline_chart.title = 'Browser usage evolution (in %)'
  stackedline_chart.x_labels = map(str, range(2002, 2013))
  stackedline_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  stackedline_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  stackedline_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  stackedline_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Bar charts / Histograms
-----------------------

Basic
~~~~~

Basic simple bar graph:

.. pygal-code::

  bar_chart = pygal.Bar()
  bar_chart.title = 'Browser usage evolution (in %)'
  bar_chart.x_labels = map(str, range(2002, 2013))
  bar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  bar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  bar_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  bar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Stacked
~~~~~~~

Same graph but with stacked values:

.. pygal-code::

  stackedbar_chart = pygal.StackedBar()
  stackedbar_chart.title = 'Browser usage evolution (in %)'
  stackedbar_chart.x_labels = map(str, range(2002, 2013))
  stackedbar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  stackedbar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  stackedbar_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  stackedbar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Horizontal
~~~~~~~~~~

Horizontal bar diagram:

.. pygal-code::

  horizontalbar_chart = pygal.HorizontalBar()
  horizontalbar_chart.title = 'Browser usage in February 2012 (in %)'
  horizontalbar_chart.add('IE', 19.5)
  horizontalbar_chart.add('Firefox', 36.6)
  horizontalbar_chart.add('Chrome', 36.3)
  horizontalbar_chart.add('Safari', 4.5)
  horizontalbar_chart.add('Opera', 2.3)


XY charts
---------

Basic
~~~~~

Basic XY lines, drawing cosinus:

.. pygal-code::

  from math import cos
  xy_chart = pygal.XY()
  xy_chart.title = 'XY Cosinus'
  xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
  xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
  xy_chart.add('x = 1',  [(1, -5), (1, 5)])
  xy_chart.add('x = -1', [(-1, -5), (-1, 5)])
  xy_chart.add('y = 1',  [(-5, 1), (5, 1)])
  xy_chart.add('y = -1', [(-5, -1), (5, -1)])


Scatter Plot
~~~~~~~~~~~~

Disabling stroke make a good scatter plot

.. pygal-code::

  xy_chart = pygal.XY(stroke=False)
  xy_chart.title = 'Correlation'
  xy_chart.add('A', [(0, 0), (.1, .2), (.3, .1), (.5, 1), (.8, .6), (1, 1.08), (1.3, 1.1), (2, 3.23), (2.43, 2)])
  xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
  xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])


DateY
~~~~~
You can index values by dates (Thanks to `Snarkturne <https://github.com/snarkturne>`_)

.. pygal-code::

  from datetime import datetime, timedelta
  datey = pygal.DateY(x_label_rotation=20)
  datey.add("Visits", [
      (datetime(2013, 1, 2), 300),
      (datetime(2013, 1, 12), 412),
      (datetime(2013, 2, 2), 823),
      (datetime(2013, 2, 22), 672)
  ])

The x axis and tool tip x labels can be specified using `x_label_format`. This uses the formatting string for strftime from `here <http://docs.python.org/2/library/time.html#time.strftime>`_

The x labels can also be specified, using an array of datetime objects.

.. pygal-code::

  from datetime import datetime, timedelta
  datey = pygal.DateY(x_label_rotation=20)
  datey.add("Visits", [
      (datetime(2013, 1, 2), 300),
      (datetime(2013, 1, 12), 412),
      (datetime(2013, 2, 2), 823),
      (datetime(2013, 2, 22), 672)
  ])
  datey.x_label_format = "%Y-%m-%d"
  datey.x_labels = [
	datetime(2013, 1, 1),
	datetime(2013, 2, 1),
	datetime(2013, 3, 1)
  ]

Pies
----

Basic
~~~~~

Simple pie:


.. pygal-code::

  pie_chart = pygal.Pie()
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)


Multi-series pie
~~~~~~~~~~~~~~~~

Same pie but divided in sub category:

.. pygal-code::

  multipie_chart = pygal.Pie()
  multipie_chart.title = 'Browser usage by version in February 2012 (in %)'
  multipie_chart.add('IE', [5.7, 10.2, 2.6, 1])
  multipie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
  multipie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
  multipie_chart.add('Safari', [4.4, .1])
  multipie_chart.add('Opera', [.1, 1.6, .1, .5])


Radar charts
------------

Basic
~~~~~

Simple Kiviat diagram:

.. pygal-code::

  radar_chart = pygal.Radar()
  radar_chart.title = 'V8 benchmark results'
  radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


Box plot
--------

Basic
~~~~~

Here's some whiskers:

.. pygal-code::

  box_plot = pygal.Box()
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


Dot charts
----------

Basic
~~~~~

Punch card like chart:

.. pygal-code::

  dot_chart = pygal.Dot(x_label_rotation=30)
  dot_chart.title = 'V8 benchmark results'
  dot_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  dot_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  dot_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  dot_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  dot_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


Funnel charts
-------------

Basic
~~~~~

Funnel chart:

.. pygal-code::

  funnel_chart = pygal.Funnel()
  funnel_chart.title = 'V8 benchmark results'
  funnel_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  funnel_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  funnel_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  funnel_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])


Gauge charts
------------

Basic
~~~~~

Simple gauge chart:

.. pygal-code::

  gauge_chart = pygal.Gauge(human_readable=True)
  gauge_chart.title = 'DeltaBlue V8 benchmark results'
  gauge_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  gauge_chart.range = [0, 10000]
  gauge_chart.add('Chrome', 8212)
  gauge_chart.add('Firefox', 8099)
  gauge_chart.add('Opera', 2933)
  gauge_chart.add('IE', 41)


Pyramid charts
--------------

Basic
~~~~~

Population pyramid:

.. pygal-code:: 600 600

  ages = [(364381, 358443, 360172, 345848, 334895, 326914, 323053, 312576, 302015, 301277, 309874, 318295, 323396, 332736, 330759, 335267, 345096, 352685, 368067, 381521, 380145, 378724, 388045, 382303, 373469, 365184, 342869, 316928, 285137, 273553, 250861, 221358, 195884, 179321, 171010, 162594, 152221, 148843, 143013, 135887, 125824, 121493, 115913, 113738, 105612, 99596, 91609, 83917, 75688, 69538, 62999, 58864, 54593, 48818, 44739, 41096, 39169, 36321, 34284, 32330, 31437, 30661, 31332, 30334, 23600, 21999, 20187, 19075, 16574, 15091, 14977, 14171, 13687, 13155, 12558, 11600, 10827, 10436, 9851, 9794, 8787, 7993, 6901, 6422, 5506, 4839, 4144, 3433, 2936, 2615),
     (346205, 340570, 342668, 328475, 319010, 312898, 308153, 296752, 289639, 290466, 296190, 303871, 309886, 317436, 315487, 316696, 325772, 331694, 345815, 354696, 354899, 351727, 354579, 341702, 336421, 321116, 292261, 261874, 242407, 229488, 208939, 184147, 162662, 147361, 140424, 134336, 126929, 125404, 122764, 116004, 105590, 100813, 95021, 90950, 85036, 79391, 72952, 66022, 59326, 52716, 46582, 42772, 38509, 34048, 30887, 28053, 26152, 23931, 22039, 20677, 19869, 19026, 18757, 18308, 14458, 13685, 12942, 12323, 11033, 10183, 10628, 10803, 10655, 10482, 10202, 10166, 9939, 10138, 10007, 10174, 9997, 9465, 9028, 8806, 8450, 7941, 7253, 6698, 6267, 5773),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 91, 412, 1319, 2984, 5816, 10053, 16045, 24240, 35066, 47828, 62384, 78916, 97822, 112738, 124414, 130658, 140789, 153951, 168560, 179996, 194471, 212006, 225209, 228886, 239690, 245974, 253459, 255455, 260715, 259980, 256481, 252222, 249467, 240268, 238465, 238167, 231361, 223832, 220459, 222512, 220099, 219301, 221322, 229783, 239336, 258360, 271151, 218063, 213461, 207617, 196227, 174615, 160855, 165410, 163070, 157379, 149698, 140570, 131785, 119936, 113751, 106989, 99294, 89097, 78413, 68174, 60592, 52189, 43375, 35469, 29648, 24575, 20863),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 74, 392, 1351, 3906, 7847, 12857, 19913, 29108, 42475, 58287, 74163, 90724, 108375, 125886, 141559, 148061, 152871, 159725, 171298, 183536, 196136, 210831, 228757, 238731, 239616, 250036, 251759, 259593, 261832, 264864, 264702, 264070, 258117, 253678, 245440, 241342, 239843, 232493, 226118, 221644, 223440, 219833, 219659, 221271, 227123, 232865, 250646, 261796, 210136, 201824, 193109, 181831, 159280, 145235, 145929, 140266, 133082, 124350, 114441, 104655, 93223, 85899, 78800, 72081, 62645, 53214, 44086, 38481, 32219, 26867, 21443, 16899, 13680, 11508),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 5, 17, 15, 31, 34, 38, 35, 45, 299, 295, 218, 247, 252, 254, 222, 307, 316, 385, 416, 463, 557, 670, 830, 889, 1025, 1149, 1356, 1488, 1835, 1929, 2130, 2362, 2494, 2884, 3160, 3487, 3916, 4196, 4619, 5032, 5709, 6347, 7288, 8139, 9344, 11002, 12809, 11504, 11918, 12927, 13642, 13298, 14015, 15751, 17445, 18591, 19682, 20969, 21629, 22549, 23619, 25288, 26293, 27038, 27039, 27070, 27750, 27244, 25905, 24357, 22561, 21794, 20595),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 8, 0, 8, 21, 34, 49, 84, 97, 368, 401, 414, 557, 654, 631, 689, 698, 858, 1031, 1120, 1263, 1614, 1882, 2137, 2516, 2923, 3132, 3741, 4259, 4930, 5320, 5948, 6548, 7463, 8309, 9142, 10321, 11167, 12062, 13317, 15238, 16706, 18236, 20336, 23407, 27024, 32502, 37334, 34454, 38080, 41811, 44490, 45247, 46830, 53616, 58798, 63224, 66841, 71086, 73654, 77334, 82062, 87314, 92207, 94603, 94113, 92753, 93174, 91812, 87757, 84255, 79723, 77536, 74173),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 11, 35, 137, 331, 803, 1580, 2361, 3632, 4866, 6849, 8754, 10422, 12316, 14152, 16911, 19788, 22822, 27329, 31547, 35711, 38932, 42956, 46466, 49983, 52885, 55178, 56549, 57632, 57770, 57427, 56348, 55593, 55554, 53266, 51084, 49342, 48555, 47067, 45789, 44988, 44624, 44238, 46267, 46203, 36964, 33866, 31701, 28770, 25174, 22702, 21934, 20638, 19051, 17073, 15381, 13736, 11690, 10368, 9350, 8375, 7063, 6006, 5044, 4030, 3420, 2612, 2006, 1709, 1264, 1018),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 11, 20, 68, 179, 480, 1077, 2094, 3581, 5151, 7047, 9590, 12434, 15039, 17257, 19098, 21324, 24453, 27813, 32316, 37281, 43597, 49647, 53559, 58888, 62375, 67219, 70956, 73547, 74904, 75994, 76224, 74979, 72064, 70330, 68944, 66527, 63073, 60899, 60968, 58756, 57647, 56301, 57246, 57068, 59027, 59187, 47549, 44425, 40976, 38077, 32904, 29431, 29491, 28020, 26086, 24069, 21742, 19498, 17400, 15738, 14451, 13107, 11568, 10171, 8530, 7273, 6488, 5372, 4499, 3691, 3259, 2657)]

  types = ['Males single', 'Females single',
           'Males married', 'Females married',
           'Males widowed', 'Females widowed',
           'Males divorced', 'Females divorced']

  pyramid_chart = pygal.Pyramid(human_readable=True, legend_at_bottom=True)
  pyramid_chart.title = 'England population by age in 2010 (source: ons.gov.uk)'
  pyramid_chart.x_labels = map(lambda x: str(x) if not x % 5 else '', range(90))
  for type, age in zip(types, ages):
      pyramid_chart.add(type, age)


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

Next: `Styles </styles>`_
