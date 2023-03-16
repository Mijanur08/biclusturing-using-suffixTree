

class Rule:
    def __init__(self, antecedent_set = set(), consequent_set = set(), support_object = list(),lift = 1.0, confidence = 0.0):
        self._antecedent = antecedent_set
        self._consequent = (consequent_set - antecedent_set)
        self._support_object = support_object
        self._support = len(support_object)
        self._confidence = confidence
        self._lift = lift
    
    def support(self) ->int:
        return self._support
    
    def confidence(self) ->float:
        return self._confidence
    
    def lift(self) -> float:
        return self._lift
    
    def antecedent(self) ->set:
        return self._antecedent
    
    def consequent(self) ->set:
        return self._consequent
    
    def is_valid(self, min_confidence: float) ->bool:
        return self._confidence >= min_confidence
    
    def is_exact(self) ->bool:
        return self._confidence == 1.0

    def find_support_count(itemset: set, FCPs :list) ->int:
        max_count = 0
        for pattern in FCPs:
            sup_count = pattern.support_count()
            if sup_count > max_count and itemset.issubset(pattern.get_itemset()):
                max_count = sup_count
        return max_count

    def generate_rules(GEN, FCP, dataset_size) ->list:
       

        AR_E = list()
        AR_SB = list()
        AR_PB = list()

        for g in GEN:
            for pattern in FCP:
                consequent = (pattern.get_itemset() - g[0].get_itemset())
                if g[1].get_itemset() == pattern.get_itemset():
                    if(g[0].get_itemset() != pattern.get_itemset()):
                        lift = (pattern.support_count()*dataset_size)/(g[0].support_count()*Rule.find_support_count(consequent, FCP)) 
                        rule = Rule(g[0].get_itemset(), pattern.get_itemset(), pattern.get_object(), lift, 1.0)
                        AR_E.append(rule)
                else:
                    if g[1].get_itemset().issubset(pattern.get_itemset()):
                        confidence = float(len(pattern.get_object()))/float(len(g[0].get_object()))
                        lift = (pattern.support_count()*dataset_size)/(g[0].support_count()*Rule.find_support_count(consequent, FCP))
                        rule = Rule(g[0].get_itemset(), pattern.get_itemset(), pattern.get_object(), lift, confidence)
                        AR_SB.append(rule)
        
        for Fi in FCP:
            for Fj in FCP:
                if(Fi.size() < Fj.size() and Fi.get_itemset().issubset(Fj.get_itemset())):
                    confidence = float(len(Fj.get_object()))/float(len(Fi.get_object()))
                    lift = (Fj.support_count()*dataset_size)/(Fi.support_count()*Rule.find_support_count(Fj.get_itemset()-Fi.get_itemset(), FCP))
                    rule = Rule(Fi.get_itemset(), Fj.get_itemset(), Fj.get_object(), lift, confidence)
                    AR_PB.append(rule)
        
        return {
            "AR_E": AR_E,
            "AR_SB": AR_SB,
            "AR_PB": AR_PB
        }
    
    def __str__(self):
        return "Rule(\n\t"+str(self._antecedent)+" => "+str(self._consequent)+"\n\tSupport: "+str(self.support())+"\n\tConfidence: "+str(self.lift())+"\n\tConfidence: "+str(self.confidence())+"\n)\n"
    



