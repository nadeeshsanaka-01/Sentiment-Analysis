import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Sentiment Analysis System")
st.title("SENTIMENT ANALYSIS SYSTEM")
choice=st.sidebar.selectbox("My Menu", ("HOME", "ANALYSIS", "RESULTS"))
if(choice=="HOME"):
   st.image("https://user-images.githubusercontent.com/57702598/90991088-264c8880-e56c-11ea-9895-90029d3c2139.gif")
   st.write("It is a natural language processing system which can analyze the sentiment of text data")
   st.write("The application predicts the sentiment into 3 categories: Positive, Negative and Neutral")
   st.write("This application then visualises the results based on different factors such as age, gender, language and city")
elif(choice=="ANALYSIS"):
   sid=st.text_input("Enter your Google Sheet ID")
   r=st.text_input("Enter range between first column and last column")
   c=st.text_input("Enter column name that is to be analyzed")
   btn=st.button("Analyze")
   if btn:
       if 'cred' not in st.session_state:
           f=InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
           st.session_state['cred']=f.run_local_server(port=0)
       mymodel=SentimentIntensityAnalyzer()
       service=build("Sheets", "v4", credentials=st.session_state['cred']).spreadsheets().values()
       d=service.get(spreadsheetId=sid, range=r).execute()
       data=d["values"]
       df=pd.DataFrame(data=data[1:], columns=data[0])
       l=[]
       for i in range(0, len(df)):
           t=df._get_value(i, "Review")
           pred=mymodel.polarity_scores(t)
           if(pred['compound']>0.5):
               l.append("Positive")
           elif(pred["compound"]<-0.5):
               l.append("Negative")
           else:
               l.append("Neutral")
       df['Sentiment']=l
       df.to_csv("results.csv", index=False)
       st.subheader("The analysis results have been saved by the name of a results.csv")
elif(choice=="RESULTS"):
   df=pd.read_csv("results.csv")
   choice2=st.selectbox("Choose visualization", ("NONE", "PIE CHART", "HISTOGRAM", "BAR PLOT", "COUNT PLOT", "SCATTER PLOT"))
   st.dataframe(df)
   if(choice2=="PIE CHART"):
       sentiment_counts = df['Sentiment'].value_counts()
       plt.figure(figsize=(6, 6))
       sentiment_counts.plot.pie(colors=['green', 'orange', 'red'])
       plt.title('Sentiment Distribution')
       plt.ylabel('')
       st.pyplot(plt)
   if(choice2=="HISTOGRAM"):
       k=st.selectbox("Choose column", df.columns)
       if k:
           plt.figure(figsize=(6, 4))
           sns.histplot(df[k], bins=5, kde=True, color='blue')
           plt.title(k+' Distribution')
           plt.xlabel(k)
           plt.ylabel('Frequency')
           st.pyplot(plt)
   if(choice2=="BAR PLOT"):
       g=st.selectbox("Choose column", df.columns)
       if g:
           gender_counts = df[g].value_counts()
           plt.figure(figsize=(6, 4))
           sns.barplot(x=gender_counts.index, y=gender_counts.values)
           plt.title(g+' Distribution')
           plt.xlabel(g)
           plt.ylabel('Count')
           st.pyplot(plt)
   if(choice2=="COUNT PLOT"):
       h=st.selectbox("Choose column", df.columns)
       if h:
           plt.figure(figsize=(8, 6))
           sns.countplot(data=df, x='Sentiment', hue=h, palette='Set2')
           plt.title('Sentiment Distribution by '+h)
           plt.xlabel('Sentiment')
           plt.ylabel('Count')
           plt.legend(title=h)
           st.pyplot(plt)
   if(choice2=="SCATTER PLOT"):
       i=st.selectbox("Choose column", df.columns)
       j=st.selectbox("Choose another column", df.columns)
       if i and j:
           plt.figure(figsize=(8, 6))
           df['SentimentScore'] = df['Sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1})
           plt.figure(figsize=(8, 6))
           sns.scatterplot(data=df, x=i, y='SentimentScore', hue=j, style=j, s=100)
           plt.title('Scatterplot: '+i+' vs Sentiment Score')
           plt.xlabel(i)
           plt.ylabel('Sentiment Score')
           plt.legend(title=j)
           st.pyplot(plt)
