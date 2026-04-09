# Created by FEN1X-coder & Google Gemini.

from py_stealth import *
import re
import random  

# ==========================================
# CONFIGURATION
# ==========================================
CORPSE_GRAPHIC = 0x2006
LOOT_DESTINATION = Backpack()
LOOT_DISTANCE = 2
ACTION_DELAY = 600 # Milliseconds to wait between looting items

# Define the attributes you want and the MINIMUM value required to loot it.
# Make sure the text matches exactly what appears on your server's tooltips.
DESIRED_ATTRIBUTES = {
    "Swordsmanship": 1,
    "Tactics": 1,
    "Bushido": 1,
    "Anatomy": 1,
    "Parrying": 1,
    "Evaluating Intelligence": 1,
    "Magery": 1
}
# ==========================================
# FUNCTIONS
# ==========================================
def get_item_stats(item_id):
    """
    Reads the tooltip of an item and extracts the numeric values 
    for the attributes we care about.
    """
    stats = {}
    
    # GetTooltip retrieves the property string of the item from the server
    tooltip = GetTooltip(item_id)
    if not tooltip:
        return stats
        
    for attribute in DESIRED_ATTRIBUTES.keys():
        # Added the pipe (|) character to the exclusion list!
        # Now it will instantly stop searching if it hits the end of a tooltip line.
        pattern = rf"{attribute}[^\d\r\n|]*(\d+)"
        match = re.search(pattern, tooltip, re.IGNORECASE)
        
        if match:
            # Convert the found text number into an actual integer
            stats[attribute] = int(match.group(1))
            
    return stats

def is_worth_looting(item_stats):
    """
    Compares the item's stats against our configured minimums.
    Returns True if AT LEAST ONE attribute meets the minimum requirement.
    """
    for attribute, min_value in DESIRED_ATTRIBUTES.items():
        if attribute in item_stats and item_stats[attribute] >= min_value:
            return True
    return False

def scan_and_loot():
    """
    Finds corpses, opens them, scans items, and loots matches.
    """
    # Search for corpses on the ground within our distance
    if FindTypeEx(CORPSE_GRAPHIC, 0xFFFF, Ground(), False):
        corpses = GetFindedList()
        
        for corpse in corpses:
            if GetDistance(corpse) <= LOOT_DISTANCE:
                AddToSystemJournal(f"Opening corpse: {corpse}")
                
                # Open the corpse and wait for the server to send the contents
                UseObject(corpse)
                Wait(1000) 
                
                # Find all items inside this specific corpse (0xFFFF means 'any graphic/color')
                if FindTypeEx(0xFFFF, 0xFFFF, corpse, False):
                    items = GetFindedList()
                    
                    for item in items:
                        # Grab the stats from the tooltip
                        stats = get_item_stats(item)
                        
# Check if it meets our criteria
                        if is_worth_looting(stats):
                            AddToSystemJournal(f"*** Looting item! Stats: {stats} ***")
                            
                            # Generate random drop coordinates to prevent UO from auto-shuffling
                            drop_x = random.randint(20, 120)
                            drop_y = random.randint(20, 120)
                            
                            MoveItem(item, 0, LOOT_DESTINATION, drop_x, drop_y, 0)
                            Wait(ACTION_DELAY)
                            
                            # CRITICAL: Tell Stealth to permanently forget this item ID 
                            # so it never tries to move it again.
                            Ignore(item)
                            
                # Tell Stealth to ignore this corpse so we don't scan it again
                Ignore(corpse)

# ==========================================
# MAIN LOOP
# ==========================================
AddToSystemJournal("Starting Advanced Auto-Looter...")

while True:
    if Connected() and not Dead():
        scan_and_loot()
    
    # Brief pause to prevent the script from locking up the Stealth client CPU
    Wait(500)
