import cssutils

SVG = 'SVG 1.1' # http://www.w3.org/TR/SVG11/styling.html

macros = {
	'paint': 'none|currentColor|{color}',
	# spec actually says length, but our length macro requires units, so use positivenum
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