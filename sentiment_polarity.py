from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()
def getVaderPolarity(sentence):
    return analyser.polarity_scores(sentence)["compound"]

def getVaderMatch(df):
    df["vader_match"]=np.where(  
      ( ((df['score'] > 0.5) & (df['vader_polarity'] > 0)) |  ((df['score'] < 0.5) & (df['vader_polarity'] < 0)) ) 
        , 1, 0)
    return df
  
## NLTK sentiment 

# textblob sentiment
