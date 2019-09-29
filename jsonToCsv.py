import json

def flatten(dictionary, json):
    for attribute in json:
        if type(json[attribute]) is dict:
            flatten(dictionary, json[attribute])
        else:
            dictionary.append(json[attribute])
    return dictionary

def getTitles(dictionary, json, string):
    for attribute in json:
        if type(json[attribute]) is dict:
            if string != "":
                getTitles(dictionary, json[attribute], string+'.'+attribute)
            else:
                getTitles(dictionary, json[attribute], attribute)
        else:
            dictionary.append(string+'.'+attribute)
    return dictionary
