# Loop control variable
playing = input('Would you like to sing a song? y/n: ');

# Amount of possible bottles
BOTTLES = 100;

# While playing starts with a y (loop test)
while (playing.lower().startswith('y')):

    # Get the number of verses we want to sing
    verses = input('How many verses do you want to sing?: ');
    # If not the verse is a digit, or the verses are less than 1, or the verses are greater than bottles, request input again.
    while (not(verses.isdigit()) or int(verses) < 1 or int(verses) > BOTTLES):
        verses = input('How many verses do you want to sing?: ');

    # Cast to an int
    verses = int(verses);

    # Bit more room here
    print();

    # For each verse in the verses range.
    for verse in range(verses):
        # Our current bottle, and our next bottle (for bottom preview)
        bottle_num = BOTTLES - verse;
        bottle_num_next = bottle_num - 1;

        print(bottle_num, 'bottles of beer on the wall');
        print(bottle_num, 'bottles of beer');
        print('If one of those bottles should happen to fall');

        # If the bottles are zero, then we simply state we have none left!
        if (bottle_num_next == 0):
            print('No bottles of beer on the wall!!');
        else:
            print(bottle_num_next, 'bottles of beer on the wall');
            
        print();

    # Update loop control variable
    playing = input('That was fun, want to play again? y/n: ');

print('Thanks for singing along! :D');
