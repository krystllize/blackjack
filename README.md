# blackjack
Deck and probability tracker for a typical game of blackjack. 

This script aims to track the objective progress and probabilities of the cards in play during a blackjack game. Each turn provides the player with an overview of which cards are left in the deck and what probabilities they have in drawing optimal hands. The player must input which cards are drawn throughout the game as prompted.

Given the objective nature of the script, bet suggestions and strategy suggestions are not included. The player must make their own subjective decision what strategy to play during the game.

Given that each casino outlines different rules surrounding blackjack, the most common assumptions used in blackjack are used in this script:
- Aces are considered as a value of 1 or 11
- Dealer draws until 16 and must stand on 17 or above
- A deck is comprised of the standard 52 cards
- All cards from all players are made visible, and only the first card that the dealer draws is revealed
- If a dealer draws a card of value 10 (10, J, Q, K) or an Ace, they must check and confirm to all players whether or not they have received a blackjack after all players have received their cards. If the dealer immediately receives a blackjack, the round ends immediately.
- If a player receives two cards of the same denomination (e.g. two 7s), they have the option to split and play each card as a separate hand. Only one split can be made on the initial hand.
- If a player receives two aces, the hand is automatically split, and you may only draw one card on each split ace.
- The program assumes that a same number of players will be playing each round, and that each player's turn number will remain the same across all rounds
- Probabilities of the dealer drawing high values (17+) is provided to the player before they choose to hit or stand, to provide them with additional information to make their decision
