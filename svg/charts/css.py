import cssutils

SVG = 'SVG 1.1' # http://www.w3.org/TR/SVG11/styling.html

macros = {
	'paint': 'none|currentColor|{color}',
	'unitidentifier': 'em|ex|px|pt|pc|cm|mm|in|%',
	'length': '{positivenum}({unitidentifier})?',
	'dasharray': '{positivenum}(\s*,\s*{positivenum})*',
	# a number greater-than or equal to one
	'number-ge-one': '{[1-9][0-9]*(\.[0-9]+)?',
	}
properties = {
	# Clipping, Masking, and Compositing
	'clip-path': '{uri}|none|inherit',
	'clip-rule': 'nonzero|evenodd|inherit',
	'mask': '{uri}|none|inherit',
	'opacity': '{num}|inherit',

	# Filter Effects
	'enable-background': 'accumulate|new(\s+{num}){0,4}|inherit',
	'filter': '{uri}|none|inherit',
	'flood-color': 'currentColor|{color}|inherit',
	'flood-opacity': '{num}|inherit',
	'lighting-color': 'currentColor|{color}|inherit',

	# Gradient Properties
	'stop-color': 'currentColor|{color}|inherit',
	'stop-opacity': '{num}|inherit',

	# Interactivity Properties
	'pointer-events': 'visiblePainted|visibleFill|visibleStroke|visible|painted|fill|stroke|all|none|inherit',

	# Color and Pointing Properties
	'color-interpolation': 'auto|sRGB|linearRGB|inherit',
	'color-interpolation-filters': 'auto|sRGB|linearRGB|inherit',
	'color-rendering': 'auto|optimizeSpeed|optimizeQuality|inherit',
	'shape-rendering': 'auto|optimizeSpeed|crispEdges|geometricPrecision|inherit',
	'text-rendering': 'auto|optimizeSpeed|optimizeLegibility|geometricPrecision|inherit',
	'fill': '{paint}',
	'fill-opacity': '{num}|inherit',
	'fill-rule': 'nonzero|evenodd|inherit',
	'image-rendering': 'auto|optimizeSpeed|optimizeQuality|inherit',
	'marker': 'none|inherit|{uri}',
	'marker-end': 'none|inherit|{uri}',
	'marker-mid': 'none|inherit|{uri}',
	'marker-start': 'none|inherit|{uri}',
	'shape-rendering': 'auto|optimizeSpeed|crispEdges|geometricPrecision|inherit',
	'stroke': '{paint}',
	'stroke-dasharray': 'none|{dasharray}|inherit',
	'stroke-dashoffset': '{length}|inherit',
	'stroke-linecap': 'butt|round|square|inherit',
	'stroke-linejoin': 'miter|round|bevel|inherit',
	'stroke-miterlimit': '{number-ge-one}|inherit',
	'stroke-opacity': '{num}|inherit',
	'stroke-width': '{length}|inherit',
	'text-rendering': 'auto|optimizeSpeed|optimizeLegibility|geometricPrecision|inherit',

	# Text Properties
	'alignment-baseline': 'auto|baseline|before-edge|text-before-edge|middle|central|after-edge|text-after-edge|ideographic|alphabetic|hanging|mathematical|inherit',
	'baseline-shift': 'baseline|sub|super|{percentage}|{length}|inherit',
	'dominant-baseline': 'auto|use-script|no-change|reset-size|ideographic|alphabetic|hanging||mathematical|central|middle|text-after-edge|text-before-edge|inherit',
	'glyph-orientation-horizontal': '{angle}|inherit',
	'glyph-orientation-vertical': 'auto|{angle}|inherit',
	'kerning': 'auto|{length}|inherit',
	'text-anchor': 'start|middle|end|inherit',
	'writing-mode': 'lr-tb|rl-tb|tb-rl|lr|rl|tb|inherit',
	}

cssutils.profile.addProfile(SVG, properties, macros)

cssutils.profile.defaultProfiles = [SVG, cssutils.profile.CSS_LEVEL_2]