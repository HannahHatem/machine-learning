from typing import List
def count_duplicates(text: str) -> list(tuple((str, int))):
    '''
    This function takes a text then detects duplicates and  
    it should ONLY return duplicates and their number of occurencesses in the form of list if tuples 
    '''
    output : list(tuple((str, int)))=[] 
    #TODO: ADD YOUR CODE HERE
    dict = {}
    text = text.lower()
    #text = text.split()
    for key in text:
        dict[key] = 0

    for key in text:
        dict[key] = dict[key] + 1

    for key in dict:
        if dict[key] > 1:
            output.append((key, dict[key]))


    return output