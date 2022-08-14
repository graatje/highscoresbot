from typing import List, Union, Dict

from commands.utils.utils import tablify


def tablify_dict(dictionary: List[Dict[str, str]], order: Union[List[str], None] = None) -> List[str]:
    """

    :param dictionary: list of the json data you want tablified
    :param order: the order in which you want the
    :return:
    """
    layout = []
    if order is not None:
        layout += order
    layoutSet = False

    values = []
    for i in dictionary:
        if not layoutSet:
            for key in i.keys():
                if key not in layout:
                    layout.append(key)
            layoutSet = True
        temp = []
        for key in layout:
            temp.append(i[key])
        values.append(temp)
    return tablify(layout, values)
