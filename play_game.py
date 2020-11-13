import json, time, sys, random

def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('spooky_mansion.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")    
    play(game)



def play(rooms):
    start = time.time()
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break
        print("  {}".format(here["description"]))
        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print(" {}. {}".format(i+1, exit['description']))
        
        for item in here["items"]:
            print ("a",item , "has been found in the room")
        
        cat_rooms = find_non_win_rooms(rooms)
        
        cat_room = random.choice(cat_rooms)
        
        if cat_room == current_place:
            print("Black cat has entered the room")
            continue

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action == "help":
            print_instructions()
            continue
        if action == "stuff":
            if len(stuff) > 0:
                print(stuff)
                continue
            else:
                print("you have nothing")
                continue
        if action == "take":
            if len(here["items"]) > 0:
                print("You took all items")
                for item in here["items"]:
                    stuff.append(item)
                    print("You took...", item)
                here["items"].clear()
                continue
        if action == "drop":
            print("What would you like to drop?")
            for item in stuff:
                print(item)
            drop = input("Which one?")
            stuff.remove(drop)
            here["items"].append(drop)
            print("item has been dropped")
            continue   
        if action == "search":
            for ex in here["exits"]:
                if ex.get("hidden"):
                    here["exits"]["hidden"] = False
                    print("You found a hidden...", ex)
            continue

        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if "required_key" in selected:
                if selected["required_key"] in stuff:
                    current_place = selected['destination']
                else:
                    print("The door is locked!")
            else:
                current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")
    end = time.time()
    total = end - start
    minutes = total // 60
    total -= minutes * 60
    seconds = total
    print("YOU TOOK THIS LONG ", minutes, "minutes", seconds, "seconds")

def find_usable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
