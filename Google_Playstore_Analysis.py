#!/usr/bin/env python
# coding: utf-8

# #### importing libraries

# In[1]:


import pandas as pd  # pandas: data manipulation and analysis library
import numpy as np  # numpy: numerical computing library providing support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions
import seaborn as sns  # seaborn: data visualization library based on matplotlib, providing a high-level interface 
import matplotlib.pyplot as plt # matplotlib: 2D plotting library for creating static, interactive, and animated visualizations in Python
import missingno as msno # missingno: data visualization library for visualizing missing data patterns in datasets


# #### loading data and explore  values

# In[2]:


df = pd.read_csv("C:\\Users\\midoo\\googleplaystore.csv")
df.head()


# #### explore #_rows,#_null values,datatypes of columns

# In[3]:


df.info()
df[df['Reviews'].str.contains('M')]


# ## Data Cleaning

# ### 1. Which of the following column(s) has/have null values?

# #### quick visualization by missingno library
# 

# In[4]:


# Visualize missing values in each column using the missingno library, with a plot size of 10x6 inches.
msno.bar(df, figsize=(10, 6)) 
# Set the title of the plot to 'Missing Values in Each Column'.
plt.title('Missing Values in Each Column')  
# Set the label for the x-axis to 'Column_name', indicating the name of the columns in the DataFrame.
plt.xlabel('Column_name')  
# Set the label for the y-axis to 'Count of Missing Values', indicating the number of missing values in each column.
plt.ylabel('Count of Missing Values')  
# Display the plot.
plt.show() 


# In[5]:


#Highlighting columns with missing data by using isnull func to indicate null values along column axis by any func
df.columns[df.isnull().any(axis=0)]
#another approach 
#using isna func to bring null values in columns and get # of null values
df.isna().sum()


# #### Remove the invalid values from Rating (if any). Just set them as NaN.

# ##### let's use histogram to see invalid values

# In[6]:


df['Rating'].plot(kind='hist')
#as we know the rating range between (1,5) but we see there are values more than 5 so we must replace it with nan


# In[7]:


# we can see that there are values like 19 which is outlires
df.describe()


# In[8]:


#replace any value in rating column with nan by using mask method allows you to selectively replace values in a 
#DataFrame based on a condition, while leaving other values unchanged
df['Rating'] = df['Rating'].mask(df['Rating'] > 5, np.nan)
#another appraoch 
# based on condition rating>5 replace value in rating column with nan
df.loc[df['Rating']>5,'Rating']=np.nan


# #### visuallize result

# In[9]:


df['Rating'].plot(kind='hist')
# as we can see the values between (1,5)


# In[10]:


df.describe()
# checking min and max values which now are valid values


# #### Fill the null values in the Rating column using the mean()
# 

# In[11]:


#calculate the mean of rating column by neglect any null values 
mean=df['Rating'].mean()
#replace any nan value with mean in rating column
df['Rating']=df['Rating'].replace(np.nan, mean)


# #### visualize result

# In[12]:


#check the # of null value in rating which is done
msno.bar(df, figsize=(10, 6)) 


# #### Clean any other non-numerical columns by just dropping the values

# In[13]:


# select all rows along row axis contain at least one null value and reverse the answer 
df=df[~df.isnull().any(axis=1)]
#another approach 
df.dropna(inplace=True)
# as we can see we get only the row which have only none null values
msno.bar(df, figsize=(10, 6)) 


# In[14]:


#another check for the null values
df.isna().sum()


# ### 2. Clean the column Reviews and make it numeric

# In[15]:


#we want to see if there are any value have character so we will neglect errors parameter to see where error pattern
#as we see from error there is character M add at the end of the value so we will explore it 
#df['rev'] = pd.to_numeric(df['Reviews'] )
#df[df['Reviews'].str.contains('M')]
#we will add new column 'rev' and pass errors as coerce to converts non-convertible data into NaN (Not a Number) values.
df['rev'] = pd.to_numeric(df['Reviews'],errors='coerce').astype('Int64')
#so any rev column have null value because non-convertible data
#df[df['rev'].isnull()]
#we will solve it by convert any M by multiplying it with 1000000 by bring nan in rev and split num until space ,convert it 
# to float and multiplying it with 1000000
df.loc[df['rev'].isnull(),'rev']=(df['Reviews'].str.split(' ').str[0]).astype(float )*1000000
#check if it is done and it work properly we convert M to 1000000
df[df['Reviews'].str.contains('M')]


# ### 3. How many duplicated apps are there?

# In[16]:


#he asks for duplicated apps not dupliacated rows there are difference in the answer 
#we bring duplicated app and set keep to false to bring all duplicated
df[df.duplicated(subset=['App'],keep=False)].shape


# ### 4. Drop duplicated apps keeping the ones with the greatest number of reviews

# In[17]:


df.sort_values(by=['App','rev'],ascending=False,inplace=True)
df.drop_duplicates(subset='App', keep='first',inplace=True)
df.head()


# ### 5. Format the Category column

