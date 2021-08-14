import pickle
import pandas as pd

def FOPs_extractor(POS_tags, polarity, FOPs_game_dic):
    F_list=[]
    O_list=[]
    FOPs={}

    # tag features and opinions
    for word, tag in POS_tags:
        if tag=="n":
            # print(word, tag)
            F_list.append(word)
        else: # or tag=="v"
            O_list.append(word)

    # Count FSPs and weighted importance
    for feature in F_list:
        if feature not in FOPs_game_dic:
            FOPs_game_dic[feature]={} 

        FOPs[feature]=O_list

        for opinion in O_list:
            if opinion not in FOPs_game_dic[feature]:
                FOPs_game_dic[feature][opinion]={}
                FOPs_game_dic[feature][opinion]["count"]=1 # frequency, number of occurence of the pair
                FOPs_game_dic[feature][opinion]["importance"]=polarity # frequency weighted with polarity of the sentence containing the occurence
            else:
                FOPs_game_dic[feature][opinion]["count"]+=1
                FOPs_game_dic[feature][opinion]["importance"]+=polarity


    return FOPs, FOPs_game_dic
    # print(F_list)
    # def product_FOPs_extractor(df):
    #   count all FOPs 
    
def extract_all_FOPs(FOPs_df, chosen_game):

    FOPs_df=FOPs_df.loc[FOPs_df['game_title'] ==chosen_game ]
    FOPs_df=FOPs_df.reset_index(drop=True)

    df_len=len(FOPs_df.index)
    print(df_len, " sentences for the game ",chosen_game )
    percent=int(df_len/10)
    FOPs_sent_dic={} # FOPs in each sentence 
    FOPs_game_dic={} # FOPs all data-wise
    for index, row in FOPs_df.iterrows():
    #     if index==2:
    #         break
        if (index%percent)==1:
            print(int(index/df_len*100) , " % processed", end="\r", flush=True)

        sent_FOPs, FOPs_game_dic = FOPs_extractor(row["tags"], row["vader_polarity"], FOPs_game_dic)

        FOPs_sent_dic[index] = {'review_id' : row["review_id"],
                      'game_title' : row["game_title"],
                      'sentence': row["sentence"],
                      'vader_polarity': row["vader_polarity"],
                      'processed_sentence': row["processed_sentence"],
                      'tags': row["tags"],
                      'FOPs': sent_FOPs}
        
    return FOPs_game_dic




from csv import writer 
import os
    
def save_FOPs_dic_csv(FOPs_game_dic,wdir, chosen_game ):
    csvName = wdir+chosen_game+"_FOPs.csv"
    try:
        os.remove(csvName)
    except OSError:
        pass


    with open(csvName, 'a', newline='') as csvfile:
        
        csvwriter = writer(csvfile, delimiter=' ')
        csvwriter.writerow(["feature"+","+ "opinion"+","+ "count"+","+ "importance"])
    
        all_FOPs={}
        for feature, opinions in FOPs_game_dic.items():

            for  opinion, scores in opinions.items():
                csvwriter.writerow([feature +","+ opinion+","+ str(scores["count"])+","+ str(scores["importance"])])
    f = open(wdir+chosen_game+"_FOPs.pkl","wb")
    pickle.dump(FOPs_game_dic,f)
    f.close()


def read_FOPs_csv(filepath):
    FOPs_df = pd.read_csv(filepath)  # Creation of the dataframe 
    FOPs_df["polarity"] = FOPs_df["importance"]/FOPs_df["count"]
    FOPs_df["abs_importance"]= abs(FOPs_df["importance"])
    FOPs_df = FOPs_df.sort_values('count', ascending=False)
    FOPs_df=FOPs_df.reset_index(drop=True)
    return FOPs_df