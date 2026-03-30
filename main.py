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
data_manager.load_slices_to_memory(slice_types)

# Tested Slice Soft Search Methods
matched_cards = data_manager.soft_search_for_colors(["B"])
matched_cards = data_manager.soft_search_for_colors(["R"], matched_cards)
matched_cards = data_manager.soft_search_for_colors(["G"], matched_cards)
#matched_cards = data_manager.soft_search_for_color_identity(["B", "R", "G"])
matched_cards = data_manager.soft_search_for_name('Korvold', matched_cards)

# Testing Methods
with open('card_data/saved_searches/forest_cards.json', 'w') as saved_search:
    json.dump(matched_cards, saved_search)

for type_slice in matched_cards:
    for card in matched_cards[type_slice]:
        print(card, len(matched_cards[type_slice][card]))
    print(len(matched_cards[type_slice]))
