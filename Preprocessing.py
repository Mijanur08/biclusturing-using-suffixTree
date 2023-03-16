import csv

attribute_mapping = dict() #Global variable that stores the mapping between items and assigned ids


def map_attributes(attribute_count,min_supp_cnt): #This function will create the object mapping 
    mp = dict()
    id = 1
    for keys in attribute_count:
        if attribute_count[keys] > min_supp_cnt:
            mp[keys] = id
            id+=1
    return mp

def get_items_mapping(): #will give access to the object map outside of the module
    return attribute_mapping


def get_org_item(): # will create reverse mapping from ids to objects
    reverse_mp = dict()
    for key in attribute_mapping:
        reverse_mp[attribute_mapping[key]] = key
    return reverse_mp

def get_sorted_dictionary(attribute_count):
    temp_sorted = sorted(attribute_count.items(), key=lambda x:x[1])
    return dict(temp_sorted)

def generate_sfd(rows, attribute_count,min_supp_cnt):
    sfd = dict()
    cnt = 1
    for row in rows:
        temp_dict = dict()
        for items in row:
            if attribute_count[items]>min_supp_cnt:
                temp_dict[attribute_mapping[items]] = attribute_count[items]
        sorted_row = get_sorted_dictionary(temp_dict)
        if len(sorted_row) > 1:
            transaction = "T"+str(cnt)
            cnt+=1
            sfd[transaction]=list((sorted_row.keys()))
    return sfd

def get_SFD(filepath, min_support):

    attribute_count = dict()
    rows = list()
    cnt = 120
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            arr = list()
            repeat_check = dict()
            for str in row[:-1]:
                if str not in repeat_check:
                    if str not in attribute_count:
                        attribute_count[str] = 1
                    else:
                        attribute_count[str]+=1
                    arr.append(str)
            rows.append(arr)
            cnt-=1
            if cnt == 0 :
                break
    
    # print(rows)
    attribute_count = get_sorted_dictionary(attribute_count)
    # print(attribute_count)
    min_supp_cnt = len(rows)*(min_support/100)
    # print("minimum support = ",min_supp_cnt)
    global attribute_mapping
    attribute_mapping = map_attributes(attribute_count,min_supp_cnt)
    final_sfd = generate_sfd(rows,attribute_count,min_supp_cnt)
    return final_sfd


# if __name__ == "__main__":
#     filepath = 'Datasets\DataSetA.csv'
#     print(get_SFD(filepath, 45))
