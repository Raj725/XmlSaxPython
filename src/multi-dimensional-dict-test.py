


drugs={}

drug_1={}
drug_1['name']='d1'
drug_1['forms']=["apple", "banana", "cherry"]

drug_2={}
drug_2['name']='d2'
drug_2['forms']=["apple", "banana", "cherry"]

drug_3={}
drug_3['name']='d3'
drug_3['forms']=["apple", "banana", "cherry"]

drugs['drug_1']=drug_1
drugs['drug_2']=drug_2
drugs['drug_3']=drug_3

# print(drugs)

# for key,value in drugs.items():
#     print(key,value)

drug_4={}
for key,value in drug_3.items():
    print(drug_4, key, type(value))
    if isinstance(value, str):
        drug_4[key]=value
    else:
        for val in value:
            if not key in drug_4:
                drug_4[key] = set()
            drug_4[key].add(val)

print(drug_4)