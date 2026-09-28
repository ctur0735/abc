
#defining the story function
def story(num_encounters): 
    try: #checking if this function attribute has previously been defined or set as true
        if not story.outer_recursion:
            raise AttributeError 
    except AttributeError:
        story.outer_recursion = True #defining a value so the except block won't run for any following recursions
        print("You enter the dungeon...") # hence this only prints in the outermost recursion
    
    if num_encounters <= 0: #base case to stop further encounters and recursion 
        return
    encounters = ["finding_stairs", "finding_treasure", "mirror_realm", "mysterious_stranger"]
    import random #importing module to randomly choose an element of the encounter options
    chosen = random.choice(encounters)
    #conditional code chunks to handle each chosen encounter
    if chosen == "finding_stairs":
        user_input = input("You've found some descending stairs, would you like to go down? ")
        if user_input.lower() == "yes" or user_input.lower() == "y":
            num_stairs = list(range(1, 11))
            chosen_stairs = int(random.choice(num_stairs)) #chosing a random number of stairs, between 1 and 10 inclusive
            stairs(chosen_stairs) #calling stairs function to print the chosen number of stairs
        else:
            print("You choose not to go down.") 
    elif chosen == "finding_treasure":
        #determing what treasure is found using random module
        treasure_chances = list(range(1, 11))
        chosen_treasure = int(random.choice(treasure_chances))

        if chosen_treasure == 1: # for rare diamond (this has 10% chance of being true since runs for 1 out of the 10 options)
            print("You found a rare diamond!")
            diamond_sizes = list(range(1, 16, 2))
            chosen_d_size = int(random.choice(diamond_sizes))
            diamond(chosen_d_size) #calling diamond function to print the diamond of the requried random odd size using random module
        else: # for square gem (this has a 90% chance of being true since runs for 9 out of the 10 options)
            print("You found a square gem!")
            gem_sizes = list(range(1, 6))
            chosen_gem_size = int(random.choice(gem_sizes))
            square(chosen_gem_size) #calling square function to print the gem of the requried random size using random module
    elif chosen == "mirror_realm":
        phrase = input("You've found the mirror realm! Anything you say will be reversed, try it out: ")
        #calling mirror function to reverse the character order of the 'phrase' user_input
        mirror(phrase) 
    elif chosen == "mysterious_stranger":
        print("You come across a mysterious stranger, he warns you that...")
        #calling generate_sentence function reveal the message from the text file, read by the generate_structure function
        generate_sentence("<s>", generate_structure("stranger_structure.txt"))
    story(num_encounters-1) #calling the function to recurse for the next encounter

#defining the stairs function
def stairs(integer: int):
    #setting base case to return, ensuring the function stops once no stairs are left, or so that non-positive inputs dont draw any stairs
    if integer <=0:
        return
    #first runs the function for 1 less amount of stairs (if possible) before print the stair to ensure the stairs are not printed upside down
    stairs(integer - 1)
    print("▅" * integer)

#defining the function to print the square gem of a certain size
def square(size: int, square_row: int = 1): # using a second parameter to track the row of square the function is printing in the current recursion
    #base case to stop recursion, and emitting invalid square sizes
    if size <=0 or size < square_row:
        return
    #printing the gems all across for the first and last rows, forming the top and bottom of the square
    if square_row == 1 or square_row == size:
        print("◆" * size)
    #printing the sides of the square
    else: 
        print("◆" + " " * (size - 2) + "◆")
    #calling the function in itself to print the next row of the same square, else only one row would be printed
    square(size, square_row + 1)

