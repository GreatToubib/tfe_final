import nltk
import spacy
import pandas as pd
sp = spacy.load('en_core_web_md') # keeps tok2vec, tagger ,parser and attribute_ruler, tok2vec ( vector), ner ( ent)
#     ['tok2vec', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer']
# "tok2vec","parser", "attribute_ruler", "entities"]
########################################## WordNet ######################################################

from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet

def POSLemma_extractor(proc_sent_df,POSLemmaChoice):
    df_len=len(proc_sent_df.index)
    percent=int(df_len/100)
    POSLemma_sent_dic={}
    for index, row in proc_sent_df.iterrows():

        if (index%percent)==1:
            print(int(index/df_len*100) , " % processed", end="\r", flush=True)

        processed_sentence, POS_tags= POSLemmaFunction(POSLemmaChoice , row["processed_sentence"])
#         print(POS_tags)
        POSLemma_sent_dic[index] = {'review_id' : row["review_id"],
                      'game_title' : row["game_title"],
                      'sentence': row["sentence"],
                      'vader_polarity': row["vader_polarity"],
                      'processed_sentence': processed_sentence,
                      'tags':POS_tags}

    POSLemma_sent_df = pd.DataFrame.from_dict(POSLemma_sent_dic,orient='index')  # Creation of the dataframe    
    POSLemma_sent_df = POSLemma_sent_df.sort_index()  # sorting by index

    POSLemma_sent_df.shape
    
    print("100% processed     ")
    return POSLemma_sent_df



# simplified Wordnet Tags 
def WN_simple_tagger(nltk_tag):
	if nltk_tag.startswith('J'):  # "a"
		return wordnet.ADJ
	elif nltk_tag.startswith('V'): # "v"
		return wordnet.VERB
	elif nltk_tag.startswith('N'): # "n"
		return wordnet.NOUN
	elif nltk_tag.startswith('R'): # "r"
		return wordnet.ADV
	else:		
		return None

def WordNetPOSLemmatizer(sentence):
    lemmatizer = WordNetLemmatizer()
    # tokenize the sentence and find the POS tag for each token
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    # print(pos_tagged)
    wordnet_tagged = list(map(lambda x: (x[0], WN_simple_tagger(x[1])), pos_tagged))
    # print(wordnet_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None: # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else: # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    lemmatized_sentence = " ".join(lemmatized_sentence) #reform the sentence
    # print(lemmatized_sentence)
    return lemmatized_sentence , wordnet_tagged


########################################## textblob ######################################################
from textblob import TextBlob, Word
  
def TextBlobPOSLemmatizer(sentence):
    sent = TextBlob(sentence)
    tag_dict = {"J": 'a', "N": 'n', "V": 'v', "R": 'r'}
    words_tags = [(word, tag_dict.get(pos_tag[0], None)) for word, pos_tag in sent.tags]   # convert to our simplified  word tag 
    lemma_list = [wd.lemmatize(tag) for wd, tag in words_tags] # Lemmatize using tag
    lemmatized_sentence = " ".join(lemma_list)
    return lemmatized_sentence, words_tags


########################################## Spacy ######################################################

def SpacyPOSLemmatizer(sentence):
    #     for sentence in sp.pipe(texts_batch, disable=["tok2vec","parser", "attribute_ruler", "entities"]): # keeps tok2vec, tagger    
    #     ['tok2vec', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer']
    
    sentence= sp(sentence)
    lemmatized_sentence = " ".join([word.lemma_ for word in sentence ])
    tagList=[]
    tag_dict = {"ADJ": 'a', "NOUN": 'n', "VERB": 'v', "ADV": 'r'}
    for word in sentence:
        tagList.append( (word.text, tag_dict.get(word.pos_, None)) )
    return lemmatized_sentence, tagList

# docs = list(sp.pipe(texts))[0]   # works as expected, sp.pipe returns a generator not a list. 


    
########################################## Choose method ######################################################

def POSLemmaFunction(POSLem_choice, sentence ):
    if POSLem_choice == "WN": return WordNetPOSLemmatizer(sentence)
    elif POSLem_choice== "TB": return TextBlobPOSLemmatizer(sentence)
    elif POSLem_choice== "SP": return SpacyPOSLemmatizer(sentence)