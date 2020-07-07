# Write your code here
import random

print('H A N G M A N')

word_list = ['python', 'java', 'kotlin', 'javascript']

while True:
    start_input = input('Type "play" to play the game, "exit" to quit:')
    if start_input == 'play':
        num_lives = 8
        ans = random.choice(word_list)
        string = '-' * len(ans)
        list_correct_input = []
        list_user_input = []
    elif start_input == 'exit':
        break
    else:
        continue

    while num_lives > 0:
        print(f'\n{string}')
        user_input = input("Input a letter: ")

        if user_input in list_user_input:
            print('You already typed this letter')
            continue
        if len(user_input) > 1:
            print('You should input a single letter')
            continue
        if not user_input.isalpha() or user_input.isupper():
            print('It is not an ASCII lowercase letter')
            continue

        if user_input in ans:
            list_correct_input.append(user_input)
            string = ''.join([s if s in list_correct_input else '-' for s in ans])
        else:
            print('No such letter in the word')
            num_lives -= 1

        if '-' not in string:
            print('You guessed the word!')
            print('You survived!')
            break
        list_user_input.append(user_input)
    else:
        print('You are hanged!')



