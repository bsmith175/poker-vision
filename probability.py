import math

def choose_function(cards):
    num_cards = len(cards)
    if num_cards == 2:
        return opening_probability(cards)
    else:
        #compute_probability(cards)
        pass
        
#based on the Chen formula for opening hand strength https://www.thepokerbank.com/strategy/basic/starting-hand-selection/chen-formula/
def opening_probability(cards):
    highest = larger_card(cards[0][0], cards[1][0])
    pairs = 1
    if highest == 0:
        highest = cards[0][0]
        pairs = 2
    score = 0
    #Step 1: compute highest card
    if highest == 14:
        score += 10
    elif highest == 13:
        score += 8
    elif highest == 12:
        score += 7
    elif highest == 11:
        score += 6
    else:
        score = highest/2
    #Step 2: multiply pairs
    score *= pairs
    if pairs == 2 and score < 5:
        score = 5
    #Step 3: check for matching suits
    if (cards[0][1] == cards[1][1]):
        score += 2
    #Step 4: calculate distance between cards
    gap = abs(cards[0][0] - cards[1][0])
    if gap < 3:
        score -= gap
    elif gap == 3:
        score -= 4
    else:
        score -= 5
    #Step 5: Give straight bonus
    if highest < 12 and gap <= 1:
        score += 1
    #Step 6 and 7: Round then calculate probability
    #Pocket aces have an 85% chance on average to win, so we divide the score by 23.5 (20, the score for pocket aces  divided by .85, the odds)
    return (math.ceil(score))



def larger_card(card1, card2):
    if card1 > card2:
        return card1
    if card2 > card1:
        return card2
    return 0


if __name__  == "__main__":
    cards = [(3, "d"), (8, "h")]
    choose_function(cards)