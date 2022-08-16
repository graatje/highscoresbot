from typing import List, Union, Dict

from commands.utils.utils import tablify


def tablify_dict(dictionary: List[Dict[str, str]], order: Union[List[str], None] = None,
                 verbose_names=None, max_length: int = 2000) -> List[str]:
    """


    :param dictionary: list of the json data you want tablified
    :param order: the order in which you want the layout. this is the name of the argument, not the verbose name
    :param verbose_names: dictionary of verbose names. {"name": "verbose_name"}
    :param max_length: the max length of 1 message.
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

            # removing values that were passed in the 'order' list if they don't exist.
            removing = []
            for key in layout:
                if key not in i:
                    removing.append(key)
            while len(removing) != 0:
                layout.remove(removing.pop())
            layoutSet = True
        temp = []
        for key in layout:
            temp.append(i[key])
        values.append(temp)
    layout = [verbose_names.get(key, key) for key in layout]
    return tablify(layout, values, maxlength=max_length)
