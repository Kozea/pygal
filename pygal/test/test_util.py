# -*- coding: utf-8 -*-
from pygal.util import round_to_int, round_to_float, _swap_curly, template
from pytest import raises


def test_round_to_int():
    assert round_to_int(154231, 1000) == 154000
    assert round_to_int(154231, 10) == 154230
    assert round_to_int(154231, 100000) == 200000
    assert round_to_int(154231, 50000) == 150000
    assert round_to_int(154231, 500) == 154000
    assert round_to_int(154231, 200) == 154200
    assert round_to_int(154361, 200) == 154400


def test_round_to_float():
    assert round_to_float(12.01934, .01) == 12.02
    assert round_to_float(12.01134, .01) == 12.01
    assert round_to_float(12.1934, .1) == 12.2
    assert round_to_float(12.1134, .1) == 12.1
    assert round_to_float(12.1134, .001) == 12.113
    assert round_to_float(12.1134, .00001) == 12.1134
    assert round_to_float(12.1934, .5) == 12.0
    assert round_to_float(12.2934, .5) == 12.5


def test_swap_curly():
    for str in (
            'foo',
            u'foo foo foo bar',
            'foo béè b¡ð/ĳə˘©þß®~¯æ',
            u'foo béè b¡ð/ĳə˘©þß®~¯æ'):
        assert _swap_curly(str) == str
    assert _swap_curly('foo{bar}baz') == 'foo{{bar}}baz'
    assert _swap_curly('foo{{bar}}baz') == 'foo{bar}baz'
    assert _swap_curly('{foo}{{bar}}{baz}') == '{{foo}}{bar}{{baz}}'
    assert _swap_curly('{foo}{{{bar}}}{baz}') == '{{foo}}{{{bar}}}{{baz}}'
    assert _swap_curly('foo{ bar }baz') == 'foo{{ bar }}baz'
    assert _swap_curly('foo{ bar}baz') == 'foo{{ bar}}baz'
    assert _swap_curly('foo{bar }baz') == 'foo{{bar }}baz'
    assert _swap_curly('foo{{ bar }}baz') == 'foo{bar}baz'
    assert _swap_curly('foo{{bar }}baz') == 'foo{bar}baz'
    assert _swap_curly('foo{{ bar}}baz') == 'foo{bar}baz'


def test_format():
    assert template('foo {{ baz }}', baz='bar') == 'foo bar'
    with raises(KeyError):
        assert template('foo {{ baz }}') == 'foo baz'

    class Object(object):
        pass
    obj = Object()
    obj.a = 1
    obj.b = True
    obj.c = '3'
    assert template('foo {{ o.a }} {{o.b}}-{{o.c}}',
               o=obj) == 'foo 1 True-3'
