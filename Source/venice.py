# Author Stephen Witty switty@level500.com
# Test harness for venice.ai prompts
#
# V1 8-23-25 - Initial release

import http.client
import time
import sys
import os
import random
import requests

# Venice key
key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# AI model below
ai_model="venice-uncensored" # venice.ai  model

###################### Constants ##########################################################
NUMBER_OF_CYCLES = 20         # Number of cycles to run before exiting
AI_RETRY_LIMIT = 25           # Number of times to retry AI if errors occur

####### Appends text to the end of a file ###########
def write_to_file(filename, text):
   try:
      with open(filename, 'a') as f:
         f.write(text)
   except Exception as e:
      print(f"An error occurred: {e}")
      sys.exit()

########### This function formats an output string ####################
def print_string(string):
   cnt = 0
   for char in string:
      print(char, end = "")
      cnt = cnt + 1

      if (char=="\n" or char=="\r"):
         cnt = 0

      if (cnt > 80 and char == " "):
         print()
         cnt = 0
   print()
   sys.stdout.flush()

########## This function calls venice.ai ###########
def call_ai(prompt_message):
   try:

      URL = "https://api.venice.ai/api/v1/chat/completions"

      headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
      }

      payload = {
         "model": ai_model,
         "messages": [
         {
            "role": "system",
            "content": "You are a helpful assistant"
         },
         {
            "role": "user",
            "content": prompt_txt
         }
      ],
      "venice_parameters": {
      "enable_web_search": "on",
      "include_venice_system_prompt": True
      },
      "frequency_penalty": 0,
      "presence_penalty": 0,
      "max_tokens": 1000,
      "max_completion_tokens": 998,
      "temperature": 1,
      "top_p": 0.1,
      "stream": False
      }

      resp = requests.post(URL, json=payload, headers=headers, timeout=60)
      resp.raise_for_status()
      data = resp.json()

      response = data["choices"][0]["message"]["content"]

   except Exception as e:
      return False, "", "WARNING:  System Error during AI api  call: " + str(e)

   return True, response, ""

###############  Start of main routine ##############################################################
number_of_cycles = 0
ai_errors = 0

# Read in the prompt from a file
try:
   with open('prompt.txt', 'r', encoding='utf-8') as file:
      prompt_txt = file.read()
except Exception as e:
   print(f"An error occurred: {e}")
   sys.exit()

print("Starting........")
print("Prompt:")
print_string(prompt_txt)
print("Model: " + ai_model)
print("------------------------\n\n")

while(number_of_cycles < NUMBER_OF_CYCLES): # Main loop to run prompts

   retry_count = 0
   success = False # Keep running prompt until we get a valid answer to check

   while (not success):

      if (retry_count == AI_RETRY_LIMIT):
         print("\n\nERROR: Too many AI errors, exiting\n")
         sys.exit()

      success, ai_reply, error_text = call_ai(prompt_txt) # Call AI, retry if error
      if (not success):
         print(error_text)
         retry_count = retry_count + 1
         ai_errors = ai_errors + 1
         continue

      print("***** Answer number: " + str(number_of_cycles + 1) + " ****************************\n")
      print_string(ai_reply)
      print("\n")

      write_to_file("answer.txt","\n\n\n******** Answer number: " + str(number_of_cycles + 1) + " ************\n\n")
      write_to_file("answer.txt",ai_reply)

# back to main outside loop 
   number_of_cycles = number_of_cycles + 1

print("\n----------- Final report -------------- ")
print("AI Prompt:")
print_string(prompt_txt)
print("AI model: " + ai_model)

print("\nNumber of cycles: " + str(number_of_cycles))
print("AI Errors: " + str(ai_errors))
