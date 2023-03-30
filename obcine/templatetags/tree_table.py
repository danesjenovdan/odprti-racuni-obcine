import math

from django import template

register = template.Library()


def next_multiple(value, multiple_of):
    return math.ceil(value / multiple_of) * multiple_of


def get_max_amount(node):
    return max([node.get("amount", 0), node.get("planned", 0), node.get("realized", 0)])


@register.simple_tag
def child_max_graph_scale(tree_node, precision=2, slice_count=6):
    children = (tree_node or {}).get("children", []) or [{"amount": 0}]
    child_amounts = [get_max_amount(child) for child in children]
    value_max = math.ceil(max(child_amounts))
    num_digits = len(str(value_max))
    divisor = math.pow(10, num_digits - precision)
    factor = math.ceil(value_max / divisor)
    rounded_max = next_multiple(factor, 6) * divisor
    return rounded_max


@register.simple_tag
def graph_scale_values(value_max, slice_count=6):
    value_slice = value_max / slice_count
    values = [int(value_slice * i) for i in range(slice_count + 1)]
    return values
