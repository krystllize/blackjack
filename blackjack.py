import math
import pandas as pd
 
# Game Marker - helps mark whether the player is playing a game or not.
in_play = True
 
class Deck:
    def __init__(self, players, place):
        self.players = players
        self.card_num = decks
        self.place = place
        self.deck_dict = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
        self.deck_list = list(self.deck_dict.keys())
        self.blackjack = False
        self.my_values = [] # string list of card values
        self.my_running_sum  = [] # int list of converted card values
        self.player_cards = []
        self.dealer_cards = []
    
    #Default draw card function, removes the specified card from the current deck and returns a dataframe of remaining cards in the deck.
    def draw(self, values_drawn):
        for x in values_drawn:
            i = self.deck_list.index(x)
            self.card_num[i] -= 1
        tracker = {"Card Values": self.deck_list, "Number of Cards Left in the Deck": self.card_num}
        print(pd.DataFrame(tracker))
 
   #Initial draw of your own cards in the round
    def self_cards(self):
        for e in range(len(self.my_values)):
            self.my_running_sum.append(self.deck_dict[self.my_values[e]]) # convert card values and append to running sum list
            
        #Splits occur when you receive two cards of the same denomination, which gives you the option to play each card as a separate hand.    
        if (self.my_values[0] == self.my_values[1]):
            while True:
                pass_option = input("You may choose to split. Proceed? (Y/N)").upper()
                if pass_option == "Y":
                    self.split_draw()
                    break
                elif pass_option == "N":
                    self.current_self_value()
                    self.self_rehit()
                    break
                else:
                    print("Please ensure you have typed 'Y' or 'N' correctly.")
        else: #For two regular cards received (non-split cards)
            self.current_self_value()
            if self.blackjack == False:
                self.self_rehit()
            
    def current_self_value(self):
        total = sum(self.my_running_sum) #current total value in hand
        if "A" in self.my_values:
            if total == 11: # Ace is listed as having a value of 1 in the deck dictionary, therefore immediately having a value of 10 + ace (11) would mean you'd have a blackjack.
                print("You have achieved a natural/blackjack! Your turn with your current hand is now finished.")
                self.blackjack = True
                return
            else:
                if (total+10) < 21:
                    print("Your current value in your hand is", str(total), "or", str(total+10) + ".") # Ace represents a 1 or 11 in value
                    self.probability([total, total+10], "my_turn")
                else: 
                    print("Your current value in your hand is", str(total) + ".")
                    self.probability([total], "my_turn")
                
        elif total == 21: # If total in your hand equals 21 without the help of an ace
            print("You have achieved a natural/blackjack! Your turn with your current hand is now finished.")
            self.blackjack = True
            return
        else:
            print("The current value in your hand is", str(total) + ".")
            if total < 21:
                self.probability([total], "my_turn")
        
        if total > 21:
            print("You have drawn a hand over 21, your turn will now end.")
            return
 
    def split_draw(self):
        if (self.my_values[0] == "A") and (self.my_values[1] == "A"): # Special case of drawing two aces in your hand, this program assumes the casino only allows you to draw one card on each split ace.
            print("Since you have drawn two aces, you will draw two cards per split ace and will not be able to draw again.")
            for z in range(0, 2): 
                self.probability([11], "my_turn")
                print("Please print the value you have received on your ace.")
                self.check_initial_values_deck("split_ace")
            
            print("The value you have obtained for both split ace hands are", (11 + self.deck_dict[self.my_values[2]]), "and", str(11 + self.deck_dict[self.my_values[3]]) + ".")
            if ((11 + self.deck_dict[self.my_values[2]]) == 21) or ((11 + self.deck_dict[self.my_values[3]])) == 21: # If either your left ace or right ace hands reach 21
                print("Congratulations, you have achieved a blackjack!")
                self.blackjack = True
            else:
                print("You will not be able to draw any more cards, and your turn is finished.")
        else:
            # Regular non-ace split
            print("You will be able to draw on both cards. Please play the hand on your left first.")
            self.my_running_sum.pop(1) # Remove second value fom the running sum given that you are splitting hands
            self.probability([self.deck_dict[self.my_values[0]]], "my_turn") # Probability for first split ace
            self.self_rehit()
            print("For your right split hand:")
            self.probability([self.deck_dict[self.my_values[1]]], "my_turn") # Probability for second split ace
            print("Now, please play the hand on your right.")
            self.my_running_sum.clear()
            self.my_running_sum.append(self.deck_dict[self.my_values[1]]) # Replace running sum with other split hand value
            
            for i in range(1, len(self.my_values)): # Clear values obtained from previous split hand except for the split card currently in play 
                self.my_values.pop(1)
            self.self_rehit()
 
    def probability(self, total, player):
        if len(total) == 1:
            base_value = total[0]
            hit_list = list(range(base_value + 1, base_value + 12)) # Range is 11 given that an ace can represent 1 or 11
            prob_list = []
        
            # Probability of remaining below 21 if you have not exceeded 21 in your current hand.
            if player == "my_turn":
                for y in range(0, 9):
                    probability = (math.comb(self.card_num[y], 1)) / (math.comb(sum(self.card_num)-1, 1)) # Use combination formula to measure probability of drawing each value out of the remaining cards in the deck.
                    prob_list.append(probability)
            
                # Since 10 + J + Q + K all equal 10, tens probability must be calculated separately by summing the number of 10, J, Q, and K cards left.
                tens_probability = math.comb(sum(self.card_num[-4:]), 1) / (math.comb(sum(self.card_num)-1, 1))
                prob_list.append(tens_probability)
                
                #Since ace counts as 11, this simply equals the probability of drawing +1.
                elevens_probability = math.comb(self.card_num[0], 1) / (math.comb(sum(self.card_num)-1, 1))
                prob_list.append(elevens_probability)

                print("These are your probabilities:")
                print(pd.DataFrame({"Possible Hit Values": hit_list, "Probability": prob_list}))
                if base_value == 10:
                    under_21_prob = sum(prob_list[0:hit_list.index(21)])
                    print("You have a", ("{:.4%}".format(under_21_prob)), "chance of drawing a value that keeps you 21 or under. Your probability of drawing a Blackjack next round is", "{:.4%}".format(prob_list[hit_list.index(21)]) + ".")
                elif 21 in hit_list and base_value < 21:
                    under_21_prob = sum(prob_list[0:hit_list.index(21)+1])
                    print("You have a", ("{:.4%}".format(under_21_prob)), "chance of drawing a value that keeps you 21 or under. Your probability of drawing a Blackjack next round is", "{:.4%}".format(prob_list[hit_list.index(21)]) + ".")
                elif base_value < 21: # If your current value in your hand is too small to reach 21 in the next draw (you have a value of 10 or less).
                    print("You have a 100% chance of drawing a value that keeps you 21 or under. However, you don't have a high enough value to obtain a Blackjack in the next round.")
            elif player == "dealer":
                for y in range(0, 9):
                    probability = (math.comb(self.card_num[y], 1)) / (math.comb(sum(self.card_num), 1)) 
                    prob_list.append(probability)
            
                tens_probability = math.comb(sum(self.card_num[-4:]), 1) / (math.comb(sum(self.card_num), 1))
                prob_list.append(tens_probability)
                
                #Since ace counts as 11, this simply equals the probability of drawing +1.
                elevens_probability = math.comb(self.card_num[0], 1) / (math.comb(sum(self.card_num), 1))
                prob_list.append(elevens_probability)

                if base_value == 10:
                    print("The dealer has a 100% chance of drawing a value 20 or under. While they cannot obtain a blackjack with their current cards, these are the following probabilities in which the dealer can obtain values between 17 and 20:")
                    print(pd.DataFrame({"Possible Hit Values": hit_list[hit_list.index(17):hit_list.index(21)], "Probability": prob_list[hit_list.index(17):hit_list.index(21)]}))
                elif base_value == 1:
                    print("The dealer has a 100% chance of drawing a value 20 or under. While they cannot obtain a blackjack with their current cards given their previous confirmation, these are the following probabilities in which the dealer can obtain values between 17 and 20:")
                    new_hit_list = [i for i in range(17,21)]
                    print(pd.DataFrame({"Possible Hit Values": new_hit_list, "Probability": prob_list[hit_list.index(7):hit_list.index(11)]}))
                elif base_value >= 6:
                    print("The dealer has a 100% probability to stay", hit_list[-1], "or under. While they cannot obtain a blackjack with their current cards, these are the following probabilities in which the dealer can obtain values above 17:")
                    print(pd.DataFrame({"Possible Hit Values": hit_list[hit_list.index(17):], "Probability": prob_list[hit_list.index(17):]}))
                else:
                    print("The dealer is guaranteed to stay 21 or under on their next draw, however they will be unable to reach a value of 17 or over flipping over their card.")
        else: # Case of having an ace in your current hand
            base_value = total[0]
            hit_list = list(range(base_value + 1, base_value + 22)) # Range is 21 since the ace can represent 1 or 11
            prob_list = []
            
            for x in range(len(total)):
                for y in range(0, 9):
                    probability = (math.comb(self.card_num[y], 1)) / (math.comb((sum(self.card_num)-1), 1)) # Subtract one from the total to represent the hidden card drawn by the dealer not present in the deck
                    prob_list.append(probability)
            
                tens_probability = math.comb(sum(self.card_num[-4:]), 1) / (math.comb((sum(self.card_num)-1), 1))
                prob_list.append(tens_probability)
                
                # We don't append the probability of drawing 11 to the initial value to the first iteration, only the second, since the probability of drawing +11 will be replaced by the next iteration representing base_value +10 +1.
                if x == 1:
                    elevens_probability = math.comb(self.card_num[0], 1) / (math.comb((sum(self.card_num)-1), 1))
                    prob_list.append(elevens_probability)
            
            print(pd.DataFrame({"Possible Hit Values": hit_list, "Probability": prob_list}))
            
            under_21_prob = sum(prob_list[hit_list.index(base_value+11):hit_list.index(21)+1])
            print("You are 100% guaranteed to stay below 21, however if you are counting from", str(base_value + 10) + ", your probability of staying below 21 is", ("{:.4%}".format(under_21_prob)), 
                "and your probability of drawing a Blackjack next round is", "{:.4%}".format(prob_list[hit_list.index(21)]) + ".")
 
    def check_initial_values_deck(self, turn):
        if turn == "my_turn":
            while True:
                card = list(input().split())
                if len(card) != 2:
                    print("Please ensure you have typed two cards.")
                    continue
                elif (card[0] not in self.deck_list) or (card[1] not in self.deck_list):
                    print("Please ensure you have typed the correct card values.")
                    continue
                elif (self.card_num[self.deck_list.index(card[0])] == 0) or (self.card_num[self.deck_list.index(card[1])] == 0): # If the card amount has reached 0, raise error.
                    print("Please ensure you have typed the correct values.")
                    continue
                else:
                    self.draw(card)
                    self.my_values.extend((card[0], card[1]))
                    break
        elif turn == "split_ace":
            while True:
                card = input().split()
                if len(card) != 1:
                    print("Please ensure you have typed one card.")
                    continue
                elif (card[0] not in self.deck_list):
                    print("Please ensure you have typed the correct card value.")
                    continue
                elif (self.card_num[self.deck_list.index(card[0])] == 0):
                    print("Please ensure you have typed the correct value.")
                else:
                    self.draw(card)
                    self.my_values.append(card[0])
                    break           
        elif turn == "dealer":
            while True:
                card = input().split()
                if len(card) != 1:
                    print("Please ensure you have typed one card.")
                    continue
                elif card[0] not in self.deck_list:
                    print("Please ensure you have typed the correct card value.")
                    continue
                elif (self.card_num[self.deck_list.index(card[0])] == 0):
                    print("Please ensure you have typed the correct value.")
                else:
                    self.draw(card)
                    self.dealer_cards.append(self.deck_dict[card[0]])
                    break
        elif turn == "dealer_blackjack":
            if self.dealer_cards[0] == 10:
                self.draw("A") # If the dealer draws a value that equals 10, the program operates under the assumption that the dealer must check their cards 
                #to see if they have drawn a blackjack. If they have achieved a blackjack and their initial value was worth 10, they must have drawn an ace.

                self.dealer_cards.append(1)
            else:
                while True:
                    dealer_bj = input("What card did the dealer draw?").split()
                    if (dealer_bj[0] != "10") & (dealer_bj[0] != "J") & (dealer_bj[0] != "Q") & (dealer_bj[0] != "K"):
                        print("Please ensure you have typed the correct card value: 10, J, Q, or K.")
                        continue
                    elif self.card_num[self.deck_list.index(dealer_bj[0])] == 0:
                        print("Please ensure you have typed the correct card value: 10, J, Q, or K.")
                        continue
                    else:
                        self.draw(dealer_bj)
                        self.dealer_cards.append(self.deck_dict[dealer_bj[0]])
                        break
 
    def check_others_initial_values(self):
        while len(self.player_cards) < (self.players-1)*2: # Check the cards that others have drawn based on number of players
            self.player_cards.clear()
            p_card = list(input().split())
            if len(p_card) != (self.players-1)*2:
                print("Please ensure you have typed the correct number of cards from other players.")
            else:
                for f in range(len(p_card)):
                    if p_card[f] in self.deck_list:
                        self.player_cards.append(p_card[f])
                    else:
                        print("Please ensure you have typed the correct card values from other players.")
                        f = 0
                        break
  
    def dealer_blackjack(self):
        if (self.dealer_cards[0] == 10) | (self.dealer_cards[0] == 1): # If the dealer draws a card worth 10 or an ace, they must check to see if they have drawn 
            while True:
                dealer_bj = input("Has the dealer received a blackjack? (Y/N)").upper()
                if dealer_bj == "Y":
                    if (self.dealer_cards[0] == 10) and (self.card_num[self.deck_list.index("A")] == 0):
                        print("There are no more aces left in the deck, it is not possible for the dealer to obtain a blackjack. Please type 'N' in the next prompt.")
                    else:
                        print("Unlucky!")
                        self.check_initial_values_deck("dealer_blackjack")
                        break
                elif dealer_bj == "N":
                    break
                else:
                    print("Please ensure you have typed 'Y' or 'N' correctly.") 
 
    def player_hit(self):
        while True:
            hit_card = input().split()
            if len(hit_card) != 1:
                print("Please ensure you have typed one card for each hit.")
                continue
            elif hit_card[0] == "0":
                break
            elif hit_card[0] not in self.deck_list:
                print("Please ensure you have typed the correct card value.")
                continue
            elif self.card_num[self.deck_list.index(hit_card[0])] == 0:
                print("Please ensure you have typed the correct value.")
                continue
            else:
                self.draw(hit_card)
                self.player_rehit()
                break     
  
    def self_hit(self):
        while True:
            hit_card = input().split()
            if len(hit_card) != 1:
                print("Please ensure you have inputted one card value for your hit.")
                continue
            elif hit_card[0] not in self.deck_list:
                print("Please ensure you have typed the correct card value.")
                continue
            elif self.card_num[self.deck_list.index(hit_card[0])] == 0:
                print("Please ensure you have typed the correct value.")
                continue
            else:
                self.draw(hit_card)
                self.my_running_sum.append(self.deck_dict[hit_card[0]])
                self.my_values.append(hit_card[0])
                self.current_self_value()
                if (sum(self.my_running_sum) == 21) or (sum(self.my_running_sum) == 11) and ("A" in self.my_values): # If you gain a blackjack after hitting, break
                    break
                self.self_rehit()
                break
 
    def self_rehit(self):
        if sum(self.my_running_sum) > 21: # The function should not run if your hand has a value above 21
            return
        else:
            self.probability(self.dealer_cards, "dealer")
            while True:
                again = input("Please choose to hit or stand on your current hand by typing 'hit' or 'stand'.").upper()
                if again == "HIT":
                    print("What value have you drawn?")
                    self.self_hit()
                    break
                elif again == "STAND":
                    break
                else:
                    print("Please ensure you have typed 'hit' or 'stand' correctly.") 
 
    def player_rehit(self):
        while True:
            again = input("Is the player hitting again? (Y/N)").upper()
            if again == "Y":
                print("What value has the player obtained?")
                self.player_hit()
                break
            elif again == "N":
                break
            else:
                print("Please ensure you have typed 'Y' or 'N' correctly.") 
 
    def end_of_round(self):
        while True:
            round_end = input("The current round has ended. Will you be playing another round? (Y/N)").upper()
            if round_end == "Y":
                break
            elif round_end == "N":
                print("The game will now end. Thank you for playing!")
                global in_play 
                in_play = False # Sets global game marker to false, shuts down the while loop below that initializes each round
                break
            else:
                print("Please ensure you have typed in 'Y' or 'N' correctly.")
                continue
 
    def reset_deck(self):
        while True:
            reset_deck = input("Has the deck been reset this round? (Y/N)").upper() # Decks are sometimes reset after a round, allows the player to reset the deck to their initial full values
            if reset_deck == "Y":
                global decks
                decks = [4*value] * 13
                break
            elif reset_deck == "N":
                break
            else:
                print("Please ensure you have typed 'Y' or 'N' correctly.")   
      
#initialize
print("Welcome to the Blackjack Cards and Probability Tracker! To begin, please input the following numbers:")
initialize_values_list = []
 
print("How many decks are you using?")
while True:
    value = int(input())       
    if value <= 0 or value > 8:
        print("Please ensure that you are entering a correct value.")
    else:
        global decks
        decks = [4*value] * 13
        break
 
def initialize_values(max):
    while True:
        value = int(input())       
        if value <= 0 or value > max:
            print("Please ensure that you are entering a correct value.")
        else:
            initialize_values_list.append(value)
            break
 
def initializer():
    print("How many players are playing, including yourself?")
    initialize_values(7)
    
    print("What number is your turn? (1 for going first, 2 for going second, etc.) If you are the only one playing, input '1'.")
    initialize_values(initialize_values_list[0])
    
    global play
    play = Deck(initialize_values_list[0], initialize_values_list[1])
 
initializer()
 
#rounds
while in_play == True:
    print("A new round has started.")
    
    if play.players > 1:
        print("In a space-separated line, please enter the cards drawn by other players before the round.")
        play.check_others_initial_values()
        play.draw(play.player_cards)
    
    print("In a space-separated line, please enter the two cards you have received.")
    play.check_initial_values_deck("my_turn")
    
    print("In a space-separated line, please enter the the card the dealer drew.")
    play.check_initial_values_deck("dealer")
    play.dealer_blackjack()
  
    if len(play.dealer_cards) == 2: # If the dealer has obtained a blackjack, they would have two values drawn under the dealer cards list. Given that a round immediately ends after a dealer draws blackjack, this stops the loop.
        play.end_of_round()
        if in_play == False:
            break
        else:
            print("You have chosen to play another round.")
            play.reset_deck()
            initialize_values_list.clear()
            play.blackjack = False
            play.my_values.clear()
            play.my_running_sum.clear()
            play.player_cards.clear()
            play.dealer_cards.clear()
            initializer()
            continue
    
    print("The hit/stand process begins.")
    if play.players > 1:
        for w in range(1, play.players+1): # Your probability depends on what order you play in with other players
            if w == play.place:
                print("It is now your turn.")
                play.self_cards()
            else:
                print("It is another player's turn - please input the single card value if they have chosen to hit. If they have chosen to stand, please type '0'.")
                play.player_hit()
    else:
        print("It is now your turn.")
        play.self_cards()
            
    print("It is the dealer's turn to reveal their card. Please first input the card value that the dealer has turned over.")
    play.check_initial_values_deck("dealer")
    while sum(play.dealer_cards) < 17: # The dealer keeps drawing until 17
        print("Please input the next card that the dealer has drawn.")
        play.check_initial_values_deck("dealer")
    print("The dealer has finished drawing.")
    
    play.end_of_round()
    if in_play == False:
        break
    else:
        print("You have chosen to play another round.")
        play.reset_deck()
        initialize_values_list.clear()
        play.blackjack = False
        play.my_values.clear()
        play.my_running_sum.clear()
        play.player_cards.clear()
        play.dealer_cards.clear()
        initializer()
        continue
