import pandas as pd
import math
 
deck_dict = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
deck_list = list(deck_dict.keys())
 
class Initialize:
    def __init__(self):
        self.statements = ["How many decks are you using?", "How many players are playing this round?", "What is your turn number? (1 for going first, 2 for going second, etc.) If you are the only one playing, input '1'."]
        self.initialize = [0] * 3 # append input values for deck number, player number, turn number
        self.cards = [] # number of cards in deck
        self.in_play = True

    def inputs(self):
        for i in range(3):
            max = [8,7, self.initialize[1]]
            print(self.statements[i])
 
            while True:
                value = int(input())
                if (value <= 0) or (value > max[i]):
                    print("Please ensure that you are entering a correct value.") 
                else:
                    self.initialize[i] = value
                    break                     
 
        self.cards = [4*self.initialize[0]] * 13
        return self.initialize
 
    def end_round(self):
        while True:
            round_end = input("The current round has ended. Will you be playing another round? (Y/N)").upper()
            if round_end == "Y":
                break
            elif round_end == "N":
                print("The game will now end. Thank you for playing!")
                self.in_play = False
                break
            else:
                print("Please ensure you have typed in 'Y' or 'N' correctly.")
                continue
 
class Draw_values:
    def __init__(self):
        self.cards_drawn = [] # string values
        self.values = [] # numeric values
  
    def draw(self, player_num):
        while len(self.cards_drawn) < (player_num-1)*2: # Check the cards that others have drawn based on number of players
            self.cards_drawn.clear() # reset list if input is mistake
            card = list(input().split())
            if len(card) != (player_num-1)*2:
                print("Please ensure you have typed the correct number of cards.")
                continue
            else:
                for c in card:
                    if (c in deck_list) and (initialize.cards[deck_list.index(c)] > 0):
                        self.cards_drawn.append(c)
                        self.values.append(deck_dict[c])
                    else:
                        print("Please ensure you have typed the correct card values.")
                        c = 0
                        break
        return [self.cards_drawn, self.values]
 
    def card_remove(self, remove_values):
        for x in range(len(remove_values)):
            index_value = deck_list.index(remove_values[x])
            initialize.cards[index_value] -= 1
 
        tracker = {"Card Values": deck_list, "Number of Cards Left in the Deck": initialize.cards}
        print(pd.DataFrame(tracker))
 
class Dealer_Moves:
    def __init__(self, values):
        self.cards = values[0]
        self.values = values[1]
        self.blackjack = False
 
    def dealer_blackjack(self):
        second_value = ""
        if (self.values[0] == 10) | (self.values[0] == 1):
            while True:
                dealer_bj = input("Has the dealer received a blackjack? (Y/N)").upper()
                if dealer_bj == "Y":
                    if (self.values[0] == 10) and (initialize.cards[deck_list.index("A")] > 0):
                        print("Unlucky!")
                        self.blackjack = True
                        second_value = "A"
                        break
                    elif (self.values[0] == 1):
                        print("What card did the dealer draw?")
                        while True:
                            ace_blackjack = str(input())
                            if (ace_blackjack in deck_list) and (deck_dict[ace_blackjack] == 10) and (initialize.cards[deck_list.index(ace_blackjack)] > 0):
                                self.blackjack = True
                                second_value = ace_blackjack
                                break
                            else:
                                print("Please ensure you have typed the correct card value: 10, J, Q, or K.")
                                continue
                        break
                    else:
                        print("Please ensure you have correctly verified the dealer's blackjack.")
                        continue
                elif dealer_bj == "N":
                    break
                else:
                    print("Please ensure you have typed 'Y' or 'N' correctly.")
                    continue
        return [self.blackjack, second_value]
    
    def dealer_draws(self):
        while sum(self.values) < 17: # dealer keeps drawing until they reach a total value of 17
            print("Please input the dealer's next card drawn.")
            dealer_cards = Draw_values()
            dealer_hit = dealer_cards.draw(1.5)
            dealer_cards.card_remove(dealer_hit[0])
            self.cards += dealer_hit[0]
            self.values += dealer_hit[1]
            print(f"The dealer's total is {sum(self.values)}.")
        if sum(self.values) == 21:
            print("Unlucky, the dealer received a blackjack.")
 
