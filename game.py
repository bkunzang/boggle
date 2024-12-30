class Game:
    def __init__(self, player_list, board):
        '''
        Currently set up for single-player use in the terminal.
        '''
        self.player_list = player_list
        self.board = board

    def run_game(self, player):
        print("Welcome to Boggle! You will have 5 minutes to list as many words as you can.
        x = input("Press enter to begin.")
        print(board)

        # some psuedocode while I wait to implement the 5 minute timer function
        # not sure if I'll use another language to implement GUI where I can do that through the GUI
        # or use tkinter
        # but for now, limits number of words you can enter to 10
        while len(player.word_list) < 10
            word = input("Enter a word: ")
            if word is in self.player_list:
                print("You already entered that word!")
            else:
                player.word_list.append(word)

        print("Time's up!")

        # check each player's word list
        # lots of commented stuff because some of it is multi-player functionality related things
        removed_words = []

        for i in len(self.player_list):
            invalid_words = []

            for word in self.player_list[i].word_list:
                # if word in removed_words:
                #     self.player_list[i].word_list.remove(word) # if word has already been removed (it has been found in another player's word list)
                if word not in board.all_words:
                    self.player_list[i].word_list.remove(word) # word is an invalid word
                    invalid_words.append(word)

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

        # print("The following words were shared with other players: ", end="")
        # for word in removed_words:
        #     print(word, end=", ") 

class Player:
    def __init__(self, word_list=[], game, point_total, level="Easy"):
        self.word_list = word_list
        self.game = game
        self.point_total = point_total
        self.level = level

    def calculate_points(self):
        for word in word_list:
            if len(word) == 3:
                if self.level = "Easy":
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