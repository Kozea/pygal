_ = (x) -> document.querySelectorAll(x)
__ = (x) -> document.getElementById(x)
padding = 5
tooltip_timeout = 0
tooltip_font_size = @config.tooltip_font_size
anim_steps = @config.animation_steps

class Queue
    constructor: (@delay) ->
        @queue = []
        @running = false

    add: (f, args...) ->
        @queue.push f: f, a: args
        if (!@running)
            @running = true
            @_back()

    _run: (f) ->
        if(!f)
            @running = false
        else
            setTimeout (=>
                f.f f.a...
                @_back()
            ), @delay

    _back: ->
        @_run @queue.shift()

    clear: ->
        if @running
            @queue = []
            @running = false

tooltip_anim_Q = new Queue 1

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

width = (e) -> (e.getBBox() and e.getBBox().width) or e.offsetWidth
height = (e) -> (e.getBBox() and e.getBBox().height) or e.offsetHeight

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
    tooltip_anim_Q.clear()
    clearTimeout(tooltip_timeout)
    _tooltip = __('tooltip')
    _tooltip.setAttribute('display', 'inline')
    _text = _tooltip.getElementsByTagName('text')[0]
    _rect = _tooltip.getElementsByTagName('rect')[0]
    value = elt.nextElementSibling
    _text.textContent = value.textContent
    w = width(_text) + 2 * padding
    h = height(_text) + 2 * padding
    _rect.setAttribute('width', w)
    _rect.setAttribute('height', h)
    _text.setAttribute('x', padding)
    _text.setAttribute('y', padding + tooltip_font_size)
    x_elt = value.nextElementSibling
    y_elt = x_elt.nextElementSibling
    x = parseInt(x_elt.textContent)
    if has_class(x_elt, 'centered')
        x -= w / 2
    else if has_class(x_elt, 'left')
        x -= w

    y = parseInt(y_elt.textContent)
    if has_class(y_elt, 'centered')
        y -= h / 2
    else if has_class(y_elt, 'top')
        y -= h

    [current_x, current_y] = (parseInt(s) for s in _tooltip.getAttribute('transform').replace('translate(', '').replace(')', '').split ' ')
    return if current_x == x and current_y == y
    if anim_steps
        x_step = (x - current_x) / (anim_steps + 1)
        y_step = (y - current_y) / (anim_steps + 1)
        anim_x = current_x
        anim_y = current_y
        for i in [0..anim_steps]
            anim_x += x_step
            anim_y += y_step
            tooltip_anim_Q.add ((_x, _y) ->
                _tooltip.setAttribute('transform', "translate(#{_x} #{_y})")), anim_x, anim_y
        tooltip_anim_Q.add -> _tooltip.setAttribute('transform', "translate(#{x} #{y})")
    else
        _tooltip.setAttribute('transform', "translate(#{x} #{y})")

untooltip = ->
    tooltip_timeout = setTimeout (->
        __('tooltip').setAttribute('display', 'none')), 1000

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
