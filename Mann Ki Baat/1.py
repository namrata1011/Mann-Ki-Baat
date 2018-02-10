#extraction
import urllib.request
import csv
from bs4 import BeautifulSoup
import pygal
import sys
from nltk.corpus import stopwords
filename = "comments.csv"
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
all_comments = [] 
max_comments = 1000
base_url = 'https://www.mygov.in/'
next_page = base_url + '/group-issue/share-your-ideas-pm-narendra-modis-mann-ki-baat-26th-march-2017/'

while next_page and len(all_comments) < max_comments : 
    response = response = urllib.request.urlopen(next_page)
    srcode = response.read()
    soup = BeautifulSoup(srcode, "html.parser")

    all_comments_div=soup.find_all('div', class_="comment_body");
    for div in all_comments_div:
        all_comments.append(div.find('p').text.translate(non_bmp_map))

    next_page = soup.find('li', class_='pager-next first last')
    if next_page : 
        next_page = base_url + next_page.find('a').get('href')
    print('comments: {}'.format(len(all_comments)))

#print(all_comments)
print(len(all_comments))

#remove hindi content
import enchant
import nltk
d = enchant.Dict("en_US")
list = []
s=1
for string in all_comments:
	english_words = []
	for word in string.split():
		if d.check(word):
			english_words.append(word)
	line = ' '.join(english_words)
	list.append(line)
#print(list)
#csv code
ai = open('comments.xls', 'a')
writer = csv.writer(ai)
for i in list:
	writer.writerow([i])

data = (" ".join(list))

#lemmatize data
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize(data)

#remove digits or symbols
import re
letters_only = re.sub("[^a-zA-Z]"," ",data) # remove letters other than a-z
lower_case = letters_only.lower()        # Convert to lower case
words = lower_case.split()

#remove stopwords 
from nltk.corpus import stopwords # Import the stop word list
#print (stopwords.words("english"))
words = [w for w in words if not w in stopwords.words("english")]
# print (words)

pos = ['nice','brilliant','great','good','excellent','entertain','funny','cool','best','fun']
neg = ['bad','gross','disappointed','poor','terrible','crass','boring','uninspiring','disappoint']
categories = ['people','water','government','govt','minister','state','student','education','school','doctors','money','financial','public','private','central','life']
sectors = ['government','govt','minister','state','public','private','central']
education =['student','education','school']
poscore=0
negscore=0
for w in words:
	if w in pos:
		poscore+=1
for w in words:
	if w in neg:
		negscore+=1
print (poscore)
print (negscore)
print (1000-(poscore+negscore))

neutral = 1000-(poscore+negscore)
bar_chart = pygal.Pie()
bar_chart.add('Positive', [poscore])
bar_chart.add('Negative', [negscore])
bar_chart.add('Neutral', [neutral])
bar_chart.render_to_file('pie_chart.svg')

edu=0
for w in words:
	if w in education:
		edu+=1
gauge = pygal.SolidGauge(inner_radius=0.50)
percent_formatter = lambda x: '{:.10g}'.format(x)
gauge.value_formatter = percent_formatter
gauge.add('EDUCATION', [{'value': edu, 'max_value': 1000}])
gauge.render()
gauge.render_to_file('education.svg')

#tagging
tagged = (nltk.pos_tag(words))
# print (tagged)

#freq of tags
fd = nltk.FreqDist(tagged)
fd_tagged = nltk.FreqDist(tag for (word,tag) in tagged)
top = fd_tagged.most_common(10)
print (top)

# print([w[0] for (w, _) in fd.most_common() if w[1] == 'NNP'][:10])
# find top 10 nouns
nouns = [word for word,pos in tagged if pos == 'NN' or pos == 'NNS']
freq = nltk.FreqDist(nouns)
top = freq.most_common(25)
print("top nouns: ")
print(top)

nouns = [word for word,pos in tagged if pos == 'JJ' or pos == 'JJR' or pos == 'JJS']
freq = nltk.FreqDist(nouns)
top = freq.most_common(25)
print("top adjectives: ")
print(top)

nouns = [word for word,pos in tagged if pos == 'RB' or pos == 'RBR' or pos == 'RBS']
freq = nltk.FreqDist(nouns)
top = freq.most_common(25)
print("top adverbs: ")
print(top)

nouns = [word for word,pos in tagged if pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP']
freq = nltk.FreqDist(nouns)
top = freq.most_common(25)
print("top verbs: ")
print(top)

#find top 10 used words - correct
freq = nltk.FreqDist(words)
top10 = freq.most_common(25)
print("top words: ")
print (top10)

line_chart = pygal.Bar()
for token,count in top10:
	line_chart.add(token,count)
line_chart.render_to_file('bar_chart.svg')