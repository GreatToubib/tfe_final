from nltk.corpus import wordnet
nltk.download('wordnet')    
w1 = wordnet.synset("price" '.n.01')  #wordnet.lemmas(i2)[0]
w2 = wordnet.synset("amount" + '.n.01') 
print(w1.wup_similarity(w2))
F_dict={}
n_feature=0
for feature, opinions in FOPs_game_dic.items():
    for opinion in feature:
        n_feature+=1
    if feature in F_dict:
        F_dict[feature]+=1
    else:
        F_dict[feature]=0

F_list=list(F_dict.keys())
print(len(F_dict), n_feature)


############### merge similar features #####################

sim_dict = FOPs_game_dic
print(len(sim_dict))

import itertools
k=0

i=-1
while 1:
    if i%50==0:
        print(int(i/len(sim_dict)*100), " %")
    i+=1
    try: 
        a= F_list[i]
    except:
        print("end i")
        break

    j=-1
  
    while 1:
        j+=1

        try:
            b= F_list[j]
            if b==a: 
            # print("end j ")
                break
        except:
            break

    try:
        w1 = wordnet.synset(a+ '.n.01')  #wordnet.lemmas(i2)[0]
        w2 = wordnet.synset(b + '.n.01') 
    except:
      # print("not a noun")
      continue

    wup=w1.wup_similarity(w2)

    if wup>0.50:
        # print(wup, a, b)
        feature_count_a = sum(d['count'] for d in sim_dict[a].values() if d)
        feature_count_b = sum(d['count'] for d in sim_dict[b].values() if d)
        if feature_count_a==0 or feature_count_b==0:
            continue
      
        if feature_count_a > feature_count_b:
            print("merging", b," into ", a)
            sim_dict = merge_features(a,b,sim_dict)
            continue # dont compare i to all other j
        else:
            print("merging", a," into ", b)
            sim_dict = merge_features(b,a,sim_dict)
            continue # dont compare i to all other j
            
            
            
            
def merge_features(a,b,sim_dict):
    for opinion in sim_dict[b].keys():

        if opinion in sim_dict[a].keys():
            sim_dict[a][opinion]["count"] += sim_dict[b][opinion]["count"]
            sim_dict[a][opinion]["importance"] += sim_dict[b][opinion]["importance"]
        else:
            sim_dict[a][opinion]={}
            sim_dict[a][opinion]["count"] = sim_dict[b][opinion]["count"]
            sim_dict[a][opinion]["importance"] = sim_dict[b][opinion]["importance"]

        sim_dict[b][opinion]["count"] = 0
        sim_dict[b][opinion]["importance"] = 0
        return sim_dict