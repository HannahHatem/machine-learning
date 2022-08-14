import ast

def count_occurrences(filePath: str , word: str) -> int:
    '''
    This function takes a filePath
    It should return number of occurrences for a given word in this file"  
    '''
    occurrences:int=0
    #TODO: ADD YOUR CODE HERE
    with open(filePath, 'r') as file:
        data = file.read().replace('\n', '')

    word = word.lower()
    data = data.lower()
    data = data.replace(".", " ")
    data = data.replace(",", " ")
    data = data.replace("@", " ")
    data = data.replace("!", " ")
    data = data.replace("'", " ")
    res = data.split()  
    dict = {}
    for key in res:
        dict[key] = 0

    for key in res:
        dict[key] = dict[key] + 1

    occurrences =  dict.get(word, 0)

    return occurrences