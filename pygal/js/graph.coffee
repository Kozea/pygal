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


@svg_load = ->
    for element in _('.reactive-text')
        element.addEventListener('mouseover', ((e) ->
            ->
                add_class(e, 'active')
                add_class(document.getElementById(e.id.replace(/re/, '')), 'active')
        )(element), false)
        element.addEventListener('mouseout', ((e) ->
            ->
                rm_class(e, 'active')
                rm_class(document.getElementById(e.id.replace(/re/, '')), 'active')
        )(element), false)
    for element in _('.reactive')
        element.addEventListener('mouseover', ((e) ->
            ->
                add_class(e, 'active')
                add_class(document.getElementById('re' + e.id), 'active')
        )(element), false)
        element.addEventListener('mouseout', ((e) ->
            ->
                rm_class(e, 'active')
                rm_class(document.getElementById('re' + e.id), 'active')
        )(element), false)

    for element in _('.activate-serie')
       element.addEventListener('mouseover', ((e) ->
            ->
                num = e.id.replace('activate-serie-', '')
                for element in _('.serie-' + num + ' .reactive')
                    add_class(element, 'active')
                    add_class(document.getElementById('re' + element.id), 'active')
        )(element), false)
        element.addEventListener('mouseout', ((e) ->
            ->
                num = e.id.replace('activate-serie-', '')
                for element in _('.serie-' + num + ' .reactive')
                    rm_class(element, 'active')
                    rm_class(document.getElementById('re' + element.id), 'active')
        )(element), false)
