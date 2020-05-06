import dataframe_generator
df = dataframe_generator.dataframe_generator().gen_news()
import os
os.chdir('../preprocessing')
import pprocess
st = pprocess.preprocessing()
st.applystw(df, 'text', 'text_processed')
st.applystem(df, 'text_processed', 'text_processed')
st.applystw(df, 'title', 'title_processed')
st.applystem(df, 'title_processed', 'title_processed')
st.toPickle(df, 'news.pkl')

