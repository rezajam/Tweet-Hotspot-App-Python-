import numpy.matlib
import numpy as np
import sys
from copy import deepcopy
import matplotlib.pyplot as plt
import scipy 
import random 
import logging
from random import randint
import csv
import pandas as pd
import math 
from scipy.spatial.distance import pdist, squareform
from collections import OrderedDict
from operator import itemgetter
import itertools
from itertools import islice

list_0 = []
list_1 = []
list_2 = []
dict_0 = {}
dict_1 = {}
dict_2 = {}
foo = ()
def take(n, iterable):
	return list(islice(iterable,n))

files = open('recomendation.txt', 'a')


#go through the csv file that has and in each different cluster dictionary, add the hastags that are suppose to be in that cluser to the dictionary
#if the hashtags are already in the dictionary, incease the value of the hashtag.
with open('export_dataframe.csv',newline='',encoding='utf8') as f:
	reader = csv.reader(f)
	next(reader)
	
	for row in reader:
		
		hast = row[3].split(',')
		
		if (row[5] == '0'):
			
			for has in hast:
				has = has.replace(' ', '')
				if(len(has) > 0):
					if has not in dict_0:
						dict_0[has] = 1
					else:
						dict_0[has] += 1
		if (row[5] == '1'):
			
			
			for has in hast:
				has = has.replace(' ', '')
				
				if(len(has) > 0):
					if has not in dict_1:
						dict_1[has] = 1
					else:
						dict_1[has] += 1
		if (row[5] == '2'):
		
		
			for has in hast:
				has = has.replace(' ', '')
				
				if(len(has) > 0):
					if has not in dict_2:
						dict_2[has] = 1
					else:
						dict_2[has] += 1

# Sort the dictionary made for each cluster's hashtags
ordered = OrderedDict(sorted(dict_0.items(), key=itemgetter(1), reverse=True))
ordered1 = OrderedDict(sorted(dict_1.items(), key=itemgetter(1), reverse=True))
ordered2 = OrderedDict(sorted(dict_2.items(), key=itemgetter(1), reverse=True))

#get top then for each cluster
out = dict(list(ordered.items())[0:10])
out1 = dict(list(ordered1.items())[0:10])
out2 = dict(list(ordered2.items())[0:10])
# out2 = sorted(out.items())
# print(out)

# print(out)
# print(out1)
# print(out2)


#grapg the trending hashtags for the clusters
plt.bar(*zip(*out.items()))
# print('tring to show graph')
plt.title('Cluster 0 Trending Hashtags')
plt.show()

plt.bar(*zip(*out1.items()))
# print('tring to show graph')
plt.title('Cluster 1 Trending Hashtags')
plt.show()

plt.bar(*zip(*out2.items()))
# print('tring to show graph')
plt.title('Cluster 2 Trending Hashtags')
plt.show()

df = pd.read_csv("export_dataframe.csv")
df['ID'] = df['ID'].astype('int64')
df2 = df


#Recomendation system. For every user in the list, checks for the oens that match that user in hashtags and sentiment and cluster and prints it in another file the pairs that match
for i in range(len(df)):
	for j in range(i+1, len(df2)):
		if(df['Hashtag'][i] == df['Hashtag'][j] and df['Sentiment'][i] == df['Sentiment'][j] and df['Clusters'][i] == df['Clusters'][j]):
			# print('works')
			files.write('%s and %s \n' % (df['ID'][i], df['ID'][j]))

files.close()
