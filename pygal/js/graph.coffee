_ = (x) -> document.querySelectorAll(x)

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

activate = (elements...) ->
    for element in elements
        add_class(element, 'active')

deactivate = (elements...) ->
    for element in elements
        rm_class(element, 'active')

reactive = (element) -> document.getElementById('re' + element.id)
active = (element) -> document.getElementById(element.id.replace(/re/, ''))

hover = (elts, over, out) ->
    for elt in elts
        elt.addEventListener('mouseover',
            ((elt) -> (-> over.call(elt)))(elt)
        , false)
        elt.addEventListener('mouseout',
            ((elt) -> (-> out.call(elt)))(elt)
        , false)

@svg_load = ->
    hover _('.reactive-text'), (-> activate(@, active(@))), (-> deactivate(@, active(@)))
    hover _('.reactive'), (-> activate(@, reactive(@))), (-> deactivate(@, reactive(@)))
    hover _('.activate-serie'), (
        ->
            num = this.id.replace('activate-serie-', '')
            for element in _('.serie-' + num + ' .reactive')
                activate(element, reactive(element))), (
        ->
            num = this.id.replace('activate-serie-', '')
            for element in _('.serie-' + num + ' .reactive')
                deactivate(element, reactive(element)))
