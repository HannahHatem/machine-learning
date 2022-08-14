# Problem Set 0: Introduction to Python

The goal of this problem set is to test your ability to code simple python programs and understand python code.

## Instructions

- In the attached python files, you will find locations marked with:

```
  #TODO: ADD YOUR CODE HERE
```

- Here you should write your solution to the problem. **DO NOT MODIFY ANY OTHER CODE**;

- You will find test cases folder where you can find input test cases for each question these test cases will be used in the grading phase so make sure that the output for each input is correct.

- [Hint] in the first 2 test cases for each problem you will find expected output for the givin input to help you figuring out your mistakes

- The `main.py` file can be used to run all the test cases which create three output files each file has your function's output for all the test cases. **DO NOT MODIFY CODE IN THIS FILE**

## Submission Format

You should submit a zipped file which follow the following format **StudentID_StudentFullName_TutCode_Ass0.zip** for example 1170289_HosamHazemEzzat_2_Ass0

where TutCode refers to in which room do you take your tutorial
3706 --> 1 and 3708 --> 2

---

## Introduction to Type hints

In the given code, we heavily use [Type Hints](https://docs.python.org/3/library/typing.html). Although Python is a dynamically typed language, there are many reasons that we would want to define the type for each variable:

1. Type hints tell other programmers what you intend to put in each variable.
2. It helps the intellisense find reasonable completions and suggestions for you.

Type hints are defined as follows:

    variable_name: type_hint

for example:

    #  x will contain an int
    x: int

    # x contains a string
    x: str = "hello"

    # l contains a list of anything
    l: List[Any] = [1, 2, "hello"]

    # u contains a float or a None
    u: Union[float, None] = 1.25

We can also write type hints for functions as follows:

    # Function is_odd takes an int and returns a bool
    def is_odd(x: int) -> bool:
        return (x%2) == 1

Some type hints must be imported from the package `typing`. Such as:

    from typing import List, Any, Union, Tuple, Dict

In all of the assignments, we will use type hints whenever possible and we recommend that you use them for function and class definitions.

---

## Problem 1: Caesar cypher

Caesar cypher is a simple substitution cypher in which each letter of the plain text is substituted with a letter found by moving n places down the alphabet.

```

For example, assume the input plain text is the following:
abcdxyz
If the shift value, n, is 4, then the encrypted text would be the following:
efghbcd

```

Inside `encryption.py`, modify the function `check_and_extract_key` which takes a message and cyphered text as argument

- first check if cyphered text is encrypted by Caesar cypher method from the given message
- then extract the key (number of letters to shift) used in encryption
- return the key NOTE KEY MUST BE POSITIVE int
- if cyphered text is NOT encrypted from the message return -1

**Note: You can assume the message is only alphabetic there is neither numbers nor special chars.**

## Problem 2: word counter

Inside `word_counter.py`, modify the function `count_occurrences`. This function takes a file path and a word and it should return the number of the word occurrences in this file.
**Note: it should be case-insensitive for example if the word is "hi" then HI , Hi or hI does count**

## Problem 3: Count Duplicates

Inside `duplicates_counter.py`, modify the function `count_duplicates` which take input text as argument and should return the count of distinct case-insensitive alphabetic characters and numeric digits that occur more than once in the input string. The input string can be assumed to contain only alphanumeric characters, including digits, uppercase and lowercase alphabets
for example:
"aaBcbde" -> [('a',2) ,(b,2)]
"aBcd" -> []

## Problem 4: Bad Sequence

Adam's friends made him a birthday present — a bracket sequence. Adam was quite disappointed with his gift, because he dreamed of correct bracket sequence, yet he told his friends nothing about his dreams and decided to fix present himself.

To make everything right, Adam is going to move **at most one bracket** from its original place in the sequence to any other position. Reversing the bracket (e.g. turning "(" into ")" or vice versa) **isn't allowed**.

We remind that bracket sequence s is called correct if:

- s is empty;
- s is equal to "(t)", where t is correct bracket sequence;
- s is equal to t1t2, i.e. concatenation of t1 and t2, where t1 and t2 are correct bracket sequences.

For example, "(()())", "()" are correct, while ")(" and "())" are not. Help Adam to fix his birthday present and understand whether he can move one bracket so that the sequence becomes correct.

Inside `bracket_sequence.py`, modify the function `check_bracket_sequence` which take sequence of brackets as string and return true if the sequence can be fixed within at most one move (requires 0 or 1 move) and false otherwise

examples:

- if input "(())" then output is true (0 moves are required to fix it)
- if input "())(" then output is true (1 move is required to fix it)
- if input "))()((" then output is false (2 moves are required to fix it)
- if input "()(" then output is false(it can not be fixed)

## Delivery

The delivery deadline is saturday `March 5th 2022 23:59`. It should be delivered on **Blackboard**.This is an individual assignment. The delivered code should be solely written by the student who delivered it. Any evidence of plagiarism will lead to receiving **zero** points. and late submission would be penalized
