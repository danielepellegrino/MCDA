#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import numpy as np 

import random


# In[2]:


INPUT = pd.read_csv('DEF.csv',sep=";")

DM = int(INPUT['NUM'][0])

num_sim = int(INPUT['NUM'][1])

alternatives = int(INPUT['NUM'][4])

dms_weights = []

for i in range(DM):
    
    dms_weights.append(INPUT.iloc[2][i+1])
    
weights = str(tuple(dms_weights))


# In[3]:


def distance_alfa(d_tilde):
    
#     risk neutral
    
    a1 = d_tilde[0]
    a2 = d_tilde[1]
    a3 = d_tilde[2]
    a4 = d_tilde[3]
    
    result = ((a2+a3)/2)**2 +(1/3)*((a2+a3)/2)*((a4-a3)-(a2-a1))+(2/3)*((a3-a2)/2)**2+(1/9)*((a3-a2)/2)*((a4-a3)+(a2-a1))+(1/18)*((a4-a3)**2+(a2-a1)**2)-(1/18)*((a2-a1)*(a4-a3))
    
    return result


# In[4]:


def distance_one(d_tilde):
    
#     risk prone
    
    a1 = d_tilde[0]
    a2 = d_tilde[1]
    a3 = d_tilde[2]
    a4 = d_tilde[3]
    
    result = ((a2+a3)/2)**2+(1/2)*((a2+a3)/2)*((a4-a3)-(a2-a1))+(1/3)*(((a3-a2)/2)**2)+(1/6)*((a3-a2)/2)*((a4-a3)+(a2-a1))+(1/9)*((a4-a3)**2+(a2-a1)**2)-(1/9)*((a2-a1)*(a4-a3))
    
    return result


# In[5]:


def distance_alfa_2(d_tilde):
    
#     risk averse
    
    a1 = d_tilde[0]
    a2 = d_tilde[1]
    a3 = d_tilde[2]
    a4 = d_tilde[3]
    
    result = ((a2+a3)/2)**2+(1/4)*((a2+a3)/2)*((a4-a3)-(a2-a1))+ ((a3-a2)/2)**2 +(1/12)*((a3-a2)/2)*((a4-a3)+(a2-a1))-(1/144)*((a4-a3)**2+(a2-a1)**2)+(1/96)*((a2-a1)*(a4-a3))
    
    return result


# In[6]:


def dominance_intensity(d_tilde,f):
    
    a1 = d_tilde[0]
    a2 = d_tilde[1]
    a3 = d_tilde[2]
    a4 = d_tilde[3]
    
    if a4 < 0:
        
        dominance = -distance(d_tilde,f)

    elif a1 > 0:
        
        dominance = distance(d_tilde,f)
        
    elif a1 < 0 and a2 > 0:

        dominance = ((a2*(-a2+a3+a4)-a1*(a3+a4))/((a2-a1)*(a4+a3-a2-a1)))*distance(d_tilde,f)-((a1**2)/((a4+a3-a2-a1)*(a2-a1)))*distance(d_tilde,f)
        
    elif a3 < 0 and a4 > 0:

        dominance = ((a4**2)/((a4-a3)*(a4+a3-a2-a1)))*distance(d_tilde,f)-((a4*(a4-a2-a1)-a3*(a3-a2-a1))/((a4+a3-a2-a1)*(a4-a3)))*distance(d_tilde,f)
        
    elif a2 <0 and a3 > 0 :

        dominance = ((-a2-a1)/(a4+a3-a2-a1))*distance(d_tilde,f)-((a4+a3)/(a4+a3-a2-a1))*distance(d_tilde,f)
        
    else:
        
        dominance = 0
    
    return dominance


# In[7]:


def distance(d_tilde,f):
    
#     f = 0 Risk prone
#     f = 1 Risk neutral
#     f = 2 Risk averse
    
    if f == 0:
        
        result = distance_one(d_tilde)
        
    elif f == 1:
        
        result = distance_alfa(d_tilde)
        
    else:
        
        result = distance_alfa_2(d_tilde)
        
    return result


# In[8]:


