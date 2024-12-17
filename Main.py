import random
import sys

HEARTS = chr(9829)  # Character 9829 is ♥.
DIAMONDS = chr(9830)  # Character 9830 is ♦.
SPADES = chr(9824)  # Character 9824 is ♠.
CLUBS = chr(9827)  # Character 9827 is ♣.
BACKSIDE = 'backside'

def main():
    print("Rules:\nTry to get as close to 21 without going over.")

    money = 5000

    while True:  # Game loop
        if money <= 0:
            print("You need more money.")
            print('Thanks for playing!')
            sys.exit()

        print(f'Money: {money}')

        bet = getBet(money)

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Handle player actions:
        print(f'Bet: {bet}')

        while True:  # Player's turn
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break  # Bust

            move = getMove(playerHand, money - bet)

            if move == 'D':  # Double down
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Bet increased to {bet}.')

            if move in ('H', 'D'):  # Hit or double down
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}.')
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    break  # Bust

            if move in ('S', 'D'):  # Stand or double down
                break

        # Dealer's turn:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)
                if getHandValue(dealerHand) > 21:
                    break  # Dealer busts

                input('Press Enter to continue...')
                print('\n\n')

        # Show final hands:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        # Determine outcome:
        if dealerValue > 21:
            print(f'Dealer busts! You win ${bet}!')
            money += bet
        elif playerValue > 21 or playerValue < dealerValue:
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print(f'You won ${bet}!')
            money += bet
        elif playerValue == dealerValue:
            print("It's a tie, the bet is returned to you.")

        input('Press Enter to continue...')
        print('\n\n')

# Function for getting the player's bet
def getBet(maxBet):
    while True:
        print(f'How much do you want to bet? (1-{maxBet}, or QUIT to exit)')
        bet = input('> ').upper().strip()

        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)

        if 1 <= bet <= maxBet:
            return bet

# Function for getting the deck of cards
def getDeck():
    deck = []

    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck

# Function to display the hands of the player and dealer
def displayHands(playerHand, dealerHand, showDealerHand):
    print()

    if showDealerHand:
        print(f'DEALER: {getHandValue(dealerHand)}')
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards([BACKSIDE] + dealerHand[1:])

    print(f'PLAYER: {getHandValue(playerHand)}')
    displayCards(playerHand)

# Function to get the hand value
def getHandValue(cards):
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0]

        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    value += numberOfAces

    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value

# Function to display the cards
def displayCards(cards):
    rows = ['', '', '', '', '']

    for card in cards:
        rows[0] += ' ___  '

        if card == BACKSIDE:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} | '
            rows[2] += f'| {suit} | '
            rows[3] += f'|_{rank.rjust(2, "_")}| '

    for row in rows:
        print(row)

# Function to get the player's move
def getMove(playerHand, money):
    while True:
        moves = ['(H)it', '(S)tand']

        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()

        if move in ('H', 'S'):
            return move

        if move == 'D' and '(D)ouble down' in moves:
            return move

if __name__ == "__main__":
    main()
