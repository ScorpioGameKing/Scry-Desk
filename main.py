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
#data_manager.update_sliced_card_data(True)
data_manager.load_slices_to_memory(slice_types)

# Tested Slice Soft Search Methods
#matched_cards = data_manager.soft_search_loaded_slices_for_name('Forest')
#matched_cards = data_manager.soft_search_loaded_slices_for_color_identity(["B"])
#matched_cards = data_manager.soft_search_loaded_slices_for_colors(['B'])

# Testing Methods

#for card in matched_cards:
#    print(card, len(matched_cards[card]))
print(len(matched_cards))
