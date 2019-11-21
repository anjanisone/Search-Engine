# -*- coding: utf-8 -*-
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from nltk.corpus import stopwords
import glob, os
import PyPDF2
import json
import requests
import re
import spacy
import sys

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
        
    def listToString(s):
        str1 = ""
        for ele in s:
            str1 += ele+" "
        return str1


    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        return filtered_sentence
    
    def remove(list):
        pattern = '[0-9]'
        list = [re.sub(pattern,"",i) for i in list]
        return list
    
    def clean(text):
        output = text.replace("-","")
        output = output.replace("..","")
        output = output.replace("...","")
        output = output.replace(". .","")
        output = output.replace(". . .","")
        output = output.replace("/","")
        output = output.replace("(  )","")
        output = output.replace("q      q","")
        output = output.replace("q . q","")
        output = output.replace("q  q","")
        output = output.replace("q    q","")
        output = output.replace("(","")
        output = output.replace(")","")
        output = output.replace("."," ")
        output = output.replace("&","")
        output = output.replace(":","")
        output = output.replace("=","")
        output = output.replace(",","")
        output = output.replace(".","")
        output = output.replace("_","")
        output = output.replace('"',"")
        output = output.replace("@","")
        output = output.replace("'","")
        output = output.replace("~","")
        output = output.replace("`","")
        output = output.replace("^","")
        output = output.replace("!","")
        output = output.replace("#","")
        output = output.replace("$","")
        output = output.replace("%","")
        output = output.replace("*","")
        output = output.replace("-","")
        output = output.replace("+","")
        output = output.replace("ˆ","")
        output = output.replace("˙","")
        output = output.replace("?","")
        output = output.replace("<","")
        output = output.replace(">","")
        output = output.replace("/","")
        output = output.replace("{","")
        output = output.replace("}","")
        output = output.replace(";","")
        output = output.replace(":","")
        output = output.replace("'","")
        output = output.replace("[","")
        output = output.replace("]","")
        output = output.replace("{","")
        output = output.replace("}","")
        output = output.replace("=","")
        return output

    def remove_duplicates(list):
        final_list = []
        for word in list:
            if word not in final_list:
                final_list.append(word)
        return final_list
    
    def get_only_nouns(text):
        _nlp = spacy.load('en_core_web_sm')
        all_prompts = []
        doc = _nlp(text)
        def certain_conditions(prompt):
            return True

        for token in doc.noun_chunks:
            prompt = token.text
            if certain_conditions(prompt = prompt):
                all_prompts.append(prompt)
        return listToString(all_prompts)
    
    
    def get_4grams(text):
        list_with_nostopwords = remove_stopwords(text)
        list_no_sw_no_numbers = remove(list_with_nostopwords)
        string_no_sw_no_numbers = listToString(list_no_sw_no_numbers)
        clean_string_no_sw_no_numbers = clean(string_no_sw_no_numbers)
        token = nltk.word_tokenize(clean_string_no_sw_no_numbers)
        fourgram = nltk.ngrams(token, n=4)
        new_list = list(fourgram)
        output_list = []
        for  i in range(len(new_list)):
            new_list[i] = list(new_list[i])
            new_list[i] = listToString(new_list[i])
            output_list.append(new_list[i])
        return output_list





    def get_extension(file):
        return file.split(".")[1]

    count = 1
    os.chdir("pdfs/")
    for file in glob.glob("*.pdf"):
        title = get_filename(file)
        file_type = get_extension(file)
        text = readfiles(file)
        fourgram_list = get_4grams(text)
        ngram_list = remove_duplicates(fourgram_list)
        print(len(ngram_list))
        print("Title: "+ title)
        print("file_type"+file_type)
        print("Text"+text)
        post_url = "http://localhost:9200/hacker/files"
        post_autocomplete_url = "http://localhost:9200/autocomplete/text"

        payload = {
            "text":text,
            "title": title,
            "filetype": file_type
        }
        
        headers = {
            "Content-Type": "application/json",
            "cache-control": "no-cache"
        }
        payload = json.dumps(payload)
        response = requests.request("POST",post_url,data=payload, headers=headers)

        for ngram in range(len(fourgram_list)):
            ngram_based_suggestion = fourgram_list[ngram]
            payload_autocomplete = {
            "text": ngram_based_suggestion,
            "text_suggest": ngram_based_suggestion
            }
            payload_autocomplete = json.dumps(payload_autocomplete)
            response_autocomplete = requests.request("POST",post_autocomplete_url,data=payload_autocomplete,headers=headers)

            if (response.status_code == 201):
                print("Values Posted in Hacker Index")
            if (response_autocomplete.status_code == 201):
                print("Values Posted in autocomplete index")

            print("----------------", count, "----------------------")
            count = count + 1