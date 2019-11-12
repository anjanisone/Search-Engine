import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from nltk.corpus import stopwords
import glob, os
import PyPDF2
import json
import requests


print("Reached First Point")



print("Reached Main Function")
if __name__ == "__main__":

    def readfiles(file):
        file = open(file,'rb')
        reader = PyPDF2.PdfFileReader(file)
        eachPageText=[]
        for i in range(0,reader.getNumPages()):
            pageText = reader.getPage(i).extractText()
            eachPageText.append(pageText)
            output =  '\n '.join(eachPageText)
            output = output.lower()
            output = output.replace("\n"," ")
        return output

    def get_filename(file):
        print(file)
        return file.split(".")[0]


    def get_extension(file):
        print(file)
        return file.split(".")[1]

    count = 1
    for file in glob.glob("dataset/*.pdf"):
        title = get_filename(file)
        file_type = get_extension(file)
        text = readfiles(file)

        print("Title: ", title)
        print("file_type",file_type)
        print("Text",text)
        post_url = "http://localhost:9200/hacker/files"
        post_autocomplete_url = "http://localhost:9200/autocomplete/text"

        payload = {
            "text":text,
            "title": title,
            "filetype": file_type
        }
        payload_autocomplete = {
            "text":text,
            "text_suggest": text
        }
        headers = {
            "Content-Type": "application/json",
            "cache-control": "no-cache"
        }

        payload = json.dumps(payload)
        payload_autocomplete = json.dumps(payload_autocomplete)
        response = requests.request("POST",post_url,data=payload, headers=headers)

        response_autocomplete = requests.request("POST",post_autocomplete_url,data=payload_autocomplete,headers=headers)

        if (response.status_code == 201):
            print("Values Posted in Hacker Index")
        if (response_autocomplete.status_code == 201):
            print("Values Posted in autocomplete index")

        print("----------------", count, "----------------------")
        count = count + 1
        
