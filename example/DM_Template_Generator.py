#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import random

INPUT = pd.read_csv('DEF.csv',sep=";")

n = int(INPUT['NUM'][3])

m = int(INPUT['NUM'][4])

maax = max(m,n)

miin = min(m,n)

# define x-axis of dataframe
index = range(0,(maax+4))

# define y-axis of dataframe
columns = []

for j in range(0,(maax+2)):
    
    col = 'Unnamed: '+str(j)
    
    columns.append(col)
    
# Generate dataframe to fill
df=pd.DataFrame(index=index,columns=columns)

# construct dataframe
df = df.rename(columns={'Unnamed: 0': 'Case', 'Unnamed: 1': 'Num.'})

df['Case'][0]='n (Atributes)'

df['Case'][1]='m (Alternatives)'

df['Case'][n+2]='Pesos'

df['Case'][n+3]='END'

df['Num.'][0]=str(n)

df['Num.'][1]=str(m)

for i in range(n):
    
    df['Case'][i+2]=i
    
    df['Num.'][i+2]=random.randint(0, 1)
    
df['Num.'][n+2]=random.randint(0, 1)

df['Num.'][n+3]=0

for j in range(2,(miin+2)):
    
    for i in range(maax):
        
        df['Unnamed: '+str(j)][i+2]=[0.0,0.0,0.0,0.0]

for j in range(2,(maax+2)):
    
    df['Unnamed: '+str(j)][maax+2]=[0.0,0.0,0.0,0.0]
    
    df['Unnamed: '+str(j)][maax+3]=[0.0,0.0,0.0,0.0]# last row empty

df.to_csv (r'DM_Template.csv',sep=';',encoding='utf-8',index=None)

