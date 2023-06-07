from biclustering import FIST
fist = FIST()
fist.process("./Datasets/","Exampledata.csv",'ID','Itemsets',max_entries=10000,
min_supp_percent=30,min_conf_percent=0.0,produce_final_img=True)
