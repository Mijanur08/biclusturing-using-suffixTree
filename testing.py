from demodata import SFD_1
from suffix_tree import build_sufix_tree
from frequent_patterns import get_FCPs
# from demodata import SFD_1
from association_rules import Rule
from bicluster import get_clusters
from json import dumps
from Preprocessing import get_SFD, get_org_item
import pandas as pd

# tree = build_sufix_tree({"D1": SFD_1})
SFD_1 = get_SFD('Datasets\DataSetA.csv',min_support=40)
tree = build_sufix_tree(SFD_1)
FCPs = get_FCPs(tree, min_support_count=3)
biclusters = get_clusters(FCPs, min_support_count=3, min_size=2)
FCPJSON = [fcp.toJSON() for fcp in FCPs]

print("Total: "+str(len(FCPs))+" FCP generated.")

from generators import get_generators
GEN = get_generators(FCPs)

# GENJSON = [{ "generator" : list(g[0].get_itemset()), "FCP" : g[1].toJSON()} for g in GEN]

# with open("gen.json", "w") as outputfile:
#     outputfile.write(dumps(GENJSON, indent=2))

rules = Rule.generate_rules(GEN, FCPs)



# with open("tree.json", "w") as outputfile:
#     outputfile.write(dumps(tree, indent=2))

# with open("biclusters.json", "w") as outputfile:
#     outputfile.write(dumps(biclusters, indent=2))

# with open("fcps.json", "w") as outputfile:
#     outputfile.write(dumps(FCPJSON, indent=2))



# for key in list(rules.keys()):
#     print("Total "+str(len(rules[key]))+" "+str(key)+" rules generated.")
#     with open("rule_"+str(key)+".json", "w") as outputfile:
#         outputfile.write(dumps([rule.toJSON(True) for rule in rules[key]], indent=2))

get_name_of_items = get_org_item()

for key in list(rules.keys()):
    res = list()
    for rule in rules[key]:
        antecedent = str([get_name_of_items[id] for id in rule.antecedent()])
        consequent = str([get_name_of_items[id] for id in rule.consequent()])
        confidence = rule.confidence()
        support = rule.support()
        res.append([antecedent,consequent,confidence,support])

    rule_dataframe = pd.DataFrame(res, columns = ["Antecedent", "Consequent", "Confidence", "Support Count"])
    filename = f"./output/rule_{key}.csv"
    rule_dataframe.to_csv(filename)
    print(f"Created file {filename}")

for key in list(rules.keys()):
    print("Total "+str(len(rules[key]))+" "+str(key)+" rules generated.")

# from printing_util import generate_tree_image
# generate_tree_image(tree, "tree.png")