for dm in range(DM):
    
    csv ="DM%s.csv"%(dm+1)
    
    txt ="results_DM%s.txt"%(dm+1)
    
    to_R_txt ="to_R_DM%s.txt"%(dm+1)
    
    to_R_csv ="to_R_DM%s.csv"%(dm+1)
    
    for num in range(num_sim):

        df = pd.read_csv(csv,sep=";")

        # Define Fuzzy Linguistic Scale
        VL = [0,0,0,0.05]              # Very Low 
        L  = [0,0.075,0.125,0.275]     # Low 
        SL = [0.125,0.275,0.325,0.475] # Slightly Low
        M  = [0.325,0.475,0.525,0.675] # Medium 
        SH = [0.525,0.675,0.725,0.875] # Slightly High
        H  = [0.725,0.875,0.925,1]     # High 
        VH = [0.925,1,1,1]             # Very High

        FLS = [VL, L, SL, M, SH, H, VH]

        # Linguistic scale length
        s = len(FLS)
        #print("s Linguistic scale = ", s)

        # Alternatives
        m = int(df['Num.'][1])
        #print("m Alternatives = ", m)

        # Attributes
        n = int(df['Num.'][0])
        #print("n Attributes = ", n)

        # -------------------------------------------------------------------------    

        for j in range(2,m+2):
            for i in range(n):
                res = []
                temp = []
                if df['Num.'][i+2] == 1: # ORDINAL
                    #print ("ordinal")
                    #print(df['Unnamed: '+str(j)][i+2]) 
                    a = df['Unnamed: '+str(j)][i+2]

                    # Convert String to tuple
                    # using loop + replace() + split()
                    if type(df['Unnamed: '+str(j)][i+2])==str:

                        for token in a.split(","):

                            num = int(token.replace("(", "").replace(")", ""))

                            temp.append(num)

                            if ")" in token:

                               res.append(temp)

                               temp = []

                        df['Unnamed: '+str(j)][i+2]=res.pop()

                    else:
                        df['Unnamed: '+str(j)][i+2]=0

                else:# TRAPEZOIDAL
        #             print ("trapez")
        #             print(df['Unnamed: '+str(j)][i+2])
                    a = df['Unnamed: '+str(j)][i+2]

                    # Convert String to list
                    # using loop + replace() + split()
                    for token in a.split(","):

                        num = float(token.replace("[", "").replace("]", ""))

                        temp.append(num)

                        if "]" in token:

                           res.append(temp)

                           temp = []

                    df['Unnamed: '+str(j)][i+2]=res.pop()  


        # -------------------------------------------------------------------------
        for j in range(2,n+2):

            res = []

            temp = []

            if df['Num.'][n+2] == 1: # ORDINAL
                #print ("ordinal")
                #print(df['Unnamed: '+str(j)][i+2]) 

                a = df['Unnamed: '+str(j)][n+2]

                # Convert String to tuple
                # using loop + replace() + split()
                if type(df['Unnamed: '+str(j)][n+2])==str:

                    for token in a.split(","):

                        num = int(token.replace("(", "").replace(")", ""))

                        temp.append(num)

                        if ")" in token:

                           res.append(temp)

                           temp = []

                    df['Unnamed: '+str(j)][n+2]=res.pop()

                else:
                    df['Unnamed: '+str(j)][n+2]=0

            else:# TRAPEZOIDAL
                #print ("trapez")
                #print(df['Unnamed: '+str(j)][i+2])
                a = df['Unnamed: '+str(j)][n+2]

                # Convert String to list
                # using loop + replace() + split()
                for token in a.split(","):

                    num = float(token.replace("[", "").replace("]", ""))

                    temp.append(num)

                    if "]" in token:

                       res.append(temp)

                       temp = []

                df['Unnamed: '+str(j)][n+2]=res.pop()    

        # -------------------------------------------------------------------------


        for i in range(n):
            bb = [0]*m
            tt = m
            z = s

            if df['Num.'][i+2] == 1: # ORDINAL
        #                 print ("ordinal")
        #                 print(df['Unnamed: '+str(j)][i+2]) 
                lst = df['Unnamed: 2'][i+2]
        #         print("lst: ", lst)

                # add original position
                data = list(enumerate(lst, start=1))
        #         print("data: ", data)

                # sort by value
                data = list(sorted(data, key=lambda x: x[1], reverse=True))
        #         print("data: ", data)

                # add sorted position
                data = list(enumerate(data, start=1))
        #         print("data: ", data)

                # resort to original order
                data = list(sorted(data, key=lambda x: x[1][0]))
        #         print("data: ", data)

                # extract sorted order number
                aa = [x[0] for x in data]
    #             print("rank: ", aa)

                while tt > 0:

                    for xx in aa:
    #                     print("xx: ",xx)
    #                     print("tt: ",tt)

                        if xx == tt:
                            z = random.choice(range(tt-1,z))

                            bb[aa.index(xx)]=z

                            aa[aa.index(xx)]=-1

                            tt = tt - 1

                for j in range(2,m+2):

                    df['Unnamed: '+str(j)][i+2]=FLS[bb[j-2]]

            else:
                aa = -1

    # -------------------------------------------------------------------------

        bb = [0]*n
        t = n
        z = s

        if df['Num.'][n+2] == 1: # ORDINAL
            #print ("ordinal")
            #print(df['Unnamed: '+str(j)][i+2]) 
            if n <= s:
                lst = df['Unnamed: 2'][n+2]
            #         print("lst: ", lst)

                # add original position
                data = list(enumerate(lst, start=1))
            #         print("data: ", data)

                # sort by value
                data = list(sorted(data, key=lambda x: x[1], reverse=True))
            #         print("data: ", data)

                # add sorted position
                data = list(enumerate(data, start=1))
            #         print("data: ", data)

                # resort to original order
                data = list(sorted(data, key=lambda x: x[1][0]))
            #         print("data: ", data)

                # extract sorted order number
                aa = [x[0] for x in data]
            #         print("rank: ", aa)
                while t > 0:
                    for xz in aa:

                        if xz == t:

                            z = random.choice(range(t-1,z))

                            bb[aa.index(xz)]=z

                            aa[aa.index(xz)]=-1

                            t = t - 1
                for j in range(2,n+2):
                    df['Unnamed: '+str(j)][n+2]=FLS[bb[j-2]]
            else:
                lst = df['Unnamed: 2'][n+2]
                #print("lst: ", lst)

                # add original position
                data = list(enumerate(lst, start=1))
                #print("data: ", data)

                # sort by value
                data = list(sorted(data, key=lambda x: x[1], reverse=True))
                #print("data: ", data)

                # add sorted position
                data = list(enumerate(data, start=1))
                #print("data: ", data)

                # resort to original order
                data = list(sorted(data, key=lambda x: x[1][0]))
                #print("data: ", data)

                # extract sorted order number
                aaa = [x[0] for x in data]
                #print("rank: ", aa)

                aa = []
                for l in aaa:
                    aa.append(round(abs(l*s/n-s/n*random.uniform(0, 1)-1)))

                for j in range(2,n+2):
                    df['Unnamed: '+str(j)][n+2]=FLS[aa[j-2]]


        else:
            aa = -1

    # -------------------------------------------------------------------------
        D1 = []
        D2 = []
        D3 = []
        D4 = []

        for i in range(n):

            for j in range(2,m+2):

                for k in range(2,m+2):

                    if k==j:

                        d1 = float("nan")
                        d2 = float("nan")
                        d3 = float("nan")
                        d4 = float("nan")

                        D1.append(d1)
                        D2.append(d2)
                        D3.append(d3)
                        D4.append(d4)
                    else:

                        d1 = df['Unnamed: '+str(j)][i+2][0]-df['Unnamed: '+str(k)][i+2][3]
                        d2 = df['Unnamed: '+str(j)][i+2][1]-df['Unnamed: '+str(k)][i+2][2]
                        d3 = df['Unnamed: '+str(j)][i+2][2]-df['Unnamed: '+str(k)][i+2][1]
                        d4 = df['Unnamed: '+str(j)][i+2][3]-df['Unnamed: '+str(k)][i+2][0]

                        D1.append(d1)
                        D2.append(d2)
                        D3.append(d3)
                        D4.append(d4)


        my_array1 = np.array(D1)
        my_array2 = np.array(D2)
        my_array3 = np.array(D3)
        my_array4 = np.array(D4)

        reshaped_array1 = my_array1.reshape(n,m,m)
        reshaped_array2 = my_array2.reshape(n,m,m)
        reshaped_array3 = my_array3.reshape(n,m,m)
        reshaped_array4 = my_array4.reshape(n,m,m)

        frame = df.to_numpy()


        DD1 = []
        DD2 = []
        DD3 = []
        DD4 = []

        for i in range(n):

            dd1 = frame[n+2][i+2][0]*reshaped_array1[i]
            dd2 = frame[n+2][i+2][1]*reshaped_array2[i]
            dd3 = frame[n+2][i+2][2]*reshaped_array3[i]
            dd4 = frame[n+2][i+2][3]*reshaped_array4[i]

            DD1.append(dd1)
            DD2.append(dd2)
            DD3.append(dd3)
            DD4.append(dd4)


        DDD1 = np.zeros((m, m))
        DDD2 = np.zeros((m, m))
        DDD3 = np.zeros((m, m))
        DDD4 = np.zeros((m, m))

        DDD01 = np.ones((m, m))*10
        DDD02 = np.ones((m, m))*10
        DDD03 = np.ones((m, m))*10
        DDD04 = np.ones((m, m))*10


        for k in range(m):

            DDD1=np.add(DDD1, DD1[k])
            DDD2=np.add(DDD2, DD2[k])
            DDD3=np.add(DDD3, DD3[k])
            DDD4=np.add(DDD4, DD4[k])


        AUX1=DDD1
        AUX2=DDD2
        AUX3=DDD3
        AUX4=DDD4

        DDD01 = np.minimum(DDD01,AUX1)
        DDD02 = np.minimum(DDD02,AUX2)
        DDD03 = np.minimum(DDD03,AUX3)
        DDD04 = np.minimum(DDD04,AUX4)


    Dominance = []

    for i in range(m):

        for j in range(m):

            Dominance.append([DDD01[i][j],DDD02[i][j],DDD03[i][j],DDD04[i][j]])

    Dominance = np.array(Dominance)

    Dominance = Dominance.reshape(m,m,4)

    I1 = np.zeros(m)
    I2 = np.zeros(m)
    I3 = np.zeros(m)
    I4 = np.zeros(m)

    for i in range(m):

        for j in range(m):

            if i!=j:

                I1[i] = I1[i]+DDD01[i][j]
                I2[i] = I2[i]+DDD02[i][j]
                I3[i] = I3[i]+DDD03[i][j]
                I4[i] = I4[i]+DDD04[i][j]

            else:

                aux = 0

    I = np.array([I1, I2, I3, I4]).T

    II = I.tolist()

    DI_prone = []
    for i in range(m):
        DI_prone.append(dominance_intensity(II[i],0))

    lst = DI_prone
    # print("lst: ", lst)

    # add original position
    data = list(enumerate(lst, start=1))
    # print("data: ", data)

    # sort by value
    data = list(sorted(data, key=lambda x: x[1], reverse=True))
    # print("data: ", data)

    # add sorted position
    data = list(enumerate(data, start=1))
    # print("data: ", data)

    # resort to original order
    data = list(sorted(data, key=lambda x: x[1][0]))
    # print("data: ", data)

    # extract sorted order number
    prone = [x[0] for x in data]
    # print("rank: ", prone)
    
    
    DI_averse = []
    for i in range(m):
        DI_averse.append(dominance_intensity(II[i],2))

    lst = DI_averse
    # print("lst: ", lst)

    # add original position
    data = list(enumerate(lst, start=1))
    # print("data: ", data)

    # sort by value
    data = list(sorted(data, key=lambda x: x[1], reverse=True))
    # print("data: ", data)

    # add sorted position
    data = list(enumerate(data, start=1))
    # print("data: ", data)

    # resort to original order
    data = list(sorted(data, key=lambda x: x[1][0]))
    # print("data: ", data)

    # extract sorted order number
    averse = [x[0] for x in data]
    # print("rank: ", averse)

    
    DI_neutral = []
    for i in range(m):
        DI_neutral.append(dominance_intensity(II[i],1))

    lst = DI_neutral
    # print("lst: ", lst)

    # add original position
    data = list(enumerate(lst, start=1))
    # print("data: ", data)

    # sort by value
    data = list(sorted(data, key=lambda x: x[1], reverse=True))
    # print("data: ", data)

    # add sorted position
    data = list(enumerate(data, start=1))
    # print("data: ", data)

    # resort to original order
    data = list(sorted(data, key=lambda x: x[1][0]))
    # print("data: ", data)

    # extract sorted order number
    neutral = [x[0] for x in data]
    # print("rank: ", neutral)



    f = open(txt, "w")

    f.write("---------------   -------    --------------\n")
    f.write("DOMINANCE MATRIX\n")
    f.write("---------------   -------    --------------\n")
    f.write(str(Dominance))

    f.write("\n---------------   -------    --------------\n")
    f.write("DOMINANCE INTENSITY\n")
    f.write("---------------   -------    --------------\n")
    f.write(str(II))

    f.write("\n---------------   -------    --------------\n")
    f.write("PRONE\n")
    f.write("---------------   -------    --------------\n")
    for i in range(len(prone)):
        f.write("Alternative: %s    rank: %s    value: %s\n" %((i+1),prone[i],round(data[i][1][1],4)))

    f.write("---------------   -------    --------------\n")
    f.write("NEUTRAL\n")
    f.write("---------------   -------    --------------\n")
    for i in range(len(neutral)):
        f.write("Alternative: %s    rank: %s    value: %s\n" %((i+1),neutral[i],round(data[i][1][1],4)))

    f.write("---------------   -------    --------------\n")  
    f.write("AVERSE\n")
    f.write("---------------   -------    --------------\n")
    for i in range(len(averse)):
        f.write("Alternative: %s    rank: %s    value: %s\n" %((i+1),averse[i],round(data[i][1][1],4)))

    f.close()
    
    f = open(to_R_txt, "w")
    
    f.write("Alternative Rank Value\n")
    
    for i in range(len(neutral)):
        f.write("A%s %s %s\n" %((i+1),neutral[i],round(data[i][1][1],4)))

    f.close()
    
    read_file = pd.read_csv (r'to_R_DM%s.txt'%(dm+1),sep=' ')
    read_file = read_file.sort_values(by=['Rank'])
    read_file.to_csv (r'to_R_DM%s.csv'%(dm+1),sep=';',encoding='utf-8',index=None)