class Current_Value:
    def __init__(self, self_cards, self_values):
        self.self_cards = self_cards
        self.self_values = self_values
        self.sum = sum(self_values)
        self.split = False
        self.blackjack = False
        self.over_21 = False
     
    def value_in_hand(self):
        if "A" in self.self_cards:
            if (self.sum == 11) or (self.sum == 21): # Ace is listed as having a value of 1 in the deck dictionary, therefore immediately having a value of 10 + ace (11) would mean you'd have a blackjack.
                print("You have achieved a natural/blackjack! Your turn with your current hand is now finished.")
                self.blackjack = True
                return
            else:
                if (self.sum+10) < 21:
                    print(f"Your current value in your hand is {self.sum} or {self.sum+10}.") # Ace represents a 1 or 11 in value
                    #self.probability([total, total+10], "my_turn")
                else:
                    print(f"Your current value in your hand is {self.sum}.")
                    #self.probability([total], "my_turn")
 
        elif self.sum == 21: # If total in your hand equals 21 without the help of an ace
            print("You have achieved a natural/blackjack! Your turn with your current hand is now finished.")
            self.blackjack = True
            return
        elif self.sum > 21:
            print(f"The current value in your hand is {self.sum}. You have drawn a hand over 21, your turn will now end.")
            self.over_21 = True
            return
        else:
            print(f"The current value in your hand is {self.sum}.")
            if self.sum < 21:
                pass
                #self.probability([total], "my_turn")
 
class Split_Play:
    def __init__(self, self_cards, self_values):
        self.self_cards = self_cards
        self.self_values = self_values
        self.sum = sum(self_values)
        self.split = False
 
    def split_cards(self):
        if self.self_cards[0] == self.self_cards[1]:
            while True:
                pass_option = input("You may choose to split. Proceed? (Y/N)").upper()
                if pass_option == "Y":
                    self.split = True
                    break
                elif pass_option == "N":
                    # regular play
                    break
                else:
                    print("Please ensure you have typed 'Y' or 'N' correctly.")
 
    def split_play(self):
        if self.self_cards[0] == "A": # Special case of drawing two aces in your hand, this program assumes the casino only allows you to draw one card on each split ace.
            print("Since you have drawn two aces, you will draw two cards per split ace and will not be able to draw again.")
            for i in range(2):
                # Probability
                if i == 0:
                    print("Please input the card value that you have received on your first ace.")
                else:
                    print("Please input the card value that you have received on your second ace.")
                ace_split_draw = Draw_values().draw(1.5)
                Draw_values().card_remove(ace_split_draw[0])
                Current_Value([self.self_cards[0]]+ace_split_draw[0], [self.self_values[0]]+ace_split_draw[1]).value_in_hand()
        else: # Regular non-ace split
            for j in range(2):
                split_value = Current_Value([self.self_cards[j]], [self.self_values[j]])
                if j == 0:
                    print(f"You will be able to draw on both cards. The current value in your left hand is {self.self_values[j]}. Please play the hand on your left first.")
                else:
                    print("Now, please play the hand on your right.")
                
                split = Hit_Stand("you")
                while split_value.over_21 == False:
                    print("Please choose to hit or stand on your hand by inputting 'hit' or 'stand'.")
                    
                    split_draw = split.hit_stand_choice()
                    if split.stand == False:
                        self.self_cards += split_draw[0]
                        self.self_values += split_draw[1]
                        split_value = Current_Value(self.self_cards[1:], self.self_values[1:])
                        split_value.value_in_hand()
                        Probability(self.self_cards, [sum(self.self_values)]).probability_calculate_self()
                        Probability(dealer_draw[0], dealer_draw[1]).probability_calculate_dealer()
                    else:
                        break

                self.self_cards = self.self_cards[0:2]
                self.self_values = self.self_values[0:2]
            # Probability

