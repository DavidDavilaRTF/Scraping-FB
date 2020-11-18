import pandas
import numpy
import nltk
import csv
csv.field_size_limit(100000000)

chatons = pandas.read_csv('C:/facebook/teb.csv',sep = ';',engine = 'python',encoding='utf-8')
sel = numpy.array(chatons['com'].apply(lambda x: str(x).lower() == 'nan'))
sel = sel == False
chatons = chatons[sel]
chatons.index = range(len(chatons))
del sel

com = chatons['noms'].unique()
post = chatons['nom_posts'].unique()

analyze = pandas.DataFrame()
for p in post:
    temp = pandas.DataFrame()
    temp['post'] = [p]
    sel = numpy.array(chatons['nom_posts'] == p)
    sel = chatons[sel]
    for c in com:
        temp[c] = numpy.sum(sel['noms'] == c)
    analyze = analyze.append(temp)
    del temp
    del sel

analyze.to_csv('C:/facebook/fb_chatons.csv',sep = ';',index = False)
del analyze
del chatons
del com
del post