#defining the diamond function to print a diamond of a given size
def diamond(size: int, row: int = 1): #using a second parameter to track the row of the diamond the function is printing in the current recursion
    #the base case to stop recursion once past the last row, and emitting invalid (negative) gem sizes
    if size <=0 or size < row:
        return
    #to print the top and bottom row of the diamond, i.e. where only one * is required to be printed in the middle
    if row == 1 or row == size:
        print(" " * int((size - 1) / 2) + "*" + " " * int((size - 1) / 2))
    # to print the middle rows of the diamond, i.e. where two * are required to be printed, with spacing dependent on the row 
    else: # can use an else statement for this since all other invalid sizes have already been returned
        middle_spaces = int(2 * min(row, size - row + 1) - 3)
        outside_spaces = int((size - middle_spaces - 2) / 2)
        print(" " * outside_spaces + "*" + " " * middle_spaces + "*" + " " * outside_spaces)
    #recursively calling the diamond function to print the next row of the same size gem
    diamond(size, row + 1)

#defining the mirror function to reverse a given string parameter
def mirror(input_string):
    '''
    to refer to the original string length throughout recursion with given coding restraints, 
    see if it is previously defined attribute of the function. Using a try and except block, 
    by trying to refer to the attribute. This will raise an attribute error if the current 
    recursion is for the original string. In this exception, the function attribute will be defined. 
    Otherwise it will remain the same as the previous, original one'''
    try: #checking if this function attribute has previously been defined or set as a not false value
        if not mirror.original_length:
            raise AttributeError
    except AttributeError:
        mirror.original_length = len(input_string) #defining the attribute the be the length of the original string
        
    #base case for when the given string is empty, i.e. when all characters of the string have been emitted in recursion
    if input_string == "":
        pass
    #printing the last letter of the string first, since the innermost recursion will be completed first
    else:
        length = len(input_string)
        mirror(input_string[1:]) #recursively calling the function excluding the first letter of the string
        print(input_string[0], end='')
    #printing a new line at the end of the reversed string, by refering to the attribute of the original length
    if len(input_string) == mirror.original_length:
        print()
        mirror.original_length = False #defining the attribute to be false at the end of recursion so the function still works when it is reused

#defining function to return a dictionary of symbol keys and expression values
def generate_structure(filename):
    structure_dict = {} # initalising empty dictionary to start with
    with open(filename, "r") as file: 
        for line in file: #iterating through the given file lines
            line = line.strip()
            symbol, expression = line.split(":") #splitting each line into its non-terminal and terminal
            options = expression.split("|") #list of options for a non-terminal's value
            structure_dict[symbol] = options #adding the non-terminal, terminal as a key, value pair to the structure dictionary
    return structure_dict

#Defining function to print a sentence
def generate_sentence(symbol, structure): 
    import random

    try: #checking if the function attribute 'depth' has been defined
        generate_sentence.depth -= 1 
    except AttributeError:
        generate_sentence.depth = 0 #initialising depth value (in outer recursion)

    sentence_s_options = structure[symbol] #list of values of the key symbol
    chosen_s = str(random.choice(sentence_s_options)) #chosing a random sentence structure for symbol
    parts = chosen_s.split(",")
    words_list = []

    #looping through symbols to make a list of the chosen terminals
    for part in parts:
        part = part.strip()
        if part.startswith("<") and part.endswith(">"):
            value = generate_sentence(part, structure) #recursively calling the function for any non-terminal
            words_list.append(value)
        else:
            words_list.append(part)

    #making a string of the words list to form a sentence/phrase
    sentence = " ".join(words_list).strip()
    
    if generate_sentence.depth == 0:
        print(sentence) #printing the sentence, only if in outer recursion so the parts of the sentences aren't only printed
    generate_sentence.depth += 1 #adjusting the depth tracking back (moving out of recursion)
    
    return sentence #also returning the sentence so it could be printed again if required


def main():
    print("Welcome to the dungeon adventure!")
    #asking user for number of encounters, and checking if the input is a valid integer
    while True:
        try:
            num_encounters = int(input("How many encounters would you like to have? "))
            break
        except ValueError:
            print("Please enter a valid integer.")
    story(num_encounters) #calling the story function with the user inputted number of encounters

if __name__ == '__main__':
    main()