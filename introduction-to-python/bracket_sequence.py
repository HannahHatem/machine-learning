def check_bracket_sequence (sequence: str)-> bool: 
    
    '''
    This function takes a sequence of brackets and return true if the sequence can be fixed within at most one step
    and return false otherwise   
    '''
    can_be_fixed:bool
    #TODO: ADD YOUR CODE HERE
    can_be_fixed  = False
    dict = {}
    #if sequence == "":
    #    return False
    
    count = 0
    
    if (len(sequence) %2) !=0:
        can_be_fixed = False
    else:
        for i in sequence:
            if i == ")":
                count = count -1
            else:
                count = count + 1
            if count < -1:
                break

        if count == 0:
            return True
        elif count == -1 or count == 1:
            return True
        else:
            return False
        
    return can_be_fixed

