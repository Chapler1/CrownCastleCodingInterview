import requests

"""
Summary:
    This solution breaks up the process into 6 different test steps. There is a counter that
    tracks how many steps passed, where the process failed (if it did), and prints the reason
    for failing. The process checks for empty responses and null cards, but does not check for
    things like:
        - Correct number of cards in a deck
        - All the correct cards present in deck
        - Deck was actually shuffled (order changed)
        - Cards were dealt randomly
    With more time, these features could be added.
"""

# To Run:
    # I used Python 3.9.1
    # pip install requests


# Sends get request to API, if we recieve successful status code, site is up and we return true. 
# If we get something else, we return false. 
def check_site_up(url="https://deckofcardsapi.com"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Site is up.")
            return True
        else:
            print("Site is down.")
            return False
    except Exception as e:
        print(f"Failed to connect to {url}: {e}")
        return False

# Make a get request to the new deck url. If we recieve a successful status code and the deck ID is
# not null, return true.
def get_new_deck():
    new_deck_url = "https://deckofcardsapi.com/api/deck/new/"
    response = requests.get(new_deck_url)
    if response.status_code == 200 and response.json()['success']:
        deck_id = response.json()['deck_id']
        if deck_id is None:
            return False
        print("New deck acquired. Deck ID:", deck_id)
        return deck_id
    else:
        print("Failed to get a new deck.")
        return False

# Make a get request to the new deck url. If we recieve a successful status code, return true.
# Given more time, we could add logic to check whether the deck was actually shuffled.
def shuffle_deck(deck_id):
    shuffle_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/"
    response = requests.get(shuffle_url)
    if response.status_code == 200 and response.json()['success']:
        print("Deck shuffled.")
        return True
    else:
        print("Failed to shuffle deck.")
        return False

# Make a get request to the new deck url. If we recieve a successful status code, return true
# and split up cards in response between players. Return each players' cards for further steps.
def deal_cards(deck_id):
    draw_cards_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=6"
    response = requests.get(draw_cards_url)
    if response.status_code == 200 and response.json()['success']:
        cards = response.json()['cards']

        if not cards: # If the API didn't return any cards, return false
            print("The cards list is empty.")
            return False

        for card in cards: # If any of the cards are null, return false
            if card is None:
                print("A player recieved a null card.")
                return False

        player1_cards = cards[:3] # Giving the first player the first 3 cards, and the second player the last 3
        player2_cards = cards[3:]
        print("Player 1 cards:", [card['code'] for card in player1_cards]) # Printing the players' cards 
        print("Player 2 cards:", [card['code'] for card in player2_cards])

        return player1_cards, player2_cards
    else:
        print("Failed to draw cards.")
        return False, False

# Because 3 cards are dealt, we are using 3 card blackjack rules.
# https://wizardofodds.com/games/three-card-blackjack/
# Best hand using 2 of 3 cards is counted.
# We return whether the player's deck has both a 10 value card and an ace
def check_blackjack(cards):
    has_ace = any(card['value'] == 'ACE' for card in cards)
    has_ten_value = any(card['value'] in ['10', 'JACK', 'QUEEN', 'KING'] for card in cards)
    return has_ace and has_ten_value

# Report whether each player has blackjack based off of the calculations of check_blackjack().
# This will always return true because the result has already been calculated.
def report_blackjack(player1_blackjack, player2_blackjack):
    if player1_blackjack:
        print("Player 1 has blackjack!")
    if player2_blackjack:
        print("Player 2 has blackjack!")
    if not player1_blackjack and not player2_blackjack:
        print("Neither player has blackjack.")
    return True

# Main driver
def main():
    steps_passed = 0 # Initial amount of steps passed
    total_steps = 6 # total amount of steps 
    
    # Step 1: Check if site is up
    print("TEST 1: Checking if site is up")
    if check_site_up():
        steps_passed += 1 # Increment amount of steps passed
    else:
        print("Step 1 Failed.")
        print(f"{steps_passed}/{total_steps} Steps passed.")
        return
    
    # Step 2: Get a new deck
    print("TEST 2: Get a new deck")
    deck_id = get_new_deck()
    if deck_id:
        steps_passed += 1
    else:
        print("Step 2 Failed.")
        print(f"{steps_passed}/{total_steps} Steps passed.")
        return
    
    # Step 3: Shuffle the deck
    print("TEST 3: Shuffle the deck")
    if shuffle_deck(deck_id):
        steps_passed += 1
    else:
        print("Step 3 Failed.")
        print(f"{steps_passed}/{total_steps} Steps passed.")
        return
    
    # Step 4: Deal cards
    print("TEST 4: Deal cards")
    player1_cards, player2_cards = deal_cards(deck_id)
    if player1_cards:
        steps_passed += 1
    else:
        print("Step 4 Failed.")
        print(f"{steps_passed}/{total_steps} Steps passed.")
        return
    
    # Step 5: Check for blackjack
    print("TEST 5: Check for blackjack")
    player1_blackjack = check_blackjack(player1_cards)
    player2_blackjack = check_blackjack(player2_cards)
    steps_passed += 1  

    # Step 6: Report blackjack status
    print("TEST 6: Report blackjack status")
    report_blackjack(player1_blackjack, player2_blackjack)
    steps_passed += 1 
    
    # Print the amount of steps that passed
    print(f"{steps_passed}/{total_steps} Steps passed.")

if __name__ == "__main__":
    main()
