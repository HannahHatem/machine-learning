import string
from typing import List


def check_and_extract_key(message: str, cyphered: str) -> int:
    '''
    This function takes a Message and possible cyphered,
    first check if cyphered is encrypted from  Message,
    then extract the key used in encryption and return it
    NOTE KEY MUST BE POSITIVE
    if cyphered is NOT encrypted from  Message return -1
    '''
    d = dict( zip(string.ascii_lowercase, (i for i in range(1, 27))))
    key: int
    message = message.lower()
    cyphered = cyphered.lower()
    msgSize = len(message)
    cyphSize = len(cyphered)
    key = 0
    if msgSize != cyphSize or message == cyphered:
         return -1
    else:
         if d[cyphered[0]] > d[message[0]]:
              key = d[cyphered[0]] - d[message[0]]
              for i in range (msgSize):
                   if d[cyphered[i]] > d[message[i]] and d[cyphered[i]] - d[message[i]]!=key:
                        return -1
                   elif d[cyphered[i]] < d[message[i]] and (d[cyphered[i]] - d[message[i]]+26)!=key:
                        return -1
     
         elif  d[cyphered[0]] < d[message[0]]:
              key = d[cyphered[0]] - d[message[0]] +26
              for i in range (msgSize):
                   if d[cyphered[i]] > d[message[i]] and d[cyphered[i]] - d[message[i]]!=key:
                        return -1
                   elif d[cyphered[i]] < d[message[i]] and (d[cyphered[i]] - d[message[i]]+26)!=key:
                        return -1

    return key
