
import sys

#Braille to English dictionary
#Mapping Braille (represented as "O" and ".") to English letters, numbers, and special symbols (like space, capital follow, and number follow)
braille_to_english = {
    "O.....": "a", "O.O...": "b", "OO....": "c", "OO.O..": "d", "O..O..": "e", "OOO...": "f", "OOOO..": "g", "O.OO..": "h",
    ".OO...": "i", ".OOO..": "j", "O...O.": "k", "O.O.O.": "l", "OO..O.": "m", "OO.OO.": "n", "O..OO.": "o", "OOO.O.": "p",
    "OOOOO.": "q", "O.OOO.": "r", ".OO.O.": "s", ".OOOO.": "t", "O...OO": "u", "O.O.OO": "v", ".OOO.O": "w", "OO..OO": "x",
    "OO.OOO": "y", "O..OOO": "z", "......": " ", ".O.OOO": "#", ".....O": "^"  # '#' for numbers, '^' for capitalization
}

#English to Braille dictionary
#Reverse the braille_to_english mapping so that we can translate from English to Braille
english_to_braille = {v: k for k, v in braille_to_english.items()}

#Mapping numbers 0-9 to their Braille representations
numbers_to_braille = {
    str(i): b for i, b in enumerate([".O....", ".O.O..", ".OO...", ".OOO..", ".O..O.", ".O.OO.", ".OO.O.", ".OOO.O", ".O..OO", ".O.OOO"])
}
#Update the English to Braille dictionary to include number mappings
english_to_braille.update(numbers_to_braille)

#Function to translate English text into Braille
def translate_to_braille(text):
    # List to store the Braille result
    result = [] 
    for char in text:
        if char.isupper():
            # If the character is uppercase, first add the capital follow symbol ('^') then the lowercase version of the letter
            result.append(english_to_braille['^'])  # Capitalization symbol
            result.append(english_to_braille[char.lower()])
        elif char.isdigit():
            # If the character is a number, first add the number follow symbol ('#') then the corresponding Braille number
            result.append(english_to_braille['#'])  # Number follow symbol
            result.append(english_to_braille[char])
        else:
            # For lowercase letters and spaces, directly append their Braille representation
            result.append(english_to_braille[char])
    return ''.join(result)  # Join list elements into a single string

# Function to translate Braille text into English
def translate_to_english(braille_text):
    # List to store the English result
    result = []
    # Index to traverse the Braille input
    i = 0
    # Total length of the Braille input
    length = len(braille_text)
    # Flag to track if we are in capitalization mode
    capital_mode = False
    # Flag to track if we are in number mode
    number_mode = False
    
    # Loop through the Braille text, 6 characters at a time (since each Braille character is represented by 6 dots)
    while i < length:
        # Extract a 6-character Braille segment
        braille_char = braille_text[i:i+6]
        # Number follow symbol
        if braille_char == ".O.OOO":
            # Number follow symbol
            number_mode = True
            i += 6
            continue
        # Capital follow symbol
        if braille_char == ".....O":
            # Enter capitalization mode for the next character
            capital_mode = True
            i += 6
            continue
        # Space symbol
        if braille_char == "......":
            # Append a space to the result
            result.append(" ")
            # Exit number mode on space
            number_mode = False
            # Exit capital mode on space
            capital_mode = False
        else:
            if number_mode:
                # If in number mode, find the corresponding number for the Braille character
                for number, b in numbers_to_braille.items():
                    if b == braille_char:
                        # Append the number to the result
                        result.append(number)
                        break
                # Exit number mode after processing one number
                number_mode = False
            else:
                # Look up the Braille character in the braille_to_english dictionary
                char = braille_to_english.get(braille_char, "")
                if capital_mode:
                    # Append the capitalized character
                    result.append(char.upper())
                    # Exit capitalization mode after one character
                    capital_mode = False
                else:
                    # Append the normal character
                    result.append(char)
        # Move to the next 6-character Braille segment
        i += 6
    # Join list elements into a single string
    return ''.join(result)

# Main function to handle input and determine translation direction
def main():
    if len(sys.argv) != 2:
        # Check if the correct number of arguments are passed (we expect one argument)
        print("Usage: python translator.py <string>")
        return
    
    # Get the input text from the command-line argument
    input_text = sys.argv[1]
    
    # Detect if the input is Braille (only contains 'O' and '.' characters) or English (letters, digits, spaces)
    # If all characters are 'O' or '.', it's Braille
    if all(c in "O." for c in input_text):
        # Translate Braille to English
        print(translate_to_english(input_text))  
    else:  # If not, it's English
        # Translate English to Braille
        print(translate_to_braille(input_text))

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
