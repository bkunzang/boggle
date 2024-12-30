class Game:
    def __init__(self, player_list, board):
        '''
        Currently set up for single-player use in the terminal.
        '''
        self.player_list = player_list
        self.board = board

    def run_game(self, player):
<<<<<<< HEAD
        print("Welcome to Boggle! You will have 5 minutes to list as many words as you can.")
        x = input("Press enter to begin.")
        print(self.board)
=======
        print("Welcome to Boggle! You will have 5 minutes to list as many words as you can.
        x = input("Press enter to begin.")
        print(board)
>>>>>>> 089b606489b9a87056bdef986bcf4ec950ef0742

        # some psuedocode while I wait to implement the 5 minute timer function
        # not sure if I'll use another language to implement GUI where I can do that through the GUI
        # or use tkinter
        # but for now, limits number of words you can enter to 10
<<<<<<< HEAD
        while len(player.word_list) < 10:
            word = input("Enter a word: ")
            if word in self.player_list:
=======
        while len(player.word_list) < 10
            word = input("Enter a word: ")
            if word is in self.player_list:
>>>>>>> 089b606489b9a87056bdef986bcf4ec950ef0742
                print("You already entered that word!")
            else:
                player.word_list.append(word)

        print("Time's up!")

        # check each player's word list
        # lots of commented stuff because some of it is multi-player functionality related things
        removed_words = []
<<<<<<< HEAD
        possible_words = self.board.get_words()

        for i in range(len(self.player_list)):
            invalid_words = []

            for word in list(self.player_list[i].word_list):
                # if word in removed_words:
                #     self.player_list[i].word_list.remove(word) # if word has already been removed (it has been found in another player's word list)
                if word not in possible_words:
                    self.player_list[i].word_list.remove(word) # word is an invalid word
                    invalid_words.append(word)
                elif word in possible_words:
                    possible_words.remove(word)
=======

        for i in len(self.player_list):
            invalid_words = []

            for word in self.player_list[i].word_list:
                # if word in removed_words:
                #     self.player_list[i].word_list.remove(word) # if word has already been removed (it has been found in another player's word list)
                if word not in board.all_words:
                    self.player_list[i].word_list.remove(word) # word is an invalid word
                    invalid_words.append(word)
>>>>>>> 089b606489b9a87056bdef986bcf4ec950ef0742

            # # compare words to other players' lists
            # for j in (i+1, len(self.player_list)):
            #     for word in self.player_list[j]:
            #         if word in self.player_list[i]:
            #             self.player_list[i].word_list.remove(word)
            #             self.player_list[j].word_list.remove(word)
            #             removed_words.append(word)

            self.player_list[i].calculate_points()
            print(f"You scored {self.player_list[i].point_total} points!")
            print("The following words you entered were invalid: ", end="")
            for word in invalid_words:
                print(word, end=", ")
<<<<<<< HEAD
            print("\n Here are all possible words you missed:")
            print(possible_words)
=======
>>>>>>> 089b606489b9a87056bdef986bcf4ec950ef0742

        # print("The following words were shared with other players: ", end="")
        # for word in removed_words:
        #     print(word, end=", ") 

class Player:
<<<<<<< HEAD
    def __init__(self, game, point_total, word_list=[], level="Easy"):
        self.game = game
        self.point_total = point_total
        self.word_list = word_list
        self.level = level

    def calculate_points(self):
        for word in self.word_list:
            if len(word) == 3:
                if self.level == "Easy":
=======
    def __init__(self, word_list=[], game, point_total, level="Easy"):
        self.word_list = word_list
        self.game = game
        self.point_total = point_total
        self.level = level

    def calculate_points(self):
        for word in word_list:
            if len(word) == 3:
                if self.level = "Easy":
>>>>>>> 089b606489b9a87056bdef986bcf4ec950ef0742
                    self.point_total += 1
            elif len(word) == 4:
                self.point_total += 1
            elif len(word) == 5:
                self.point_total += 2
            elif len(word) == 6:
                self.point_total += 3
            elif len(word) == 7:
                self.point_total += 5
            elif len(word) >= 8:
                self.point_total += 11
