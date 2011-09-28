# -*- coding: utf-8 -*-
import math

pi = math.pi


def cos(angle):
    return math.cos(angle * pi / 180)


def sin(angle):
    return math.sin(angle * pi / 180)


def calculate_right_margin(graph):
    """
    Calculate the margin in pixels to the right of the plot area,
    setting border_right.
    """
    br = 7
    if graph.key and graph.key_position == 'right':
        max_key_len = max(map(len, graph.keys()))
        br += max_key_len * graph.key_font_size * 0.6
        br += graph.key_box_size
        br += 10  # Some padding around the box
    return br


def calculate_top_margin(graph):
    """
    Calculate the margin in pixels above the plot area, setting
    border_top.
    """
    bt = 10
    if graph.show_graph_title:
        bt += graph.title_font_size
    if graph.show_graph_subtitle:
        bt += graph.subtitle_font_size
    return bt


def calculate_bottom_margin(graph):
    """
    Calculate the margin in pixels below the plot area, setting
    border_bottom.
    """
    bb = 7
    if graph.key and graph.key_position == 'bottom':
        bb += len(graph.data) * (graph.font_size + 5)
        bb += 10
    if graph.show_x_labels:
        max_x_label_height_px = graph.x_label_font_size
        if graph.x_label_rotation:
            label_lengths = map(len, graph.get_x_labels())
            max_x_label_len = reduce(max, label_lengths)
            max_x_label_height_px *= max_x_label_len * 0.6
            max_x_label_height_px *= sin(graph.x_label_rotation)
        bb += max_x_label_height_px
        if graph.stagger_x_labels:
            bb += max_x_label_height_px + 10
    if graph.show_x_title:
        bb += graph.x_title_font_size + 5
    return bb


def calculate_left_margin(graph):
    """
    Calculates the margin to the left of the plot area, setting
    border_left.
    """
    bl = 7
    # Check for Y labels
    if graph.rotate_y_labels:
        max_y_label_height_px = graph.y_label_font_size
    else:
        label_lengths = map(len, graph.get_y_labels())
        max_y_label_len = max(label_lengths)
        max_y_label_height_px = (0.6 * max_y_label_len *
                                 graph.y_label_font_size)
    if graph.show_y_labels:
        bl += max_y_label_height_px
    if graph.stagger_y_labels:
        bl += max_y_label_height_px + 10
    if graph.show_y_title:
        bl += graph.y_title_font_size + 5
    if graph.x_label_rotation:
        label_lengths = map(len, graph.get_x_labels())
        max_x_label_len = reduce(max, label_lengths)
        max_x_label_height_px = graph.x_label_font_size
        max_x_label_height_px *= max_x_label_len * 0.6
        bl += max_x_label_height_px * cos(graph.x_label_rotation)
    return bl


def calculate_offsets_bottom(graph):
    x_offset = graph.border_left + 20
    y_offset = graph.border_top + graph.graph_height + 5
    if graph.show_x_labels:
        max_x_label_height_px = graph.x_label_font_size
        if graph.x_label_rotation:
            longest_label_length = max(map(len, graph.get_x_labels()))
            max_x_label_height_px *= longest_label_length
            max_x_label_height_px *= sin(graph.x_label_rotation)
        y_offset += max_x_label_height_px
        if graph.stagger_x_labels:
            y_offset += max_x_label_height_px + 5
    if graph.show_x_title:
        y_offset += graph.x_title_font_size + 5
    return x_offset, y_offset
