import math

def choose_function(cards):
    num_cards = len(cards)
    score = 0
    if num_cards == 2:
        score = opening_probability(cards)
    else:
        score = flop_probability(cards)
    print(hand_ranking(score))
    print(best_hand(cards))
        
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
    return (math.ceil(score))

def flop_probability(cards):
    highest = largest_card(cards)
    pairT = pairs(cards)
    pair_score = 1
    if pairT[1] == 2:
        pair_score = (pairT[0]-1) * 3
    else:
        pair_score = math.ceil(pow(pairT[0]-1, 2.5)) + pairT[1]
    score = 0
    #Step 1: compute highest card

    
    #Step 2: multiply pairs
 
    #Step 3: check for matching suits
    flush_num = flush(cards)
    flush_score = 1
    if flush_num == 4:
        score += 2 * (-len(cards) + 7)
    if flush_num == 5:
        flush_score = 3.5
    #Step 4: calculate distance between cards
    straight_num = straight(cards)
    straight_score = 1
    if straight_num == 4:
        score += 2 * (-len(cards) + 7)
    if straight_num == 5:
        straight_score = 3.25
    
    if pair_score != 1 and straight_score == 1 and flush_score == 1:
        highest = pairT[-2]
        if pairT[1] == 2:
            highest = larger_card(pairT[-1], pairT[-2])
    if highest == 14:
        score += 10
    elif highest == 13:
        score += 8
    elif highest == 12:
        score += 7
    elif highest == 11:
        score += 6
    else:
        score = math.ceil(highest/2) + 1

    straight_flush_score = straight_score * flush_score
    multiplier = max(pair_score, straight_flush_score)
    multiplier = multiplier
    score *= multiplier
    #Step 6 and 7: Round then calculate probability
    print("Hand Score: " + str(score))
    return (math.ceil(score))

def larger_card(card1, card2):
    if card1 > card2:
        return card1
    if card2 > card1:
        return card2
    return 0

def largest_card(cards):
    ret = 0
    for i in cards:
        if i[0] > ret:
            ret = i[0]
    return ret

def pairs(cards):
    card_vals = {}
    vals = []
    for i in cards:
        if i[0] in card_vals.keys():
            card_vals[i[0]] += 1
        else:
            card_vals[i[0]] = 1
    for j in card_vals.items():
        vals.append(j)
    vals.sort(key = lambda x : x[1])
    if (vals[-1][1] + vals[-2][1] >= 5):
        vals[-2] = (vals[-2][0], (5 - vals[-1][1]))
    #returns (highest frequency, second highest frequency, key of highest, key of second highest)
    return (vals[-1][1], vals[-2][1], vals[-1][0], vals[-2][0])

def flush(cards):
    suits = {}
    count = 1
    for i in cards:
        if i[1] in suits.keys():
            suits[i[1]] += 1
        else:
            suits[i[1]] = 1
    for j in suits.values():
        if j > count:
            count = j
    if count > 5:
        count = 5
    return count

def straight(cards):
    nums = []
    for j in cards:
        nums.append(j[0])
    nums.sort()
    prev = 0
    count = 1
    ret = 1
    for i in nums:
        curr = i
        if curr == prev + 1:
            count += 1
        else:
            count = 1
        if count > ret:
            ret = count
        prev = curr
    if ret > 5:
        ret = 5
    return ret

def hand_ranking(score):
    if score >= 25:
        return "Excellent hand that is likely to win"
    elif score >= 15:
        return "Very good hand"
    elif score >= 10:
        return "Decent hand"
    elif score >= 5:
        return "Questionable hand"
    else:
        return "Bad Hand"

def best_hand(cards):
    best_hand = ""
    if largest_card(cards) <= 10:
        best_hand = "High Card: " + str(largest_card(cards))
    if largest_card(cards) == 11:
        best_hand = "High Card: Jak"
    if largest_card(cards) == 12:
        best_hand = "High Card: Queen"
    if largest_card(cards) == 13:
        best_hand = "High Card: King"
    if largest_card(cards) == 14:
        best_hand = "High Card: Ace"
    if pairs(cards)[:-2] == (2,1):
        best_hand = "Pair"
    if pairs(cards)[:-2] == (2,2):
        best_hand = "Two Pair"
    if pairs(cards)[:-2] ==(3,1):
        best_hand = "Threesome"
    if straight(cards) == 5:
        best_hand = "Straight"
    if flush(cards) == 5:
        best_hand = "Flush"
    if pairs(cards)[:-2] == (3, 2):
        best_hand = "Full House"
    if pairs(cards)[:-2] == (4, 1):
        best_hand = "Four of a kind"
    if straight(cards) == 5 and flush(cards) == 5:
        best_hand = "Straight Flush"
    if straight(cards) == 5 and flush(cards) == 5 and largest_card(cards) == 14:
        best_hand = "ROYAL FLUSH!"
    return "Your best hand is a " + best_hand
    
if __name__  == "__main__":
    cards = [(11, 2), (2, 1), (2, 1), (2, 1), (11, 2), (11, 3), (11, 4)]
    choose_function(cards)