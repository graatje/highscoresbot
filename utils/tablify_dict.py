from typing import List, Union, Dict

from commands.utils.utils import tablify


def tablify_dict(dictionary: List[Dict[str, str]], order: Union[List[str], None] = None,
                 verbose_names=None) -> List[str]:
    """


    :param dictionary: list of the json data you want tablified
    :param order: the order in which you want the layout.
    :param verbose_names:
    :return:
    """
    if verbose_names is None:
        verbose_names = {}
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
    layout = [verbose_names.get(key, key) for key in layout]
    return tablify(layout, values)
