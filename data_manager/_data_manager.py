import scrython
import json

class DataManager():
    """The DataManager Class. This class is used to Update, Slice and Search cards from the saved data
    
    KEY METHODS:
    update_sliced_card_data(self, update_bulk:bool, slice_types:list[str]=None) -> None:
    -> Used to update sliced card data. Also provides the option to update the local bulk data.

    load_slices_to_memory(self, slices:list[str]) -> None:
    -> Used to load slice files to memory to be searchable.

    soft_search_loaded_slices_for_name(self, card_name:str) -> dict[str:dict]:
    -> Used to soft search for a card by name in the loaded slices. This returns each
       card that contains the given string in the card name.

    soft_search_loaded_slices_for_color_identity(self, color_identity:list[str]) -> dict[str:dict]:
    -> Used to soft search for a card by color identity in the loaded slices. This returns each
       card that contains the given color identity as a subset. 

    soft_search_loaded_slices_for_colors(self, colors:list[str]) -> dict[str:dict]:
    -> Used to soft search for a card by colors in the loaded slices. This returns each
       card that contains the given color(s) as a subset. 
    """

    # --------------------------------------------------------------------------------------------------
    # Class Variables and Intialization
    # --------------------------------------------------------------------------------------------------
    bulk_data:dict
    loaded_slices:dict[str:dict]
    slice_types:list

    def __init__(self):
        self.bulk_data = {}
        self.slice_types = [
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
            'Vanguard',
            'Token']
        self.loaded_slices = {}
        for slice_type in self.slice_types:
            loaded_data_slice = {}
            self.loaded_slices.update({slice_type:loaded_data_slice})
    # --------------------------------------------------------------------------------------------------
    # Class Methods
    # --------------------------------------------------------------------------------------------------
    def _download_updated_default_cards(self) -> None:
        default_cards = scrython.bulk_data.ByType(type='default_cards')
        cards = default_cards.download(filepath='card_data/bulk_data/default_cards.json', progress=True)

    def _load_bulk_data_to_memory(self) -> None:
        with open('card_data/bulk_data/default_cards.json', 'r') as f:
            self.bulk_data = json.load(f)

    def _update_match_type_soft(self, cards:dict, card_type:str) -> dict[str:dict[str:dict]]:
        sorted_cards = {}
        for card in cards:
            try:
                if card_type in card['type_line']:
                    if not card['name'] in sorted_cards:
                        sets = {}
                        sets.update({card['set']:card})
                        sorted_cards.update({card['name']:sets})
                    else:
                        sets = sorted_cards[card['name']]
                        sets.update({card['set']:card})
                        sorted_cards.update({card['name']:sets})
            except:
                pass
        final_sorted_cards = self._update_match_typeless_to_name(cards, card_type, sorted_cards)
        return final_sorted_cards

    def _update_match_typeless_to_name(self, cards:dict, card_type:str, sorted_cards:dict) -> dict[str:dict[str:dict]]:
        for card in cards:
            missing_type = not card_type in card
            if card['name'] in sorted_cards and missing_type:
                sets = sorted_cards[card['name']]
                if 'typeless' in sets:
                    typeless = sets['typeless']
                    typeless.update({card['name']:card})
                    sets.update({'typeless':typeless})
                else:
                    typeless = {}
                    typeless.update({card['name']:card})
                    sets.update({'typeless':typeless})
                sorted_cards.update({card['name']:sets})
        return sorted_cards
    
    def _load_data_slice_to_memory(self, slice_type:str) -> None:
        with open(f"card_data/sliced_data/{slice_type}.json", 'r') as slice_data:
            self.loaded_slices.update({slice_type:json.load(slice_data)})
    # --------------------------------------------------------------------------------------------------
    # Data Updating and Slicing Methods
    # --------------------------------------------------------------------------------------------------
    def update_sliced_card_data(self, update_bulk:bool=False, slice_types:list[str]=None) -> None:
        """
        Used to update sliced card data. Also provides the option to update the local bulk data.

        VALUES:
        update_bulk:bool=False 
        -> If set to True the class will use scrython to download an updated 
           card list from scryfall and save it before continuing on to slicing the data.

        slice_types:list[str]=None 
        -> A list of the slices to update. If left empty, ALL slice files
           will be updated

        RETURNS:
        None
        """
        if update_bulk:
            self._download_updated_default_cards()
        self._load_bulk_data_to_memory()
        if slice_types == None:
            slice_types = self.slice_types
        for slice_type in slice_types:
            file_name = f"card_data/sliced_data/{slice_type}.json"
            sorted_cards = self._update_match_type_soft(self.bulk_data, slice_type)
            with open(file_name, 'w') as slice_file:
                json.dump(sorted_cards, slice_file)
            print(f"{slice_type}: {len(sorted_cards)}")
    # --------------------------------------------------------------------------------------------------    
    # Slice Management Methods
    # --------------------------------------------------------------------------------------------------
    def load_slices_to_memory(self, slices:list[str]) -> None:
        """
        Used to load slice files to memory to be searchable.

        VALUES:
        slices:list[str] 
        -> A list of slices that will be loaded into memory

        RETURNS:
        None
        """
        for type_slice in slices:
            self._load_data_slice_to_memory(type_slice)
    # --------------------------------------------------------------------------------------------------
    # Soft Search Slice Methods
    # --------------------------------------------------------------------------------------------------
    def soft_search_for_name(self, card_name:str, card_pool:dict=None) -> dict[str:dict]:
        """
        Used to soft search for a card by name in the loaded slices. This returns each
        card that contains the given string in the card name.

        VALUES:
        card_name:str 
        -> The name of the card you want to soft search for.

        card_pool:dict=None
        -> The pool of card slices to search, defaults to the loaded slices when None

        RETURNS:
        dict[str:dict] 
        -> A Dictionary of the matched card names and the matched card from 
           the loaded slices.
        """
        if card_pool == None: card_pool = self.loaded_slices
        matches = {}
        for type_slice in card_pool:
            if len(card_pool[type_slice]) > 0:
                cards = {}
                for card in card_pool[type_slice]:
                    if card_name in card:
                        cards.update({card:card_pool[type_slice][card]})
                matches.update({type_slice:cards})
        return matches
    
    def soft_search_for_color_identity(self, color_identity:list[str], card_pool:dict=None) -> dict[str:dict]:
        """
        Used to soft search for a card by color identity in the loaded slices. This returns each
        card that contains the given color identity as a subset. 
        
        EXAMPLE:
        soft_search_loaded_slices_for_color_identity(['B']) 
        -> This would return all cards with Black in the color identity 
           including all combinations i.e. ['B', 'G'], ['U', 'B'], 
           ['B', 'R', 'G'] and so on.

        VALUES:
        color_identity:list[str] 
        -> The colors in the identity of the card you want to soft search for.

        card_pool:dict=None
        -> The card pool to search the criteira for. Defaults to loaded slices when None.

        RETURNS:
        dict[str:dict] 
        -> A Dictionary of the matched card names and the matched card from 
           the loaded slices.
        """
        matches = {}
        if card_pool == None: card_pool = self.loaded_slices
        for type_slice in card_pool:
            if len(card_pool[type_slice]) > 0:
                cards = {}
                for card in card_pool[type_slice]:
                    for card_set in card_pool[type_slice][card]:
                        if 'color_identity' in card_pool[type_slice][card][card_set]:
                            if set(color_identity).issubset(card_pool[type_slice][card][card_set]['color_identity']):
                                cards.update({card:card_pool[type_slice][card]})
                matches.update({type_slice:cards})
        return matches

    def soft_search_for_colors(self, colors:list[str], card_pool:dict=None) -> dict[str:dict]:
        """
        Used to soft search for a card by colors in the loaded slices. This returns each
        card that contains the given color(s) as a subset. 
        
        EXAMPLE:
        soft_search_loaded_slices_for_colors(['B']) 
        -> This would return all cards with Black in the cost
        including all combinations i.e. ['B', 'G'], ['U', 'B'], 
        ['B', 'R', 'G'] and so on.

        VALUES:
        colors:list[str] 
        -> The colors of the card you want to soft search for.

        card_pool:dict=None
        -> The card pool to search through. Defaults to loaded slices when None

        RETURNS:
        dict[str:dict] 
        -> A Dictionary of the matched card names and the matched card from 
        the loaded slices.
        """
        if card_pool == None: card_pool = self.loaded_slices
        matches = {}
        for type_slice in card_pool:
            if len(card_pool[type_slice]) > 0:
                cards = {}
                for card in card_pool[type_slice]:
                    for card_set in card_pool[type_slice][card]:
                        if 'colors' in card_pool[type_slice][card][card_set]:
                            if set(colors).issubset(card_pool[type_slice][card][card_set]['colors']):
                                cards.update({card:card_pool[type_slice][card]})
                matches.update({type_slice:cards})
        return matches
    # --------------------------------------------------------------------------------------------------
