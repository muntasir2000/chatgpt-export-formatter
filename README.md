# What it does
ChatGPT allows to export all the conversations you had. This repository can help extract the conversations from the exported data and convert it to useful formats for finetuning an (open) LLM. 

Currently it supports conversation into these formats - 
* [ShareGPT/Vicuna](https://erichartford.com/meet-samantha)
* [Samantha](https://erichartford.com/meet-samantha)

# How to run
The repo can be run without installing any dependencies. Just make sure you have Python3 installed.

Input is typically a file named `conversations.json` from the archive provided by OpenAI when you exported your conversations.
* ShareGPT format example 
```
python3 chatgpt_to_sharegpt_format.py <input_file_path> <output_file_path>
```
* Samantha format example
```
python3 chatgpt_to_samantha_format.py --human-name "Theodore" --bot-name "Samantha" <input_file_path> <output_file_path>
```