class Hit_Stand:
    def __init__(self, player):
        self.player = player
        self.stand = False
    
    def hit_stand_choice(self):
        while True:
            player_decision = input().lower()
            if player_decision == 'hit':
                print(f"Please input the value that has been drawn by {self.player}.")
                player_hit = Draw_values()
                player_hit_values = player_hit.draw(1.5)
                player_hit.card_remove(player_hit_values[0])
                
                if self.player == "the player":
                    print(f"If {self.player} chose to hit again, please type 'hit'. Otherwise, if {self.player} chose to stand, type in 'stand'.")
                    continue
                else:
                    return player_hit_values
            elif player_decision == 'stand':
                self.stand = True
                break
            else:
                print("Please ensure you have typed 'hit' or 'stand' correctly.") 
                continue

class My_Turn:
    def __init__(self, self_cards, self_values):
        self.self_cards = self_cards
        self.self_values = self_values
        self.sum = sum(self_values)

    def play_decision(self):
        my_turn = Current_Value(self.self_cards, self.self_values)
        my_turn.value_in_hand()
        if my_turn.blackjack == True:
            return
        
        Probability(self.self_cards, [self.sum]).probability_calculate_self()
        Probability(dealer_draw[0], dealer_draw[1]).probability_calculate_dealer()
        split_option = Split_Play(self.self_cards, self.self_values)
        split_option.split_cards()
        if split_option.split == True:
            print("You have chosen to split.")
            split_option.split_play()
        else:
            turn = Hit_Stand("you")
            while (my_turn.over_21 == False) and (my_turn.blackjack == False):
                print("Please choose to hit or stand on your hand by inputting 'hit' or 'stand'.")
                next_move = turn.hit_stand_choice()
                if turn.stand == False:
                    self.self_cards += next_move[0]
                    self.self_values += next_move[1]
                    my_turn = Current_Value(self.self_cards, self.self_values)
                    my_turn.value_in_hand()
                    print(self.self_values)
                    if sum(self.self_values) < 21:
                        Probability(self.self_cards, [sum(self.self_values)]).probability_calculate_self()
                        Probability(dealer_draw[0], dealer_draw[1]).probability_calculate_dealer()
                else:
                    break

