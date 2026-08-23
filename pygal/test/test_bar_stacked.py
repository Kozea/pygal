# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2026 Kozea
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
"""StackedBar chart related tests"""

import math

from pygal import StackedBar


def test_print_zeroes():
    """Test print_zeroes option for StackedBar"""
    game_scores = {
        'Boules':  {'Luc':  7, 'Frank':  8},
        '10pin':   {'Luc': 12, 'Frank':  0},
        'Curling': {'Luc':  0, 'Frank': 20},
    }
    for print_zeroes in (True, False):
        stacked = StackedBar(print_values=True, print_zeroes=print_zeroes)
        stacked.title = "Game Scores (StackedBar test)"
        zero_scores = 0
        game_types = 0
        player_count = None
        for game, players_scores in game_scores.items():
            if player_count is None:
                player_count = len(players_scores)
                stacked.x_labels = tuple(players_scores.keys())
            scores = players_scores.values()
            stacked.add(game, scores)
            zero_scores += sum(1 if score == 0 else 0 for score in scores)
            game_types += 1
        q = stacked.render_pyquery()
        zero_height_bars = 0
        for element in q(".bar>rect[height]"):
            if math.isclose(float(element.attrib['height']), 0.0):
                zero_height_bars += 1
        if print_zeroes:
            assert zero_height_bars == zero_scores
            expected_bars = len(game_scores) * len(game_scores['Boules'])
            assert len(q(".plot .series rect")) == expected_bars
        else:
            assert zero_height_bars == 0
            expected_bars = len(game_scores) * len(game_scores['Boules']) - zero_scores
            assert len(q(".plot .series rect")) == expected_bars
        assert len(q(".axis.x")) == 1
        assert len(q(".axis.y")) == 1
        assert len(q(".legend")) == game_types

