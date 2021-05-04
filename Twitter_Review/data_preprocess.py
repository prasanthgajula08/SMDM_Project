#!/usr/bin/env python
# coding: utf-8

# In[39]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import warnings
warnings.filterwarnings('ignore')
import statsmodels.api as sm
from statsmodels.formula.api import ols


# In[4]:


data = pd.read_excel('Ave_endGame1.xlsx')


# In[5]:


data.head(10)


# In[8]:


data.sort_values(["likes_count"], axis=0,
                 ascending=False, inplace=True)


# In[9]:


data.head(10)


# In[11]:


data.info()


# In[58]:


missing_val = pd.DataFrame(data.isnull().sum())
missing_val = (missing_val/len(data))*100
missing_val.reset_index()

missing_val = missing_val.rename(columns = {'index': 'Variables', 0: 'Missing_percent'})
missing_val


# In[37]:


data=data.dropna(subset=['Tweet'])
data=data.dropna(subset=['Username'])
data.info()


# In[64]:


data['location']=data['location'].astype('category')
data['verified']=data['verified'].astype('category')
data['Datetime'] = pd.to_datetime(data['Datetime'])


# In[61]:


data['location'].loc[99]
data = data.fillna(data['location'].value_counts().index[0])
data['location'].loc[99]


# In[65]:


import datetime
data['year'] = data['Datetime'].dt.year
data['month'] = data['Datetime'].dt.month
data['day'] = data['Datetime'].dt.day
data['hour'] = data['Datetime'].dt.hour


# In[69]:


cnames = ['followers','friends','statuses','favourites']
corr = data.loc[:,cnames]
#Set the width and hieght of the plot
f, ax = plt.subplots(figsize=(7, 5))

#Generate correlation matrix
corr1 = corr.corr()

#Plot using seaborn library
sns.heatmap(corr1, mask=np.zeros_like(corr1, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)


# In[82]:


data.to_csv('Final_data.csv')


# In[ ]:




