import cssutils

SVG = 'SVG 1.1' # http://www.w3.org/TR/SVG11/styling.html

macros = {
	'paint': 'none|currentColor|{color}',
	'unitidentifier': 'em|ex|px|pt|pc|cm|mm|in|%',
	'length': '{positivenum}({unitidentifier})?',
	'dasharray': '{positivenum}(\s*,\s*{positivenum})*',
	}
properties = {
	'stroke': '{paint}',
	'fill': '{paint}',
	'text-anchor': 'start|middle|end|inherit',
	'stroke-width': '{length}|inherit',
	'fill-opacity': '{num}|inherit',
	'stroke-dasharray': 'none|{dasharray}|inherit',
	}

cssutils.profile.addProfile(SVG, properties, macros)

cssutils.profile.defaultProfiles = [SVG, cssutils.profile.CSS_LEVEL_2]