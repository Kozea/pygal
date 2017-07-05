=========
Changelog
=========

2.4.0
=====

* Generalized fix solidgauge squares algorithm (thanks @Necrote #385)
* Fix secondary series 'stroke_style' property (thanks @Yuliang-Lee #359)
* Fix wrong label colors when there are more series than colors (thanks @Brandhor #350)
* Show y guides in horizontal chart (thanks @yossisal #349)
* Fix nomenclature of Taiwan (thanks @pierrrrrrre #344)
* Better None values handling in logarithmic charts (thanks @ShuaiQin #343)


2.3.1
=====

_This is a micro release and I have very little time on my hands right now sorry_

* Fix crash with no values when the print_values_position param is set (thanks @cristen)


2.3.0
=====

* New call API: `chart = Line(fill=True); chart.add('title', [1, 3, 12]); chart.render()` can now be replaced with `Line(fill=True)(1, 3, 12, title='title').render()`
* Drop python 2.6 support


2.2.3
=====

* Fix bar static value positioning (#315)
* Add stroke_opacity style (#321)
* Remove useless js in sparklines. (#312)


2.2.2
=====

* Add `classes` option.
* Handle ellipsis in list type configs to auto-extend parent. (Viva python3)


2.2.0
=====

* Support interruptions in line charts (thanks @piotrmaslanka #300)
* Fix confidence interval reactiveness (thanks @chartique #296)
* Add horizontal line charts (thanks @chartique #301)
* There is now a `formatter` config option to format values as specified. The formatter callable may or may not take `chart`, `serie` and `index` as argument. The default value formatting is now chart dependent and is value_formatter for most graph but could be a combination of value_formatter and x_value_formatter for dual charts.
* The `human_readable` option has been removed. Now you have to use the pygal.formatters.human_readable formatter (value_formatter=human_readable instead of human_readable=True)
* New chart type: SolidGauge (thanks @chartique #295)
* Fix range option for some Charts (#297 #298)
* Fix timezones for DateTimeLine for python 2 (#306, #302)
* Set default uri protocol to https (should fix a lot of "no tooltips" bugs).

2.1.1
=====

* Import scipy as a last resort in stats.py (should workaround bugs like #294 if scipy is installed but not used)


2.1.0
=====

* Bar print value positioning with `print_values_position`. Can be `top`, `center` or `bottom` (thanks @chartique #291) `ci doc <documentation/configuration/value.html#confidence-intervals>`_
* Confidence intervals (thanks @chartique #292) `data doc <documentation/configuration/data.html#print-values-position>`_


2.0.12
======

* Use custom xml_declaration avoiding conflict with processing instructions


2.0.11
======

* lxml 3.5 compatibility (#282)


2.0.10
======

* Fix transposable_node in case all attributes are not there. (thanks @yobuntu).


2.0.9
=====

* Add `dynamic_print_values` to show print_values on legend hover. (#279)
* Fix unparse_color for python 3.5+ compatibility (thanks @felixonmars, @sjourdois)
* Process major labels as labels. (#263)
* Fix labels rotation > 180 (#257)
* Fix secondary axis
* Don't forget secondary series in table rendering (#260)
* Add `defs` config option to allow adding gradients and patterns.

2.0.8
=====

* Fix value overwrite in map. (#275)


2.0.7
=====

* Fixing to checks breaking rendering of DateTimeLine and TimeDeltaLine (#264) (thanks @mmrose)
* Fix `render_in_browser`. (#266) (#268) (thanks @waixwong)


2.0.6
=====

* Avoid x label formatting when label is a string


2.0.5
=====

* Fix x label formatting


2.0.4
=====

* Fix map coloration


2.0.3
=====

* Fix label adaptation. (#256)
* Fix wrong radar truncation. (#255)


2.0.2
=====

* Fix view box differently to avoid getting a null height on huge numbers. (#254)
* Fix broken font_family default
* Fix non namespaced svg (without embed) javascript by adding uuid in config object. (config is in window.pygal now).


2.0.1
=====

* Fix the missing title on x_labels with labels.
* Auto cast to str x labels in non dual charts (#178)
* Add ``print_labels`` option to print label too. (#197)
* Add ``value_label_font_family`` and ``value_label_font_size`` style options for ``print_labels``.
* Default ``print_zeroes`` to True
* (Re)Add xlink in desc to show on tooltip
* Activate element on tooltip hovering. (#106)
* Fix radar axis behaviour (#247)
* Add tooltip support in metadata to add a title (#249).
* Take config class options in account too.


2.0.0
=====

* Rework the ghost mechanism to come back to a more object oriented behavior, storing all state in a state object which is created on every render. (#161)
* Refactor maps
* Add world continents
* Add swiss cantons map (thanks @sergedroz)
* Add inverse_y_axis options to reverse graph (#24)
* Fix DateTimeLine time data loss (#193)
* Fix no data for graphs with only zeroes (#148)
* Support value formatter for pie graphs (#218) (thanks @never-eat-yellow-snow)
* Add new Box plot modes and outliers and set extremes as default (#226 #121 #149) (thanks @djezar)
* Add secondary_range option to set range for secondary values. (#203)
* Maps are now plugins, they are removed from pygal core and moved to packages (pygal_maps_world, pygal_maps_fr, pygal_maps_ch, ...) (#225)
* Dot now supports negative values
* Fix dot with log scale (#201)
* Fix y_labels behaviour for lines
* Fix x_labels and y_labels behaviour for xy like
* Improve gauge a bit
* Finally allow call chains on add
* Transform min_scale and max_scale as options
* mode option has been renamed to a less generic name: box_mode
* fix stack_from_top for stacked lines
* Add flake8 test to py.test in tox
* Remove stroke style in style and set it as a global / serie configuration.
* Fix None values in tables
* Fix timezones in DateTimeLine
* Rename in Style foreground_light as foreground_strong
* Rename in Style foreground_dark as foreground_subtle
* Add a ``render_data_uri`` method (#237)
* Move ``font_size`` config to style
* Add ``font_family`` for various elements in style
* Add ``googlefont:font`` support for style fonts
* Add ``tooltip_fancy_mode`` to revert to old tooltips
* Add auto ``print_value`` color + a configurable ``value_colors`` list in style
* Add ``guide_stroke_dasharray`` and ``guide_stroke_dasharray`` in style to customize guides (#242) (thanks @cbergmiller)
* Refactor label processing in a ``_compute_x_labels`` and ``_compute_y_labels`` method. Handle both string and numbers for all charts. Create a ``Dual`` base chart for dual axis charts.  (#236)
* Better js integration in maps. Use the normal tooltip.


1.7.0
=====

* Remove DateY and replace it by real XY datetime, date, time and timedelta support. (#188)
* Introduce new XY configuration options: `xrange`, `x_value_formatter`.
* Add show_x_labels option to remove them and the x axis.
* Set print_values to False by default.
* Fix secondary serie text values when None in data. (#192)

1.6.2
=====

* Add margin_top, margin_right, margin_bottom, margin_left options which defaults to margin. (thanks @djt)
* Update django mime parameter from mimetype to content_type. (thanks @kswiat)
* Allow a color and a style parameter to value metadata.

1.6.1
=====

* Fix Decimal incompatibility

1.6.0
=====

* Adds config option missing_value_fill_truncation. (thanks @sirlark)
* Avoid HTTP 301 Moved Permanently (thanks @jean)
* Add a Django response method (thanks @inlanger)
* Fix setup.py (#170)
* Fix format error on list like in table
* Add legend_at_bottom_columns option to specify number of columns in legend when at bottom. (#157)
* Fix secondary interpolation (#165)
* Adds an extra class (axis) to horizontal guides if the label is "0" (#147) (thanks @sirlark)
* Add line stroke customization parameters to style.py (#154) (thanks @blakev)

1.5.1
=====

* Add `stack_from_top` option to reverse stack graph data order
* Minor fix for empty logarithmic chart
* Reorders axes in SVG output. Fix #145 (thanks @sirlark)

1.5.0
=====

* Add per serie configuration
* Add half pie (thanks @philt2001)
* Make lxml an optionnal dependency (huge speed boost in pypy)
* Add render_table (WIP)
* Support colors in rgb / rgba for parametric styles

1.4.6
=====

* Add support for \n separated multiline titles (thanks @sirlark)
* New show_only_major_dots option (thanks @Le-Stagiaire)
* Remove 16 colors limitation
* Fix 0 in range (thanks @elpaso)

1.4.5
=====

* Fix y_labels map iterator exhaustion in python 3

1.4.4
=====

* Fix division by zero in spark text (thanks @laserpony)
* Fix config metaclass problem in python 3
* Fix --version in pygal_gen

1.4.3
=====

* Allow arbitrary number of x-labels on line plot (thanks @nsmgr8)

1.4.2
=====

* Fix broken tests

1.4.1
=====

* Fix value formatting in maps

1.4.0
=====

* Finally a changelog !
* Hopefully fix weird major scale algorithm
* Add options to customize major labels (y_labels_major, y_labels_major_every, y_labels_major_count)
* Css can now be inline with the "inline:" prefix
* Visited links bug fixed
* Add french maps by department and region (This will be externalized in an extension later)

1.3.x
=====

* Whisker Box Plot
* Python 3 fix
* DateY X axis formatting (x_label_format)
