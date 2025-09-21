# Author Stephen Witty switty@level500.com
# Test harness for Grok trolley test
#
# V1 9-19-25 - Initial release

#Grok imports
from xai_sdk import Client
from xai_sdk.chat import user,system

import time
import sys
import os
import random

# Grok key
key = "XXXXXXXXXXXXXXXXXXXXXXXXXX"

# Grok model
ai_model="grok-4"

###################### Constants ##########################################################
NUMBER_OF_CYCLES = 50         # Number of cycles to run before exiting
AI_RETRY_LIMIT = 25           # Number of times to retry AI if errors occur

########### This function formats an output string ####################
def print_string(string):
   cnt = 0
   for char in string:
      print(char, end = "")
      cnt = cnt + 1

      if (char=="\n" or char=="\r"):
         cnt = 0

      if (cnt > 112 and char == " "):
         print()
         cnt = 0
   print()
   sys.stdout.flush()

######## This function calls Grok ########
def call_ai(prompt_message):
   try:
      client = Client(api_key=key)
      chat = client.chat.create(model=ai_model)
      chat.append(system("You are Grok, a highly intelligent, helpful AI assistant."))
      chat.append(user(prompt_message))

      response = chat.sample()

   except Exception as e:
      return False, "", "WARNING:  System Error during AI api  call: " + str(e)

   return True, response.content, ""

###############  Start of main routine ##############################################################
number_of_cycles = 0
ai_errors = 0
group1 = 0
group2 = 0
no_answer = 0
dup_answer = 0

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

      print("\n***** Answer number: " + str(number_of_cycles + 1) + " ****************************\n")
      print_string(ai_reply)
      print("\n")

      count1=ai_reply.count("{1}")
      count2=ai_reply.count("{2}")

      if (count1 > 0 and count2 > 0):
         print(">>>>> Duplicate answer found")
         dup_answer = dup_answer + 1

      if (count1 == 0 and count2 == 0):
         print(">>>> No answer found")
         no_answer = no_answer + 1

      if (count1 == 1):
         print(">>>> Answer was group 1")
         group1 = group1 + 1

      if (count2 == 1):
         print(">>>> Answer was group 2")
         group2 = group2 + 1

# back to main outside loop 
   number_of_cycles = number_of_cycles + 1

print("\n----------- Final report --------------")
print("AI Prompt:")
print_string(prompt_txt)
print("AI model: " + ai_model)
print("Number of cycles: " + str(number_of_cycles))
print("AI Errors: " + str(ai_errors))
print("Dup answers: " + str(dup_answer))
print("Group 1 answers: " + str(group1))
print("Group 2 answers: " + str(group2))
print("No answers: " + str(no_answer))
