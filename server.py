from fastapi import FastAPI
import uvicorn

# from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import load_model
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import pickle
import re
import json
import time
TOKENIZER_PATH =  r'tokenizer.pkl'
MODEL_PATH =  r'name.h5'

# Getting back the objects:
with open(TOKENIZER_PATH,'rb') as f:  # Python 3: open(..., 'rb')
    tokenizer = pickle.load(f)
    
model = load_model(MODEL_PATH)

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text

app = FastAPI()



result = 0
x = 0
name = ''
@app.get("/")
def get_name(name):
    
    name = str.strip(name)
    if len(name.split()) >= 3: #check lenght of name
        t1 = time.process_time() #start time
        x = tokenizer.texts_to_sequences(normalize_arabic(name).split("-*-"))
        x = pad_sequences(x, padding='post',maxlen=3,truncating='post')
        result = model.predict(x)[0][0] #model inference
        t2 = time.process_time() #end time
        inference_time = t2 - t1 #Compute inferance time
        message = ''
        if result >= 0.75:
            message = "Valid"
        else:
            message = "Not Valid"
        
        d = {"name":name,"confidence":str(result),"result":message,
             "inference_time":str(round(inference_time,4))+" Second"}#
        return JSONResponse(d)

    else:
        return "Sorry!! You can only input 3 names"
    # print("YES")
    # if result[0] >=50:
    #     return 2
    # else:
    #     return 0





if __name__ == "__main__":
    uvicorn.run(f"server:app", reload=True, host="0.0.0.0", port=8080)
