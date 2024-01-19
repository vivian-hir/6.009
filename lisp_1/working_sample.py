#TEST 

def remove_comments(source):
    new_list=[]
    new_string=""
    remove_n=source.split('\n')
    for line in remove_n:
        input=line.split(';')[0]
        new_list.append(input)
    for item in new_list:
        new_string+=item 
    
    for char in new_string:
        if char=='(': 
            new_string.replace('(',' ( ')
        if char==')':
            new_string.replace(')', ' ) ')
    new_string.split()
    # for item in new_list: 
    #     if item!='':
    #         new_string+=item
    return 
   

def tokenize(new_string):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """

    sample_list = []
    i = 0
    # while loop transfer from smaller container to big container
    #create helper method to get rid of \n and the semicolons (comments)
    #get rid of the extra white space 
    #new_string=remove_comments(source)
    while i < len(new_string):
        small_string = ""
        # perform string concatenation
        while ( #but I only can do one character 
            new_string[i] != " " and new_string[i] != "(" and new_string[i] != ")" 
        ):  # impossible to fail or statement
            small_string += new_string[i]
            # don't need these if statements
            i += 1
            if i == len(new_string):
                break
        # check if it stopped on an empty or parentheses
        if small_string == "":
            if new_string[i] != " ": 
                sample_list.append(new_string[i])
            i += 1  # want to increment cause didn't go inside while loop
        else:
            sample_list.append(small_string)
    return sample_list
    #I think that you need to write something more specific for semicolon
    #It has to not append any character after the semicolon 
    #Use the /n, not sure how to though 
        

if __name__ == "__main__":
    new_string="(cat (dog (tomato)))"
    print(remove_comments(new_string))
    #new_string=line_helper(sample_string)
    #remove_space=string_input.split()
    #print(remove_space)
    #final_string=space_remover(new_string)
    #print(final_string)
    #how do I delete the comments in between semicolon and the \ symbol? 
    #do some while loop to delete it? 
