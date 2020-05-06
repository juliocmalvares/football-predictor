import dataframe_generator

dtf = dataframe_generator.dataframe_generator()
df = dtf.gen_news()

import os

os.chdir('../preprocessing')
print(os.getcwd(), os.listdir())


from stopwords import stopwords

stop = stopwords()
stop.apply(df.text)
