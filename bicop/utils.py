def same_type(one, two):
    """Check if two things have the same type."""

    return isinstance(one, type(two))

def merge(one, two, overwrite=False, typecheck=True):
    """Merge data from another configuration space into this one.

    There are two merge methods: overwriting and adding. With the overwrite
    method any existing values will be replaced. In adding mode only
    non-existing keys will be added. If the typecheck flag is set an exception
    will be thrown if a value has a different type in the a different type than
    the original.

    Please note that where possible this will merge data from two to one
    *without copying*.
    """
    if one is two:
        return

    if typecheck and not same_type(one, two):
        raise ValueError, "Type mismatch"

    for (key,value) in two.items():
        if key not in one:
            one[key]=value

        if typecheck and not same_type(one[key], value):
            raise ValueError, "Type mismatch"
        if isinstance(value, dict):
            merge(one[key], two[key], overwrite, typecheck)
        elif not overwrite:
            continue
        else:
            one[key]=two[key]

