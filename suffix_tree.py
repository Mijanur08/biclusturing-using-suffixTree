
def get_all_suffix(arr, leaf_obj):
    all_suffix = []

    for i in range(len(arr)):
        all_suffix.append(get_suffix(arr, i, leaf_obj))

    return all_suffix


def get_suffix(arr, idx, leaf_obj):
    suffix = []

    while idx < len(arr):
        suffix.append(arr[idx])
        idx += 1

    suffix.append(leaf_obj)
    return suffix


def build_sufix_tree(sfd):
    # HTree
    h_tree = {}

    for rows in sfd.keys():
        suffixes = get_all_suffix(sfd[rows], [rows])

        for suffix in suffixes:
            assert len(suffix) > 1

            if suffix[0] in h_tree.keys():
                match(h_tree[suffix[0]], suffix)
            else:
                h_tree[suffix[0]] = build(suffix)

    return h_tree


def match(h_node, suffix):
    assert h_node["item"] == suffix[0]

    if (len(suffix) == 2):  # suffix[1] is a leaf node
        if h_node["leaf"] == None:
            h_node["leaf"] = suffix[1].copy()
        else:
            # merge the new leaf with the existing leaf
            leaf = h_node["leaf"]
            tid = suffix[1][0]

            if (tid in leaf):
                print("Warning: Same row already exists in TREE.")
            else:
                leaf.append(tid)
    else:
        # suffix[1] will not be a leaf

        # matching suffix[1]
        for child in h_node["children"]:
            if child["item"] == suffix[1]:
                match(child, suffix[1:])
                return
        # if no match is found, building h_node
        h_node["children"].append(build(suffix[1:]))


def build(suffix):
    assert len(suffix) >= 2
    h_node = {
        "item": suffix[0],
        "children": [],
        "leaf": None
    }

    if len(suffix) == 2:
        h_node["leaf"] = suffix[1].copy()
    else:
        h_node["children"].append(build(suffix[1:]))
    return h_node


# if __name__ =='__main__':

#     SFD_mdm = {
#         "O1": [1,3,4,5],
#         "O2": [2,6,7],
#         "O3": [3,4,5],
#         "O5": [2,6,7],
#         "O6": [1,3,4,5],
#         "O7": [2,6,7],
#         "O8": [1,3,4,5],
#         "O9": [2,6,7],
#         "O10": [1,3,4,5,6,7]
#     }


#     tree = build_sufix_tree(SFD_mdm)

#     from printing_util import generate_tree_image
#     generate_tree_image(tree, "tree.png")

#     from json import dumps
#     with open("tree.json", "w") as outputfile:
#         outputfile.write(dumps(tree, indent=2))
