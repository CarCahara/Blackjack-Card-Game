# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:04:42 2019

@author: eedo

Simple Blackjack game
"""

#Import random for deck shuffling
import random 

#Declare deck card variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

#Declare game flow control variable
playing = True

#Create Card class with each card having suit and rank
class Card():
    
    def __init__(self, suit, rank): #initialise attributes
        
        self.suit = suit
        self.rank = rank
    
    
    def __str__(self): #add method for printing a card
        return f"{self.rank} of {self.suit}"

#Create Deck class that holds 52 cards that can be shuffled
class Deck():
    
    
    def __init__(self): #initialise attributes
        
        self.deck = [] #start with an empty list to fill
        
        for suit in suits: #iterate over all cards and append the Card class to the deck
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self): #print the deck method
        
        deck_comp = '' #start of with empty string
        for card in self.deck:
            deck_comp += card.__str__() + '\n' #append every card class in deck to the string
        return f"The deck has {self.deck.__len__()} cards: \n" + deck_comp #return the deck size and cards in the deck
    
    def __len__(self): #define len func to return deck size
        
        return len(self.deck)
       
    def shuffle(self): #define shuffle method
        
        random.shuffle(self.deck)
    
    def deal(self): #pop last card of the deck and return its value
        
        single_card = self.deck.pop() 
        return single_card
        
    
#Create Hand class that holds dealt hands and calculates value
class Hand():
    
    def __init__(self): #initialise attributes
        
        self.cards = [] #start with an empty list
        self.value = 0 #start with zero value
        self.aces = 0 #aces in hand count
    
    def  __str__(self):
        
        hand_comp = '' #start with empty string
        for card in self.cards:
            hand_comp += card.__str__() + ', ' #append every card class in hand to the string
        return 'Cards in hand: ' + hand_comp + '\nValue: ' + str(self.value)
        
    def add_card(self, card):
        
        self.cards.append(card) #append card called from the deal method of Deck class
        self.value += values[card.rank] #passing a Card class allows card.rank to be called
        
        if card.rank == 'Ace': #add to aces count if added card is ace
            self.aces += 1
    
    def adjust_for_ace(self):
        
        while self.value > 21 and self.aces: #if over 21 use an ace to reduce value by 10 and reduce ace count by 1
            self.value -= 10
            self.aces -= 1

#Create Chips class that hold player chips
class Chips():
    
    def __init__(self, total = 100): #initialise attributes
        
        self.total = total #set starting values for total and bet
        self.bet = 0
        
    def win_bet(self): #add bet to total
        
        self.total += self.bet
        
    def lose_bet(self): #substract bet from total
        
        self.total -= self.bet
        
def take_bet(chips): #Take the bet amount
    
    while True: #iterate until input is valid
        
        try: #take number input
            chips.bet = int(input("Place your bet: "))
        except: #if not number
            print("Bet needs to be a number.")
        else: #if it is number check that it doesn't exceed chip stack
            if chips.bet > chips.total:
                print (f"Bet amount exceeds your chip stack. You have {chips.total} chips.")
            else: #break out of the loop if bet is valid
                break
def hit(deck, hand): #Define hit function that adds a card to the hand from the deck and adjust for ace if bust
    
    hand.add_card(deck.deal()) #call the .add_card() method from the Hand class to add a card by calling the .deal() method from the Deck class
    hand.adjust_for_ace() #adjust hand value for aces if over 21 using adjust_to_ace() method from the Hand class    

#Now that all classes needed are defined, we move on to defining functions to control the game
    
def decision(deck, hand): #Define decision function that asks the player to hit or stay
    
    global playing #using the global playing variable to control the while loop
    
    while True:
        x = input("Hit or Stay? Enter 'h' or 's': ")
        
        if x[0].lower() == 'h':
            hit(deck, hand)
            print("\nPLAYER'S HAND: ")
            print(*player.cards, sep = '\n') #print vertically
        elif x[0].lower() == 's':
            print("Player stays. Dealer's Turn.")
            playing = False
        else:
            print("Invalid input.")
            continue
        break
    
#Functions to display cards in hands
        
def show_some(player, dealer): #show all player's cards and one of dealer's cards 
    
    print("\nDEALER'S HAND: ")
    print(f"<card hidden>, {dealer.cards[1]}") #print in row
    print("\nPLAYER'S HAND: ")
    print(*player.cards, sep = ', ') #print in row

def show_all(player, dealer): #show all cards in hands

    print("\nDEALER'S HAND: ", *dealer.cards, sep = '\n') #print vertically
    print("DEALER'S HAND VALUE: ", dealer.value)
    print("\n\nPLAYER'S HAND: ", *player.cards, sep = '\n') #print vertically
    print("PLAYER'S HAND VALUE: ", player.value)
    
#Now we will write functions for end of game scenarios: busts and wins + push
#These will take in 'player, dealer, chips' represented by player and dealer Hands and player's chip stack

def player_busts(player, dealer, chips): #player's hand value over 21
    
    print("Player busts!")
    chips.lose_bet()
    
def player_wins(player, dealer, chips): #player's hand value higher than dealer's
    
    print("Player wins!")
    chips.win_bet()
    
def dealer_busts(player, dealer, chips): #dealer's hand value over 21
    
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips): #dealer's hand value higher tahn player's
    
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player, dealer): #both player and dealer got 21 - no chip change
    
    print("Dealer and Player tie!")
    
#Now we have everything needed for the game and it's time for final programming of the game!
    
while True:
    
    print("Welcome to a 'S17' variation of Blackjack! \nThe deck will reset after each hand!") #Opening message
    print("\nDealing cards...")
    deck = Deck() #create a deck
    deck.shuffle() #shuffle the deck
    
    player = Hand() #create empty player'hand
    player.add_card(deck.deal()) #deal first card to player
    player.add_card(deck.deal()) #deal second card to player
    
    dealer = Hand() #create empty dealer's hand
    dealer.add_card(deck.deal()) #deal first card to dealer
    dealer.add_card(deck.deal()) #deal second card to dealer
    
    chips = Chips() #set player's chips (default 100)
    
    show_some(player, dealer) #show the cards
    
    print(f"\nYou have {chips.total} chips. Use them wisely!")
    
    take_bet(chips) #prompt player for a bet using the chip stack available
    
    while playing: #while playing (meaning player did not choose 'Stay') is true ask player for hit or stay decision
        
        decision(deck, player)
        
        if player.value > 21: #if over 21 player busts and break out of loop
           
            player_busts(player, dealer, chips)
            break
            
        
       #If player did not bust, game goes on meaning dealer hits until dealer's hand value is at least 17 (S17 variation)
    if player.value <= 21:
        
        while dealer.value < 17:
        
            hit(deck, dealer)
    
        show_all(player, dealer) #show all cards now that dealer has finished playing
    
    #check for end game scenarios
        if dealer.value > 21:
            dealer_busts(player, dealer, chips)
        elif dealer.value > player.value:
            dealer_wins(player, dealer, chips)
        elif dealer.value < player.value:
            player_wins(player, dealer, chips)
        else:
            push(player, dealer)
        
    #Print out chip total after game
    print(f"\nYou have {chips.total} chips left.")
    if chips.total == 0: #break if all chips lost
        print("You're out of chips... Thanks for playing!")
        break
    
    #ask for new game
    new_game = input("Another game ('y' / 'n'): ")
    if new_game[0].lower() == 'y':
        playing = True #reset playing value to True (has been set to False if player chose to 'Stay')
        continue #Continue the game loop
    else: #break out of the game loop
        print("Thanks for playing!")
        break
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    