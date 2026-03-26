import json
from data_manager import DataManager

data_manager = DataManager()

slice_types = [
    'Artifact', 
    'Battle',
    'Creature', 
    'Enchantment', 
    'Land', 
    'Planeswalker', 
    'Emblem', 
    'Instant', 
    'Sorcery',
    'Dungeon',
    'Conspiracy',
    'Phenomenon',
    'Plane',
    'Scheme',
    'Vanguard']

matched_cards = {}

# Tested Updating, Slicing and Loading Methods
#data_manager.update_sliced_card_data()
data_manager.load_slices_to_memory(['Land'])

# Tested Slice Soft Search Methods
#matched_cards = data_manager.soft_search_loaded_slices_for_color_identity(["B"])
#matched_cards = data_manager.soft_search_loaded_slices_for_colors(['B'])

# Testing Methods
matched_cards = data_manager.soft_search_loaded_slices_for_name('Forest')
with open('card_data/saved_searches/forest_cards.json', 'w') as saved_search:
    json.dump(matched_cards, saved_search)

#for card in matched_cards:
#    print(card, len(matched_cards[card]))
print(len(matched_cards))
