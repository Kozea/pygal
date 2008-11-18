Upgrade Notes
-------------

Upgrading from 1.x to 2.0

I suggest removing SVG 1.0 from the python installation.  This involves removing the SVG directory (or svg_chart*) from site-packages.

Change import statements to import from the new namespace.

from SVG import Bar
Bar.VerticalBar(...)
becomes
from svg.charts.bar import VerticalBar
VerticalBar(...)

--- Still to do ---

-  Implement javascript-based animation (See JellyGraph for a Silverlight example of what simple animation can do for a charting library).
