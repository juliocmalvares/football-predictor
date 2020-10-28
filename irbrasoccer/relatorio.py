import leia
from preprocess.cleaners import dot_spliter_run
import json
import pathlib
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def build() -> list:
    data: list  = dot_spliter_run()[:20]
    processed = []
    analyzer = leia.SentimentIntensityAnalyzer()
    print('[LOG] Starting process')
    for sample in data:
        if sample.get('phrases') != None:
            d = {}
            d['phrases'] = list()
            for i in sample['phrases']:
                if i != '' and i != '.':
                    d['phrases'].append({
                        'phrase': i,
                        'result': analyzer.polarity_scores(i)
                    })
            # if sample.get('comments_phrases') != None:
            #     for i in sample['comments_phrases']:
            #         if i != '' and i != '.':
            #             d['phrases'].append({
            #                 'phrase': i,
            #                 'result': analyzer.polarity_scores(i)
            #             })
            d['final'] = {
                'neg': 0,
                'pos': 0,
                'neu': 0,
                'compound': 0,
            }
            for i in d['phrases']:
                d['final']['neg'] += i['result']['neg']
                d['final']['neu'] += i['result']['neu']
                d['final']['pos'] += i['result']['pos']
                d['final']['compound'] += i['result']['compound']
            d['final']['neg'] /= len(d['phrases'])
            d['final']['neu'] /= len(d['phrases'])
            d['final']['pos'] /= len(d['phrases'])
            d['final']['compound'] /= len(d['phrases'])
            processed.append(d)
        # print(sample)
        # print(sample['phrases'])
    # print(processed[:20])
    print(len(processed))
    for i in range(20):
        with open('./result_rel/{}.json'.format(i), 'w') as jsf:
            json.dump(processed[i], jsf, indent=4, ensure_ascii=False)
    return processed

def build_word_cloud(data: list) -> None:
    words = ''
    print('[LOG] Building Corpus')
    for i in data:
        for j in i['phrases']:
            for k in j['phrase'].split(' '):
                if words.rfind(k) == -1:
                    words += k + ' '
    wc = WordCloud(min_font_size=20, max_font_size=300, width=2000, height=1000, mode='RGB').generate(words)
    plt.figure(figsize = (16,9))
    plt.imshow(wc, interpolation = "bilinear")
    plt.axis("off")
    plt.show()

data = build()
build_word_cloud(data)
