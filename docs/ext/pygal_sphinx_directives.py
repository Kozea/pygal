# -*- coding: utf-8 -*-
# This file is part of pygal_sphinx_directives
#
# Pygal sphinx integration
# Copyright © 2012-2016 Florian Mounier
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.


from traceback import format_exc, print_exc

import docutils.core
from docutils.parsers.rst import Directive

import pygal
from sphinx.directives.code import CodeBlock

# Patch default style

pygal.config.Config.style.value = pygal.style.RotateStyle(
    '#2980b9',
    background='#fcfcfc',
    plot_background='#ffffff',
    foreground='#707070',
    foreground_strong='#404040',
    foreground_subtle='#909090',
    opacity='.8',
    opacity_hover='.9',
    transition='400ms ease-in')


class PygalDirective(Directive):
    """Execute the given python file and puts its result in the document."""
    required_arguments = 0
    optional_arguments = 2
    final_argument_whitespace = True
    has_content = True

    def run(self):
        width, height = map(int, self.arguments[:2]) if len(
            self.arguments) >= 2 else (600, 400)
        if len(self.arguments) == 1:
            self.render_fix = bool(self.arguments[0])
        elif len(self.arguments) == 3:
            self.render_fix = bool(self.arguments[2])
        else:
            self.render_fix = False
        self.content = list(self.content)
        content = list(self.content)
        if self.render_fix:
            content[-1] = 'rv = ' + content[-1]
        code = '\n'.join(content)
        scope = {'pygal': pygal}
        try:
            exec(code, scope)
        except Exception:
            print(code)
            print_exc()
            return [docutils.nodes.system_message(
                'An exception as occured during code parsing:'
                ' \n %s' % format_exc(), type='ERROR', source='/',
                level=3)]
        if self.render_fix:
            rv = scope['rv']
        else:
            chart = None
            for key, value in scope.items():
                if isinstance(value, pygal.graph.graph.Graph):
                    chart = value
                    self.content.append(key + '.render()')
                    break
            if chart is None:
                return [docutils.nodes.system_message(
                    'No instance of graph found', level=3,
                    type='ERROR', source='/')]
            chart.config.width = width
            chart.config.height = height
            chart.explicit_size = True

        try:
            svg = '<embed src="%s" />' % chart.render_data_uri()
        except Exception:
            return [docutils.nodes.system_message(
                'An exception as occured during graph generation:'
                ' \n %s' % format_exc(), type='ERROR', source='/',
                level=3)]
        return [docutils.nodes.raw('', svg, format='html')]


class PygalWithCode(PygalDirective):

    def run(self):
        node_list = super(PygalWithCode, self).run()
        node_list.extend(CodeBlock(
            self.name,
            ['python'],
            self.options,
            self.content,
            self.lineno,
            self.content_offset,
            self.block_text,
            self.state,
            self.state_machine).run())

        return [docutils.nodes.compound('', *node_list)]


class PygalTable(Directive):
    """Execute the given python file and puts its result in the document."""
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):

        self.content = list(self.content)
        content = list(self.content)
        content[-1] = 'rv = ' + content[-1]
        code = '\n'.join(content)
        scope = {'pygal': pygal}
        try:
            exec(code, scope)
        except Exception:
            print_exc()
            return [docutils.nodes.system_message(
                'An exception as occured during code parsing:'
                ' \n %s' % format_exc(), type='ERROR', source='/',
                level=3)]
        rv = scope['rv']

        return [docutils.nodes.raw('', rv, format='html')]


class PygalTableWithCode(PygalTable):

    def run(self):
        node_list = super(PygalTableWithCode, self).run()
        node_list.extend(CodeBlock(
            self.name,
            ['python'],
            self.options,
            self.content,
            self.lineno,
            self.content_offset,
            self.block_text,
            self.state,
            self.state_machine).run())

        return [docutils.nodes.compound('', *node_list)]


def setup(app):
    app.add_directive('pygal', PygalDirective)
    app.add_directive('pygal-code', PygalWithCode)
    app.add_directive('pygal-table', PygalTable)
    app.add_directive('pygal-table-code', PygalTableWithCode)

    return {'version': '1.0.1'}
