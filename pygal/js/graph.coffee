_ = (x) -> document.querySelectorAll(x)
__ = (x) -> document.getElementById(x)
padding = 5
tooltip_timeout = 0
tooltip_font_size = parseInt("{{ font_sizes.tooltip }}")

has_class = (e, class_name) ->
    return if not e
    cn = e.getAttribute('class').split(' ')
    for cls, i in cn
        if cls == class_name
            return true
    false

add_class = (e, class_name) ->
    return if not e
    cn = e.getAttribute('class').split(' ')
    if not has_class(e, class_name)
        cn.push(class_name)
    e.setAttribute('class', cn.join(' '))

rm_class = (e, class_name) ->
    return if not e
    cn = e.getAttribute('class').split(' ')
    for cls, i in cn
        if cls == class_name
            cn.splice(i, 1)
    e.setAttribute('class', cn.join(' '))

svg = (tag) -> document.createElementNS('http://www.w3.org/2000/svg', tag)

activate = (elements...) ->
    for element in elements
        add_class(element, 'active')

deactivate = (elements...) ->
    for element in elements
        rm_class(element, 'active')

Function.prototype.bind = (scope) ->
    _fun = @
    -> _fun.apply(scope, arguments)

hover = (elts, over, out) ->
    for elt in elts
        elt.addEventListener('mouseover', over.bind(elt) , false)
        elt.addEventListener('mouseout', out.bind(elt) , false)

tooltip = (elt) ->
    clearTimeout(tooltip_timeout)
    _tooltip = __('tooltip')
    _text = _tooltip.getElementsByTagName('text')[0]
    _rect = _tooltip.getElementsByTagName('rect')[0]
    value = elt.nextElementSibling
    _text.textContent = value.textContent
    w = _text.offsetWidth + 2 * padding
    h = _text.offsetHeight + 2 * padding
    _rect.setAttribute('width', w)
    _rect.setAttribute('height', h)
    _text.setAttribute('x', padding)
    _text.setAttribute('y', padding + tooltip_font_size)
    x_elt = value.nextElementSibling
    y_elt = x_elt.nextElementSibling
    x = x_elt.textContent
    if has_class(x_elt, 'centered')
        x -= w / 2

    y = y_elt.textContent
    if has_class(y_elt, 'centered')
        y -= h / 2
    _tooltip.setAttribute('transform', "translate(#{x} #{y})")

untooltip = ->
    tooltip_timeout = setTimeout (->
        __('tooltip').setAttribute('transform', 'translate(-100000, -100000)')), 1000

@svg_load = ->
    for text in _('.text-overlay .series')
        text.setAttribute('display', 'none')
    hover _('.reactive'), (-> activate(@)), (-> deactivate(@))
    hover _('.activate-serie'), (
        ->
            num = this.id.replace('activate-serie-', '')
            for element in _('.text-overlay .serie-' + num)
                element.setAttribute('display', 'inline')
            for element in _('.serie-' + num + ' .reactive')
                activate(element)), (
        ->
            num = this.id.replace('activate-serie-', '')
            for element in _('.text-overlay .serie-' + num)
                element.setAttribute('display', 'none')
            for element in _('.serie-' + num + ' .reactive')
                deactivate(element))
    hover _('.tooltip-trigger'), (-> tooltip(@)), (-> untooltip())
