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

{{ id }}text.no_data {
  text-anchor: middle;
}

{{ id }}.guide.line {
  fill-opacity: 0;
}

{{ id }}.centered {
  text-anchor: middle;
}

{{ id }}.title {
  text-anchor: middle;
}

{{ id }}.legends .legend text {
  fill-opacity: 1;
}

{{ id }}.axis.x text {
  text-anchor: middle;
}

{{ id }}.axis.x:not(.web) text[transform] {
  text-anchor: start;
}

{{ id }}.axis.y text {
  text-anchor: end;
}
{{ id }}.axis.y2 text {
  text-anchor: start;
}

{{ id }}.axis.y .logarithmic text:not(.major) ,
{{ id }}.axis.y2 .logarithmic text:not(.major) {
  font-size: 50%;
}

{{ id }}.axis .guide.line {
  stroke-dasharray: 4,4;
}

{{ id }}.axis .major.guide.line {
  stroke-dasharray: 6,6;
}
{{ id }}.axis text.major {
  stroke-width: 0.5px;
}

{{ id }}.horizontal .axis.y .guide.line,
{{ id }}.horizontal .axis.y2 .guide.line,
{{ id }}.vertical .axis.x .guide.line {
  opacity: 0;
}

{{ id }}.horizontal .axis.always_show .guide.line,
{{ id }}.vertical .axis.always_show .guide.line {
  opacity: 1 !important;
}

{{ id }}.axis.y .guides:hover .guide.line,
{{ id }}.axis.y2 .guides:hover .guide.line,
{{ id }}.axis.x .guides:hover .guide.line {
  opacity: 1;
}

{{ id }}.axis .guides:hover text {
  opacity: 1;
}

{{ id }}.nofill {
  fill: none;
}

{{ id }}.subtle-fill {
  fill-opacity: .2;
}

{{ id }}.dot {
  stroke-width: 1px;
  fill-opacity: 1;
}

{{ id }}.dot.active {
  stroke-width: 5px;
}

{{ id }}.series text {
  stroke: none;
}

{{ id }}.series text.active {
  opacity: 1;
}

{{ id }}.tooltip rect {
  fill-opacity: 0.8;
}

{{ id }}.tooltip text {
  fill-opacity: 1;
}

{{ id }}.tooltip text tspan.label {
  fill-opacity: .8;
}
"""