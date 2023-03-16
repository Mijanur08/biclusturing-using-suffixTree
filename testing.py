
from suffix_tree import build_sufix_tree
from frequent_patterns import get_FCPs
from association_rules import Rule
from json import dumps
from Preprocessing import get_SFD_other_fields
import pandas as pd

#Taking the Inputs
print("***Taking Input from dataset and generating SFD***")
(SFD, minimum_support_count, dataset_size, attribute_mapping, mapping_ids_to_org) = get_SFD_other_fields('Datasets\DataSetB.csv',min_support=7)
minimum_support_count_for_testing = 3

#Processing The Inputs
print("***Generating Tree from the SFD***")
tree = build_sufix_tree(SFD)

print("***Generating Frequent Close Patterns from the Tree using minimum support count = "+str(minimum_support_count_for_testing)+" ***")
FCPs = get_FCPs(tree, minimum_support_count_for_testing)
print("Total: "+str(len(FCPs))+" FCP generated.")

print("***Creating The generators***")
from generators import get_generators
GEN = get_generators(FCPs)



#Generating Outputs
print("***Processing Outputs***")
#Output-1 : Association Rules
rules = Rule.generate_rules(GEN, FCPs,dataset_size)

for key in list(rules.keys()):
    res = list()
    for rule in rules[key]:
        antecedent = str([mapping_ids_to_org[id] for id in rule.antecedent()])
        consequent = str([mapping_ids_to_org[id] for id in rule.consequent()])
        confidence = rule.confidence()
        support = rule.support()
        lift = rule.lift()
        res.append([antecedent,consequent,confidence,support,lift])

    rule_dataframe = pd.DataFrame(res, columns = ["Antecedent", "Consequent", "Confidence", "Support Count", "lift"])
    filename = f"./output/rule_{key}.csv"
    rule_dataframe.to_csv(filename)
    print(f"Created file {filename}")

for key in list(rules.keys()):
    print("Total "+str(len(rules[key]))+" "+str(key)+" rules generated.")

#Output-2: Biclusters   
data = list()

for fcp in FCPs:
    if fcp.support_count() >= minimum_support_count_for_testing and fcp.size() >= 2:
        itemset = str([mapping_ids_to_org[number] for number in fcp.get_itemset()])
        support_count = fcp.support_count()
        support_percentage = 100*support_count/dataset_size
        support_obj = fcp.get_object_as_line()
        data.append([itemset, support_count, support_percentage, support_obj])
        
df = pd.DataFrame(data, columns=["Itemset", "Support(count)", "Support(%)", "Support Object"])
filepath = f"./output/biclusters.csv"
df.to_csv(filepath)
print(f"Bi-clusters stored in file {filepath}")