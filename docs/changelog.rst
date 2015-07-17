=========
Changelog
=========

2.0.0 UNRELEASED
================
* Rework the ghost mechanism to come back to a more object oriented behavior, storing all state in a state object which is created on every render. (#161)
* Refactor maps
* Add world continents
* Add swiss cantons map (thanks sergedroz)
* Add inverse_y_axis options to reverse graph (#24)
* Fix DateTimeLine time data loss (#193)
* Fix no data for graphs with only zeroes (#148)
* Support value formatter for pie graphs (#218) (thanks never-eat-yellow-snow)
* Add new Box plot modes and outliers and set extremes as default (#226 #121 #149) (thanks djezar)
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

1.7.0
=====
* Remove DateY and replace it by real XY datetime, date, time and timedelta support. (#188)
* Introduce new XY configuration options: `xrange`, `x_value_formatter`.
* Add show_x_labels option to remove them and the x axis.
* Set print_values to False by default.
* Fix secondary serie text values when None in data. (#192)

1.6.2
=====
* Add margin_top, margin_right, margin_bottom, margin_left options which defaults to margin. (thanks djt)
* Update django mime parameter from mimetype to content_type. (thanks kswiat)
* Allow a color and a style parameter to value metadata.

1.6.1
=====
* Fix Decimal incompatibility

1.6.0
=====
* Adds config option missing_value_fill_truncation. (thanks sirlark)
* Avoid HTTP 301 Moved Permanently (thanks jean)
* Add a Django response method (thanks inlanger)
* Fix setup.py (#170)
* Fix format error on list like in table
* Add legend_at_bottom_columns option to specify number of columns in legend when at bottom. (#157)
* Fix secondary interpolation (#165)
* Adds an extra class (axis) to horizontal guides if the label is "0" (#147) (thanks sirlark)
* Add line stroke customization parameters to style.py (#154) (thanks blakev)

1.5.1
=====
* Add `stack_from_top` option to reverse stack graph data order
* Minor fix for empty logarithmic chart
* Reorders axes in SVG output. Fix #145 (thanks sirlark)

1.5.0
=====
* Add per serie configuration
* Add half pie (thanks philt2001)
* Make lxml an optionnal dependency (huge speed boost in pypy)
* Add render_table (WIP)
* Support colors in rgb / rgba for parametric styles

1.4.6
=====
* Add support for \n separated multiline titles (thanks sirlark)
* New show_only_major_dots option (thanks Le-Stagiaire)
* Remove 16 colors limitation
* Fix 0 in range (thanks elpaso)

1.4.5
=====
* Fix y_labels map iterator exhaustion in python 3

1.4.4
=====
* Fix division by zero in spark text (thanks laserpony)
* Fix config metaclass problem in python 3
* Fix --version in pygal_gen

1.4.3
=====
* Allow arbitrary number of x-labels on line plot (thanks nsmgr8)

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
