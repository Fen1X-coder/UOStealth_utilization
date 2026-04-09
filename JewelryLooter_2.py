"""
Credit: DennisMerrell86, FEN1X-coder, Google Gemini

UOStealth Jewelry Looter
Opens corpses, checks rings, bracelets, and necklaces
for 2+ skills >= 14, then loots them to your backpack.

Usage: Load this script in UOStealth and run it.
"""

import re
import random
from time import sleep

# =============================================================================
# CONFIGURATION
# =============================================================================

# Jewelry item types (graphic IDs)
RING_TYPE       = 0x108A
BRACELET_TYPE   = 0x1086
NECKLACE_TYPE_1 = 0x1F09
NECKLACE_TYPE_2 = 0x1F06

JEWELRY_TYPES = [RING_TYPE, BRACELET_TYPE, NECKLACE_TYPE_1, NECKLACE_TYPE_2]

# Corpse type
CORPSE_TYPE = 0x2006

# Minimum skill bonus value to count
MIN_SKILL_VALUE = 14

# Minimum number of skills that must meet the threshold
MIN_SKILL_COUNT = 2

# Search radius for corpses (tiles)
SEARCH_DISTANCE = 2

# Delay between main loop iterations (ms)
LOOP_DELAY = 500

# Delay after opening a corpse (ms)
OPEN_CORPSE_DELAY = 1000

# Delay after moving an item (ms)
LOOT_DELAY = 600

# All UO skill names that can appear on jewelry tooltips
SKILL_NAMES = [
    'Anatomy',
    'Animal Lore',
    'Animal Taming',
    'Archery',
    'Arms Lore',
    'Bushido',
    'Detecting Hidden',
    'Discordance',
    'Evaluating Intelligence',
    'Fishing',
    'Focus',
    'Healing',
    'Magery',
    'Musicianship',
    'Necromancy',
    'Parrying',
    'Peacemaking',
    'Provocation',
    'Resisting Spells',
    'Spirit Speak',
    'Stealing',
    'Swordsmanship',
    'Tactics',

]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def log(msg):
    """Nuclear silent mode: ONLY print to the Stealth journal if we loot an item."""
    # If the message doesn't contain the word "LOOT!", completely ignore it.
    if 'LOOT!' in msg:
        AddToSystemJournal(msg)

def count_qualifying_skills(item_id):
    """
    Read the tooltip for an item and count how many skill bonuses
    are >= MIN_SKILL_VALUE.
    Returns (count, list_of_matching_skills).
    """
    tooltip = GetTooltip(item_id)
    log(f'[DEBUG] Tooltip for 0x{item_id:08X}: "{tooltip}"')
    if not tooltip:
        log('[DEBUG] Tooltip is empty!')
        return 0, []

    matching = []

    for skill_name in SKILL_NAMES:
        # Match patterns like "Magery +15", "Swordsmanship 14", "Magery\t15"
        pattern = re.escape(skill_name) + r'[\s\t]+\+?(\d+)'
        match = re.search(pattern, tooltip, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            log(f'[DEBUG] Found: {skill_name} = {value}')
            if value >= MIN_SKILL_VALUE:
                matching.append((skill_name, value))

    log(f'[DEBUG] Total qualifying skills: {len(matching)}')
    return len(matching), matching


def find_corpses():
    """Find corpses on the ground within search distance."""
    SetFindDistance(SEARCH_DISTANCE)
    SetFindVertical(5)
    result = FindTypeEx(CORPSE_TYPE, 0xFFFF, Ground(), False)
    if result > 0:
        corpse_list = GetFindedList()
        log(f'[DEBUG] Found {len(corpse_list)} corpse(s): {corpse_list}')
        return corpse_list
    return []


def find_jewelry_in_container(container_id):
    """Find all jewelry items inside a container. Returns list of item IDs."""
    all_jewelry = []

    for jewelry_type in JEWELRY_TYPES:
        result = FindTypeEx(jewelry_type, 0xFFFF, container_id, False)
        log(f'[DEBUG] FindTypeEx(0x{jewelry_type:04X}, 0xFFFF, 0x{container_id:08X}) = {result}')
        if result > 0:
            found = GetFindedList()
            log(f'[DEBUG] Found {len(found)} item(s) of type 0x{jewelry_type:04X}: {found}')
            all_jewelry.extend(found)

    log(f'[DEBUG] Total jewelry found in container: {len(all_jewelry)}')
    return all_jewelry


def open_corpse(corpse_id):
    """Double-click a corpse to open it."""
    UseObject(corpse_id)
    Wait(OPEN_CORPSE_DELAY)


def loot_item(item_id, loot_bag):
    """Move an item to the loot bag at random coordinates."""
    drop_x = random.randint(20, 120)
    drop_y = random.randint(20, 120)
    
    if not MoveItem(item_id, 1, loot_bag, drop_x, drop_y, 0):
        # Fallback: try Grab
        Grab(item_id, 1)
    Wait(LOOT_DELAY)


def process_corpse(corpse_id, loot_bag):
    """Open a corpse, check jewelry inside, loot qualifying pieces."""
    open_corpse(corpse_id)

    jewelry_items = find_jewelry_in_container(corpse_id)

    if not jewelry_items:
        log(f'[DEBUG] No jewelry found in corpse 0x{corpse_id:08X}')
        return

    looted = 0
    for item_id in jewelry_items:
        count, skills = count_qualifying_skills(item_id)

        if count >= MIN_SKILL_COUNT:
            skill_desc = ', '.join(f'{name} +{val}' for name, val in skills)
            log(f'LOOT! {count} skills >= {MIN_SKILL_VALUE}: {skill_desc}')
            loot_item(item_id, loot_bag)
            looted += 1
            Ignore(item_id)
        else:
            Ignore(item_id)

    if looted > 0:
        log(f'Looted {looted} jewelry piece(s) from corpse.')


# =============================================================================
# MAIN SCRIPT
# =============================================================================

def setup():
    """Prompt for loot bag or default to backpack."""
    log('=== Jewelry Looter Starting ===')
    log(f'Looking for jewelry with {MIN_SKILL_COUNT}+ skills >= {MIN_SKILL_VALUE}')

    # Use backpack as default loot destination
    loot_bag = Backpack()
    log(f'Loot bag: Backpack (0x{loot_bag:08X})')
    log('Scanning for corpses...')

    return loot_bag


def main_loop(loot_bag):
    """Main scanning loop."""
    processed_corpses = set()

    while Connected():
        if Dead():
            Wait(2000)
            continue

        corpses = find_corpses()

        for corpse_id in corpses:
            if corpse_id in processed_corpses:
                continue

            log(f'Found corpse 0x{corpse_id:08X}, checking...')
            process_corpse(corpse_id, loot_bag)
            processed_corpses.add(corpse_id)

        # Prune old corpses that no longer exist
        to_remove = set()
        for cid in processed_corpses:
            if not IsObjectExists(cid):
                to_remove.add(cid)
        processed_corpses -= to_remove

        Wait(LOOP_DELAY)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    loot_bag = setup()
    try:
        main_loop(loot_bag)
    except Exception as e:
        log(f'Script error: {e}')
