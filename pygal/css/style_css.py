data="""\
/*
 * This file is part of pygal
 *
 * A python svg graph plotting library
 * Copyright © 2012 Kozea

 * This library is free software: you can redistribute it and/or modify it under
 * the terms of the GNU Lesser General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option) any
 * later version.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with pygal. If not, see <http://www.gnu.org/licenses/>.
*/

/*
 * Styles from config
 */

{{ id }}{
  background-color: {{ style.background }};
}

{{ id }}path,
{{ id }}line,
{{ id }}rect,
{{ id }}circle {
  -webkit-transition: {{ style.transition }};
  -moz-transition: {{ style.transition }};
  transition: {{ style.transition }};
}

{{ id }}.graph > .background {
  fill: {{ style.background }};
}

{{ id }}.plot > .background {
  fill: {{ style.plot_background }};
}

{{ id }}.graph {
  fill: {{ style.foreground }};
}

{{ id }}text.no_data {
  fill: {{ style.foreground_light }};
}

{{ id }}.title {
  fill: {{ style.foreground_light }};
}

{{ id }}.legends .legend text {
  fill: {{ style.foreground }};
}

{{ id }}.legends .legend:hover text {
  fill: {{ style.foreground_light }};
}

{{ id }}.axis .line {
  stroke: {{ style.foreground_light }};
}

{{ id }}.axis .guide.line {
  stroke: {{ style.foreground_dark }};
}

{{ id }}.axis .major.line {
  stroke: {{ style.foreground }};
}

{{ id }}.axis text.major {
  stroke: {{ style.foreground_light }};
  fill: {{ style.foreground_light }};
}

{{ id }}.axis.y .guides:hover .guide.line,
{{ id }}.line-graph .axis.x .guides:hover .guide.line,
{{ id }}.stackedline-graph .axis.x .guides:hover .guide.line,
{{ id }}.xy-graph .axis.x .guides:hover .guide.line {
  stroke: {{ style.foreground_light }};
}

{{ id }}.axis .guides:hover text {
  fill: {{ style.foreground_light }};
}

{{ id }}.reactive {
  fill-opacity: {{ style.opacity }};
}

{{ id }}.reactive.active,
{{ id }}.active .reactive {
  fill-opacity:  {{ style.opacity_hover }};
}

{{ id }}.series {
  stroke-width: {{ style.stroke_width }};
  stroke-linejoin: {{ style.stroke_style }};
  stroke-linecap: {{ style.stroke_style }};
  stroke-dasharray: {{ style.stroke_dasharray }};
}

{{ id }}.series text {
  fill: {{ style.foreground_light }};
}

{{ id }}.tooltip rect {
  fill: {{ style.plot_background }};
  stroke: {{ style.foreground_light }};
}

{{ id }}.tooltip text {
  fill: {{ style.foreground_light }};
}

{{ id }}.map-element {
  fill: {{ style.foreground }};
  stroke: {{ style.foreground_dark }} !important;
  opacity: .9;
  stroke-width: 3;
  -webkit-transition: 250ms;
  -moz-transition: 250ms;
  -o-transition: 250ms;
  transition: 250ms;
}

{{ id }}.map-element:hover {
  opacity: 1;
  stroke-width: 10;
}

{{ colors }}


"""