import pandas as pd
import numpy as np
import random
import re


df_raw = pd.read_csv('Arabic_names.csv')


all_names = list(df_raw['Name'].values)
male =df_raw[df_raw['Gender']=='M']['Name'].values
female = df_raw[df_raw['Gender']=='F']['Name'].values
all_char = list(set(re.findall(r'[\u0600-\u06FF]',str(all_names)))) +['']

choice  =[False,True,False,True,False,False]
def generate_negative_sample():
    
    names = []
    negative = 0
    for i in range(0,3):
        edit = random.choice(choice)
        idx = random.randint(0, len(all_names)-1)
        name = all_names[idx]
        print("Orignal name: ",name,edit)
    
        if edit:
            negative +=1
            char = random.randint(0, len(name)-1)
            noise_char = random.choice(all_char)
            name = list(name)
            name[char] = noise_char
            name = "".join(name)
        names.append(name)     
    if negative:
        return " ".join(names)
    else:
        return " "
 
def generate_positive_sample():
    
    gender = random.choice(['male','female'])
    name = []
    if gender == 'male':
        first = random.choice(male)
    else:
        first = random.choice(female)
    second = random.choice(male)
    last = random.choice(male)
    return first + ' ' + second + ' ' + last

       
negative_sample = []     
for i in range(0,23000):
    
        negative_sample.append(generate_negative_sample())
        
negative_sample = list(set(negative_sample))
negative_sample.remove(" ")


positive_sample = []     
for i in range(0,15500):
    
        positive_sample.append(generate_positive_sample())
        
positive_sample = list(set(positive_sample))

data = {'name':positive_sample + negative_sample,
        'status':list(np.ones(len(positive_sample))) + list(np.zeros(len(negative_sample)))}

df_1 = pd.DataFrame(data)

df_1 = df_1.sample(frac = 1)

df_1.to_csv('df_preprocces.csv')
