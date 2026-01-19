#!/usr/bin/env python
# coding: utf-8

# In[1]:


example = {"key1":"Value1", "key2":"Value2"}


# In[2]:


example["key1"]


# In[ ]:


example.key1   ## This is not supported in dictionary


# Inorder to make this support in the above way we do following :

# In[1]:


from box import ConfigBox


# In[2]:


example = ConfigBox({"key1":"Value1", "key2":"Value2"})
example.key1  ## Now u will be able to get the value


# Config box even in dictionary provides us this specific feature , if u have any keys u can directly call that particular key and get the value.
# This is used just to bring some easyness , bcoz we have here lot of yaml files and each and every yaml file will have values and we will be defining all our values in key value pair(dictionary) , so whenever we have in key-value pair i should be able to probably call this directly by using keys , so we are using ConfigBox.

# In[3]:


## Explanation is for ensure annotation
def get_product(x:int,y:int) -> int:
    return x*y


# In[4]:


get_product(2,2)


# In[ ]:


get_product(2,"4") ## 4 is a string multiply by 2 times its giving double 4
## Here the situation is differnt data type passed , now we want even if string is passed it should be considered as an integer.
## Or it should give as a exception


# In[6]:


from ensure import ensure_annotations

@ensure_annotations  ## Written as a decorator
def get_product(x:int,y:int) -> int:
    return x*y


# In[ ]:


get_product(2,"4")  
## Here it will throw a error , so with ensure annotation we are making it strict like whatever is my datatype that we are expecting that should be given over here.