# In[9]:


f = open("code_to_R.txt", "w")

f.write("\n")
f.write("# Call library\n")
f.write("\n")
f.write("library(RankAggreg)\n")


f.write("\n")
f.write("# DMs' weights\n")
f.write("\n")
f.write("y <- c"+weights+"\n")


f.write("\n")
f.write("# DMs' alternatives ranked\n")
f.write("\n")
f.write("x <- matrix(c(\n")
for i in range(DM-1):
    df2 = pd.read_csv("to_R_DM%s.csv"%(i+1),sep=";")
    for j in range(alternatives):
        f.write("'"+df2['Alternative'][j]+"',")
    f.write("\n")  
df2 = pd.read_csv("to_R_DM%s.csv"%(DM),sep=";") 
for j in range(alternatives-1):
    f.write("'"+df2['Alternative'][j]+"',")
    
f.write("'"+df2['Alternative'][alternatives-1]+"'")
f.write("), byrow=TRUE, ncol=%s)\n"%alternatives)

f.write("\n")
f.write("# DMs' rankings' values\n")
f.write("\n")
f.write("c <- matrix(c(\n")
for i in range(DM-1):
    df2 = pd.read_csv("to_R_DM%s.csv"%(i+1),sep=";")
    for j in range(alternatives):
        f.write(str(df2['Value'][j])+",")
    f.write("\n")  
df2 = pd.read_csv("to_R_DM%s.csv"%(DM),sep=";") 
for j in range(alternatives-1):
    f.write(str(df2['Value'][j])+",")
    
f.write(str(df2['Value'][alternatives-1]))
f.write("), byrow=TRUE, ncol=%s)\n"%alternatives)



f.write("\n")
f.write("# using the Cross-Entropy Monte-Carlo algorithm\n")
f.write("\n")
f.write("(CES <- RankAggreg(x, %s, c, 'CE',importance = y, 'Spearman', rho=.1, N=100, convIn=7))\n"%alternatives)
f.write("plot(CES)\n")
f.write("\n")
f.write("(CEK <- RankAggreg(x, %s, c, 'CE',importance = y, 'Kendall', rho=.1, N=100, convIn=7))\n"%alternatives)
f.write("plot(CEK)\n")
f.write("\n")

f.write("# using the Genetic algorithm\n")
f.write("\n")
f.write("(GAS <- RankAggreg(x, %s, c, 'GA',importance = y, 'Spearman'))\n"%alternatives)
f.write("plot(GAS)\n")
f.write("\n")
f.write("(GAK <- RankAggreg(x, %s, c, 'GA',importance = y, 'Kendall'))\n"%alternatives)
f.write("plot(GAK)\n")
f.write("\n")




f.close()

