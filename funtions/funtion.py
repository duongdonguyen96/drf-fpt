from typing import Union
from django.db import connection, reset_queries
import time
import functools


def dict_fetchall(cursor):
    "Returns all rows from a cursor as a dict."

    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : " + func.__name__)
        print("Number of Queries : {}".format(end_queries - start_queries))
        print("Finished in : {}".format(end - start))

        return result

    return inner_func


def nested_list(
        objects: Union[dict, list],
        map_with_key: str,
        children_fields: dict,
        children_list: list = None,
        key_child_map_parent=None
):
    """

    thay kiểu dũ liệu trong childfields sẽ ra data như mong muốn
    - children_fields={"detail": {'t1', 't2'}}: data child la dict
    - children_fields={"detail": ['t1', 't2']}: data child la list
    - Có thể nest con vào cha theo trường hợp trên:
        + tách key mapping
    re = ctr.nested_list(objects=data, map_with_key='the_luong_id', children_fields={"detail": ['t1', 't2']})

    re = ctr.nested_list(objects=re, map_with_key='id', children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']})

    re = ctr.nested_list(
        objects=NEST_PARENT_FD,
        map_with_key='id',
        children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']},
        children_list=NEST_CHILDREN_FD
    )
    """
    objects_cp = objects.copy()

    if isinstance(objects, dict):
        object_list = [objects_cp]
    else:
        object_list = objects_cp

    if not isinstance(children_fields, dict):
        raise Exception('fields type is dict')

    if len(children_fields) < 1:
        return objects_cp

    if not objects_cp:
        return objects_cp

    for key in children_fields:
        assert isinstance(children_fields[key], (list, set)), 'children is type list'
        assert len(children_fields[key]) > 0, 'children is not null'
        # assert children_fields[key][0][-2:] == "id", "First field of child  must be primary key ID"

    if children_list:
        data_result = _nest_child_to_parent(
            parent_list=object_list,
            map_with_key=map_with_key,
            children_fields=children_fields,
            children_list=children_list,
            key_child_map_parent=key_child_map_parent
        )
    else:
        data_result = _nest_me(
            objects=object_list,
            map_with_key=map_with_key,
            fields=children_fields
        )
    if isinstance(objects, dict):
        return data_result[0] if data_result else {}
    else:
        return data_result


def _nest_me(

        objects: list,
        map_with_key: str,
        fields: dict
):
    all_key_child = []
    for key_child, value_child in fields.items():
        all_key_child += list(value_child)

    nest_level_data = list(
        map(
            lambda x: _nest_level(data_item=x, all_key_child=all_key_child, fields=fields),
            objects
        )
    )

    key_in_parent = set()
    data_parent = dict()

    for temp in list(nest_level_data):
        if temp[map_with_key] not in key_in_parent:
            key_in_parent.add(temp[map_with_key])
            data_parent.update({
                temp[map_with_key]: temp
            })
        else:
            for key_field, value_field in fields.items():
                if not temp[key_field]:
                    continue

                if isinstance(value_field, list):
                    if temp[key_field][0] not in data_parent[temp[map_with_key]][key_field]:
                        data_parent[temp[map_with_key]][key_field].append(temp[key_field][0])
    return list(data_parent.values())


def _nest_child_to_parent(parent_list, map_with_key: str, children_fields: dict, children_list: list = None,
                          key_child_map_parent=None):
    all_key_child = []
    for key_child, value_child in children_fields.items():
        all_key_child += list(value_child)

    nest_level_data = list(
        map(
            lambda x: _nest_level(data_item=x, all_key_child=all_key_child, fields=children_fields),
            children_list
        )
    )

    for parent in parent_list:
        for child in nest_level_data:
            if key_child_map_parent:
                if parent[map_with_key] == child[key_child_map_parent]:
                    _nest_type(parent=parent, child=child, children_fields=children_fields)
            else:
                if parent[map_with_key] == child[map_with_key]:
                    _nest_type(parent=parent, child=child, children_fields=children_fields)
    return parent_list


def _nest_type(parent, child, children_fields):
    for key_field, value_field in children_fields.items():
        if not child[key_field]:
            continue
        if isinstance(value_field, list):
            if key_field not in parent:
                parent.update({
                    key_field: [child[key_field][0]]
                })
            elif child[key_field][0] not in parent[key_field]:
                parent[key_field].append(child[key_field][0])
        else:
            parent.update({
                key_field: child[key_field][0]
            })


def _nest_level(data_item: dict, all_key_child: list, fields: dict):
    child_temp = {}
    parent_temp = {}
    for key_temp, value_temp in data_item.items():
        if key_temp in all_key_child:
            for key_field, value_field in fields.items():
                if key_temp in value_field:
                    if key_field not in child_temp:
                        child_temp.update({
                            key_field: {}
                        })
                    child_temp[key_field].update({
                        key_temp: value_temp
                    })
        else:
            parent_temp.update({
                key_temp: value_temp
            })

    for key_field, value_field in fields.items():
        if isinstance(value_field, list):
            parent_temp.update({
                key_field: [child_temp[key_field]]
            })
        else:
            parent_temp.update({
                key_field: child_temp[key_field]
            })

    return parent_temp