class Probability:
    def __init__(self, cards, values):
        self.cards = cards
        self.values = values # list object of sum numerical values [17]
    
    def probability_calculate_self(self):
        if "A" not in self.cards:
            base_value = self.values[0]
            hit_list = list(range(base_value + 1, base_value + 12)) # Range is 11 given that an ace can represent 1 or 11
            prob_list = []
            
            for y in range(0, 9):
                probability = (math.comb(initialize.cards[y], 1)) / (math.comb(sum(initialize.cards)-1, 1)) # Use combination formula to measure probability of drawing each value out of the remaining cards in the deck.
                prob_list.append(probability)
            
            # Since 10 + J + Q + K all equal 10, tens probability must be calculated separately by summing the number of 10, J, Q, and K cards left.
            tens_probability = math.comb(sum(initialize.cards[-4:]), 1) / (math.comb(sum(initialize.cards)-1, 1))
            prob_list.append(tens_probability)
            
            #Since ace counts as 11, this simply equals the probability of drawing +1.
            elevens_probability = math.comb(initialize.cards[0], 1) / (math.comb(sum(initialize.cards)-1, 1))
            prob_list.append(elevens_probability)
            
            print("These are your probabilities:")
            print(pd.DataFrame({"Possible Hit Values": hit_list, "Probability": prob_list}))

            if base_value == 10:
                print("You have a 100% chance of drawing a value that keeps you 21 or under. Your probability of drawing a Blackjack next round is", "{:.4%}".format(prob_list[hit_list.index(21)]) + ".")
            elif (21 in hit_list) and (base_value < 21):
                under_21_prob = sum(prob_list[0:hit_list.index(21)+1])
                if under_21_prob >= 1:
                    under_21_prob = 1
                print("You have a", ("{:.4%}".format(under_21_prob)), "chance of drawing a value that keeps you 21 or under. Your probability of drawing a Blackjack next round is", "{:.4%}".format(prob_list[hit_list.index(21)]) + ".")
            elif base_value < 21: # If your current value in your hand is too small to reach 21 in the next draw (you have a value of 10 or less).
                print("You have a 100% chance of drawing a value that keeps you 21 or under. However, you don't have a high enough value to obtain a Blackjack in the next round.")
        else:
            base_value = self.values[0]
            hit_list = list(range(base_value + 1, base_value + 22)) # Range is 21 since the ace can represent 1 or 11
            prob_list = []

            for x in range(2):
                for y in range(9):
                    probability = (math.comb(initialize.cards[y], 1)) / (math.comb((sum(initialize.cards)-1), 1)) # Subtract one from the total to represent the hidden card drawn by the dealer not present in the deck
                    prob_list.append(probability)

                tens_probability = math.comb(sum(initialize.cards[-4:]), 1) / (math.comb(sum(initialize.cards)-1, 1))
                prob_list.append(tens_probability)

                # We don't append the probability of drawing 11 to the initial value to the first iteration, only the second, since the probability of drawing +11 will be replaced by the next iteration representing base_value +10 +1.
                if x == 1:
                    elevens_probability = math.comb(initialize.cards[0], 1) / (math.comb((sum(initialize.cards)-1), 1))
                    prob_list.append(elevens_probability)
        
            print(pd.DataFrame({"Possible Hit Values": hit_list, "Probability": prob_list}))


            under_21_prob = sum(prob_list[hit_list.index(base_value+11):hit_list.index(21)+1])
            print(f"You are 100% guaranteed to stay below 21, however if you are counting from {base_value+10}, your probability of staying below 21 is", ("{:.4%}".format(under_21_prob)), "and your probability of drawing a Blackjack next round is", "{:.4%}".format(prob_list[hit_list.index(21)]) + ".")
    
    def probability_calculate_dealer(self):
        base_value = self.values[0]
        hit_list = list(range(base_value + 1, base_value + 12)) # Range is 11 given that an ace can represent 1 or 11
        prob_list = []

        for y in range(0, 9):
            probability = (math.comb(initialize.cards[y], 1)) / (math.comb(sum(initialize.cards), 1)) 
            prob_list.append(probability)
    
        tens_probability = math.comb(sum(initialize.cards[-4:]), 1) / (math.comb(sum(initialize.cards), 1))
        prob_list.append(tens_probability)
        
        #Since ace counts as 11, this simply equals the probability of drawing +1.
        elevens_probability = math.comb(initialize.cards[0], 1) / (math.comb(sum(initialize.cards), 1))
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

# start round
print("Welcome to the Blackjack Cards and Probability Tracker! To begin, please input the following numbers:")
initialize = Initialize() # properties of game being played
round = initialize.inputs() # list of round initialized inputs
 
while initialize.in_play == True:
    print("A new round has started.")
  
    if round[1] > 1:
        print("In a space-separated line, please enter the cards drawn by other players before the round.")
        player_cards = Draw_values()
        player_draw = player_cards.draw(round[1])
        player_cards.card_remove(player_draw[0])
 
    print("In a space-separated line, please enter the two cards you have received.")
    self_cards = Draw_values()
    self_draw = self_cards.draw(2)
    self_cards.card_remove(self_draw[0])
  
    print("In a space-separated line, please enter the single card the dealer drew.")
    dealer_cards = Draw_values()
    dealer_draw = dealer_cards.draw(1.5)
    dealer_cards.card_remove(dealer_draw[0])
    dealer_blackjack = Dealer_Moves(dealer_draw).dealer_blackjack()
 
    if dealer_blackjack[0] == True:
        dealer_cards.card_remove([dealer_blackjack[1]])
        print("The round will now end.")
        break
  
    print("The hit/stand process begins.")
    if round[1] > 1:
        for w in range(1, round[1]+1): # Your probability depends on what order you play in with other players
            if w == round[2]:
                print("It is now your turn.")
                self_turn = My_Turn(self_draw[0], self_draw[1])
                self_turn.play_decision()
            else:
                print("It is another player's turn - please type in 'hit' if they have chosen to hit or 'stand' if they have chosen to stand.")
                Hit_Stand("the player").hit_stand_choice()
    else:
        print("It is now your turn.")
        self_turn = My_Turn(self_draw[0], self_draw[1])
        self_turn.play_decision()

    print("It is the dealer's turn to reveal their card.")
    Dealer_Moves(dealer_draw).dealer_draws()
  
    initialize.end_round()
