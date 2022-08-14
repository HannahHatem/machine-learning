import json
import os
from pyclbr import Function
from bracket_sequence import check_bracket_sequence
from word_counter import count_occurrences
from duplicates_counter import count_duplicates
from encryption import check_and_extract_key
#DONT CHANGE ANY OF THIS CODE

directory ='./testcases/q'



def run_testcases(problem_number: int, test_function: Function):
    problem_number=str(problem_number)
    path = directory+problem_number
    output_file = open("output/q"+problem_number+".txt", "w")
    test_index=1
    for filename in os.scandir(path):
        if filename.is_file(): 
            testcase_file=open(filename.path)
            data = json.load(testcase_file)
            input_args =data['input_args']
            output=test_function(*input_args)
            statement="test case "+str(test_index) +'\noutput:\t'+str(output)+'\n\n'
            output_file.write(statement)
            test_index+=1
            testcase_file.close()




# # main loop
run_testcases('1', check_and_extract_key)
run_testcases('2', count_occurrences)
run_testcases('3', count_duplicates)
run_testcases('4', check_bracket_sequence)


# parser_fun("())(()")