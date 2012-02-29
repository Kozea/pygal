_ = (x) -> document.querySelectorAll(x)
__ = (x) -> document.getElementById(x)
padding = 5
tooltip_timeout = 0
tooltip_font_size = parseInt("{{ font_sizes.tooltip }}")


add_class = (e, class_name) ->
    return if not e
    cn = e.getAttribute('class').split(' ')
    if class_name not in cn
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
    ->
        _fun.apply(scope, arguments)

reactive = (element) -> document.getElementById('re' + element.id)
active = (element) -> document.getElementById(element.id.replace(/re/, ''))

hover = (elts, over, out) ->
    for elt in elts
        elt.addEventListener('mouseover', over.bind(elt) , false)
        elt.addEventListener('mouseout', out.bind(elt) , false)

tooltip = (elt) ->
    clearTimeout(tooltip_timeout)
    _tooltip = __('tooltip')
    _text = _tooltip.getElementsByTagName('text')[0]
    _rect = _tooltip.getElementsByTagName('rect')[0]
    _text.textContent = elt.nextElementSibling.textContent
    w = _text.offsetWidth + 2 * padding
    h = _text.offsetHeight + 2 * padding
    _rect.setAttribute('width', w)
    _rect.setAttribute('height', h)
    _text.setAttribute('x', padding)
    _text.setAttribute('y', padding + tooltip_font_size)
    x = elt.getAttribute('cx') || elt.getAttribute('x')
    y = elt.getAttribute('cy') || elt.getAttribute('y')
    if x - w  > 0
        x -= w
    if y - h > 0
        y -= h
    _tooltip.setAttribute('transform', "translate(#{x} #{y})")

untooltip = ->
    tooltip_timeout = setTimeout (->
        __('tooltip').setAttribute('transform', 'translate(-100000, -100000)')), 1000

@svg_load = ->
    for text in _('.text-overlay .series')
        text.setAttribute('display', 'none')
    hover _('.reactive-text'), (-> activate(@, active(@))), (-> deactivate(@, active(@)))
    hover _('.reactive'), (-> activate(@, reactive(@))), (-> deactivate(@, reactive(@)))
    hover _('.activate-serie'), (
        ->
            num = this.id.replace('activate-serie-', '')
            _('.text-overlay .serie-' + num)[0].setAttribute('display', 'inline')
            for element in _('.serie-' + num + ' .reactive')
                activate(element, reactive(element))), (
        ->
            num = this.id.replace('activate-serie-', '')
            _('.text-overlay .serie-' + num)[0].setAttribute('display', 'none')
            for element in _('.serie-' + num + ' .reactive')
                deactivate(element, reactive(element)))
    hover _('.tooltip-trigger'), (-> tooltip(@)), (-> untooltip())