# #### Categories are all uppercase and words are separated using underscores. Instead, we want them with capitalized in the first character and the underscores transformed as whitespaces.

# In[18]:


#we notice that there is 1.9 in category we will convert it into unknown
df['Category'].value_counts()


# In[19]:


#replace 1.9 with unknown by str.replace 
df['Category'] = df['Category'].str.replace('1.9', 'Unknown')
#replace any underscore with whitespace 
df['Category'] = df['Category'].str.replace('_', ' ')
#capitalize first letter only 
df['Category'] = df['Category'].str.capitalize()
#check the formatted column 
df['Category'].value_counts()


# #### 6. Clean and convert the Installs column to numeric type

# In[20]:


df.head()
#we must replace + sign and , with wihtespace to easily convert it as numeric easily


# In[21]:


#as we see replace + sign and , with wihtespace 
df['Installs']=df['Installs'].str.replace(',','').str.replace('+','')
df.head()


# In[22]:


# we easily convert column into numeric easily
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
df.info()


# #### 7. Clean and convert the Size column to numeric (representing bytes)

# In[28]:


df.head(50)
#we notice that we have M refer to mega and k refer to kilo so we must replace M with 1024*1024 byte and kilo with 1024 byte
pd.to_numeric(df['Size'].str.replace('M','').str.replace('k',''))
#we get this error "Unable to parse string "Varies with device" at position 6 so we have a pure string 
#that is impossible to be replaced so we will convert it to 0 let's see how many if this value
df[df['Size']=="Varies with device"].count()
#we have about 1227 occurance of this string 
#we will convert it to 0
df['Size'] = df['Size'].replace('Varies with device', "0").astype(str)
# df.loc[df['Size'].str.contains('k'), 'Size']: Selects the values from the 'Size' column of the DataFrame df where the 'Size' values contain the letter 'k'.
#.str.replace('k', ''): Removes the letter 'k' from the selected values.
#pd.to_numeric(...): Converts the resulting strings into numeric values.
#* 1024: Multiplies the numeric values by 1024, presumably converting kilobytes to bytes.
#.astype(str): This converts the resulting numeric values (presumably in bytes) back to strings.
new_value = (pd.to_numeric(
    df.loc[df['Size'].str.contains('M'), 'Size'].str.replace('M', '')
) * (1024 * 1024)).astype(str)
df.loc[df['Size'].str.contains('M'), 'Size'] = new_value

# Transform `k` to ~1k bytes
new_value = (pd.to_numeric(
    df.loc[df['Size'].str.contains('k'), 'Size'].str.replace('k', '')
) * 1024).astype(str)
df.loc[df['Size'].str.contains('k'), 'Size'] = new_value

# Get rid of `+` and `,`
df['Size'] = df['Size'].str.replace('+', '')
df['Size'] = df['Size'].str.replace(',', '')

# Finally transform to numeric:
df['Size'] = pd.to_numeric(df['Size'])
df.head(50)


# #### 8. Clean and convert the Price column to numeric

# In[29]:


#we notice that paid app it's price has $sign and ,  so we must  first remove $ first and replace , with .
df['Price']=df['Price'].str.replace('$','').str.replace(',', '.')
# we face this error when we want to convert Unable to parse string "Everyone" at position 3850
#we convert this value with 0
df.loc[df['Price']=="Everyone",'Price']='0'
df['Price'] = pd.to_numeric(df['Price'])
df.head(50)


# #### 9. Paid or free?

# In[30]:


#creating new column Distribution if price >0 then paid otherwise Free by using apply and lambda function
df['Distribution'] = df['Price'].apply(lambda x: 'Paid' if x > 0 else 'Free')
df
#along time with cleaning 


# ## Analysis

# ### 10. Which app has the most reviews?

# In[126]:


#we get the maximum rev and bring the corresponding one 
df[df['rev']==df['rev'].max()]
#another approach sort_values by # of rev by dec 
res1=df[df['Category']=='Social'][['App', 'rev']].sort_values(by=['rev'], ascending=False).head(10)
res1


# In[115]:


plt.figure(figsize=(10, 6))  # Creates a new figure with a specified size.
plt.bar(res1['App'], res1['rev'], color='skyblue')  # Plots a bar chart with 'App' on x-axis and 'rev' on y-axis, using sky blue color.
plt.xlabel('App')  # Sets the label for the x-axis.
plt.ylabel('Number of Reviews')  # Sets the label for the y-axis.
plt.title('Top 5 Apps with the Most Reviews')  # Sets the title for the plot.
plt.xticks(rotation=90)  # Rotates the x-axis labels by 90 degrees for better readability.
plt.show()  # Displays the plot.


# #### interpreting the vizuallization

# In[133]:


#as we see there are gap between # of reviews between(facebook,instgram) and other top 8 social media apps 
# my hypothesis the # of installs play important role in this explination ,i see there is correlation between this two 
# variables # of reviews and # number of installs we will see and check for this 


# In[132]:


# bring data only related to social category 
res2=df[df['Category']=='Social']
correlation_matrix = res2.corr()  # Calculate the correlation matrix for the DataFrame 'res2'.
plt.figure(figsize=(8, 6))  # Create a new figure for the heatmap with a specified size of 8x6 inches.
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")  # Create a heatmap with Seaborn.
plt.title('Correlation Heatmap')  # Add a title to the heatmap.
plt.show()# Show the plot


# In[ ]:


#The correlation coefficient of 0.83 suggests a strong linear relationship and positve correlation between the variables
# As installs variable increases, the rev tends to increase as well, and vice versa.
#so our assumption is that if # of installs increase ,# of reviews increase  


# #### 11. What category has the highest number of apps uploaded to the store?

# In[154]:


res3=df['Category'].value_counts().reset_index(name='num').head(10)
res3


# In[152]:


plt.figure(figsize=(10, 6))  # Creates a new figure with a specified size.
plt.bar(res3['index'], res3['num'], color='skyblue')  # Plots a bar chart with 'App' on x-axis and 'rev' on y-axis, using sky blue color.
plt.xlabel('category')  # Sets the label for the x-axis.
plt.ylabel('Number of category')  # Sets the label for the y-axis.
plt.title('Top 10 categories with the Most frequent')  # Sets the title for the plot.
plt.xticks(rotation=90)  # Rotates the x-axis labels by 90 degrees for better readability.
plt.show()  # Displays the plot.


# #### interpreting the vizuallization

# In[ ]:


#we notice that occurance of family apps is double second highest category 'Game' why this whole gap 
#Family category may encompass a broad range of apps designed for families, here are seven specific subcategories or types of apps that might fall under the "Family" category
#Educational Apps for Kids,Entertainment for All Ages,Family Communication and Messaging,Health and Wellness,Travel and Leisure
#App Store Policies and Guidelines: App store policies and guidelines may influence developers' decisions to categorize 
#their apps. Developers may strategically choose the "Family" category for their apps to reach a broader audience 
#or to comply with content guidelines related to family-friendly content.
#Competition and Developer Focus: The competitive landscape within the "Family" category may also play a role.
#Developers may perceive the "Family" category  more lucrative, leading to a higher concentration of apps in this category.
#Monetization Strategies: The "Family" category may offer opportunities for developers to monetize their apps through various means
#such as subscription services, in-app purchases, or advertising targeted at families. 
#The potential for higher revenue streams may incentivize developers to prioritize the development and release of apps in this category.
#family category has all different ages so wide range of users ,so possibility to gain money more higher than other categories


# #### 12. To which category belongs the most expensive app?

# In[166]:


# filtering the DataFrame to find rows where the price matches the maximum price and then selecting the 'Category' column from these rows.
#df[df['Price']==df['Price'].max()][['Category']]
#another approach 
#sorting the rows by price column in descending order
df.sort_values(by='Price', ascending=False)[['App','Category','Price']].head(10)
# we notice that top 10  most expensive lies between  finance and lifestyle category  
#that because  Apps categorized under Finance typically appeal to individuals interested in wealth management
#investment, and financial success. The pricing of these apps may be justified by their purported ability to provide 
#financial insights, tools, or services that help users manage their money, make informed investment decisions, or achieve financial goals. 
#The high prices in this category may be perceived as an investment in one's financial future or a sign of commitment to financial responsibility
#: Apps categorized under Lifestyle often cater to personal interests, preferences,
#or aspirations beyond financial considerations. The pricing of these apps may be driven by factors such as exclusivity
#, luxury, status, or personal branding. Consumers purchasing apps in this category may be motivated by the desire to
#signal affluence, indulge in luxury, or simply own a rare or unique item. The high prices in this category may be perceived as a statement of personal style, taste, or identity..


# #### 13. What's the name of the most expensive game?

# In[38]:


#filter rows by Game category and sort them by price in ascedning order 
b=df[df['Category']=='Game'].sort_values(by='Price', ascending=False).head()


# #### 14. Which is the most popular Finance App?

# In[39]:


df[df['Category']=='Finance'].sort_values(by='Installs', ascending=False).head()


# #### 15. What Teen Game has the most reviews?

# In[44]:


#filter Content Rating with teen and Category with Game and sort by reviews decending 
df[(df['Content Rating']=='Teen')& (df['Category']=='Game')].sort_values(by='rev', ascending=False).head()


# #### 16. Which is the free game with the most reviews?

# In[45]:


#filter distibution with Free and Category with Game and sort by reviews decending 
df[(df['Distribution']=='Free')& (df['Category']=='Game')].sort_values(by='rev', ascending=False).head()


# #### 17. How many Tb (tebibytes) were transferred (overall) for the most popular Lifestyle app?¶

# In[54]:


#sort by # of installs in category of life style and get the maximum # of installs
m_l=df[df['Category']=='Lifestyle'].sort_values(by='Installs', ascending=False).head(1)
#total transfer by #_installs*size and convert the value from bytes into TB by transfer from byte to kilo to mega to giga to TB
res=(m_l['Installs']*m_l['Size'])/(1024*1024*1024*1024)
res


# In[ ]:




