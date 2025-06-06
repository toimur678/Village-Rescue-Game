# game_logic.py

class Item:
    """
    Represents an item that can be found in a village or held in the player's bag.
    """
    def __init__(self, name: str, power_score: int = 0):
        """
        Initializes an Item object.
        
        Args:
            name (str): The name of the item (e.g., "kılıç", "iksir").
            power_score (int): A numerical score for the item, which can be used later
                               for sorting in a Binary Search Tree.
        """
        self.name = name
        self.power_score = power_score

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the item.
        """
        return f"Item(name='{self.name}', power_score={self.power_score})"


class Village:
    """
    Represents a village in the game world.
    Each village has a name and contains a list of items.
    """
    def __init__(self, name: str):
        """
        Initializes a Village object.
        
        Args:
            name (str): The name of the village.
        """
        self.name = name
        # The items attribute will be a list that holds Item objects.
        # Each village must contain at least 3 different items.
        self.items = [] 

    def add_item(self, item: Item):
        """
        Adds an Item object to the village's list of items.
        """
        self.items.append(item)

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the village.
        """
        item_names = [item.name for item in self.items]
        return f"Village(name='{self.name}', items={item_names})"
    


# game_logic.py (continued)

class Node:
    """
    A helper class that serves as the building block for the linked list.
    """
    def __init__(self, data: Item):
        """
        Initializes a Node object.
        
        Args:
            data (Item): The data to be stored in the node, which is an Item object.
        """
        self.data = data  # The 'data' will be an Item object 
        self.next = None  # The 'next' attribute points to the next node in the list 

class Bag:
    """
    Implements the player's inventory (Çanta) using a Linked List that behaves like a Stack. 
    It has a fixed capacity to hold items. 
    """
    def __init__(self, capacity: int = 10):
        """
        Initializes the Bag object.
        """
        self.head = None  # Points to the start of the list (top of the stack) 
        self.capacity = capacity  # The maximum number of items the bag can hold 
        self.size = 0  # The current number of items in the bag 

    def push(self, item: Item):
        """
        Adds an item to the front of the linked list (top of the stack). 
        This method implements LIFO (Last-In, First-Out) stack behavior. 
        It returns True if the item was added successfully, False otherwise.
        """
        # Checks if the bag is full before adding a new item. 
        if self.size >= self.capacity:
            print("Warning: Bag is full! Cannot add item.")
            return False
        
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return True

    def pop(self):
        """
        Removes and returns the item from the front of the list (top of the stack). 
        Returns the removed Item object or None if the bag is empty.
        """
        if self.head is None:
            return None
        
        item_to_remove = self.head.data
        self.head = self.head.next
        self.size -= 1
        return item_to_remove

    def useItem(self, item_name: str):
        """
        Finds and removes a specific item by its name from anywhere in the list. 
        This is required for fulfilling village rescue conditions. 
        Returns True if the item was found and used, False otherwise.
        """
        if self.head is None:
            return False

        # Handle case where the item to be used is at the head
        if self.head.data.name == item_name:
            self.pop()
            return True

        # Traverse the list to find the item
        current = self.head
        while current.next is not None and current.next.data.name != item_name:
            current = current.next

        # If the item was found in the list (and not at the head)
        if current.next is not None:
            current.next = current.next.next
            self.size -= 1
            return True
        
        return False # Item not found

    def contains(self, item_name: str) -> bool:
        """
        A helper method to check if an item with a specific name exists in the bag. 
        This is used to verify conditions for rescuing the last three villages. 
        Returns True if the item is in the bag, False otherwise.
        """
        current = self.head
        while current is not None:
            if current.data.name == item_name:
                return True
            current = current.next
        return False

    def view(self) -> list:
        """
        Returns a list of the names of all items currently in the bag. 
        """
        items_list = []
        current = self.head
        while current is not None:
            items_list.append(current.data.name)
            current = current.next
        return items_list

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the bag's contents.
        """
        return f"Bag(size={self.size}, capacity={self.capacity}, items={self.view()})"
    
    def get_all_items(self) -> list:
        """
        Returns a list of all Item objects currently in the bag.
        """
        items_list = []
        current = self.head
        while current is not None:
            items_list.append(current.data)
            current = current.next
        return items_list
    
# game_logic.py (continued)

import collections

# In game_logic.py, modify the 'initialize_game' function like this:

# In game_logic.py, replace your current initialize_game function with this one.

def initialize_game():
    """
    Creates all the initial game objects and returns them.
    This function will only be run once at the start of the game.
    """
    # 1. Create all 7 Village objects
    v1 = Village(name="Aralık")
    v2 = Village(name="Ocak")
    v3 = Village(name="Şubat")
    v4 = Village(name="Mart")
    v5 = Village(name="Nisan")
    v6 = Village(name="Mayıs")
    v7 = Village(name="Haziran")

    # 2. Populate each village with at least 3 items
    v1.add_item(Item("kılıç", 10))
    v1.add_item(Item("kalkan", 8))
    v1.add_item(Item("yiyecek", 2))
    
    v2.add_item(Item("yay", 7))
    v2.add_item(Item("ok", 1))
    v2.add_item(Item("su", 1))

    v3.add_item(Item("mızrak", 9))
    v3.add_item(Item("zırh", 9))
    v3.add_item(Item("iksir", 5))

    v4.add_item(Item("gürz", 8))
    v4.add_item(Item("miğfer", 6))
    v4.add_item(Item("altın", 3))

    # Village 5 requires 'balta' and 'iksir' to be rescued
    v5.add_item(Item("balta", 8))
    v5.add_item(Item("harita", 4))
    v5.add_item(Item("halat", 2))

    v6.add_item(Item("arbalet", 9))
    v6.add_item(Item("bıçak", 5))
    v6.add_item(Item("kibrit", 1))

    v7.add_item(Item("büyülü asa", 10))
    v7.add_item(Item("tılsım", 7))
    v7.add_item(Item("pelerin", 5))
    
    # Create a list of all villages for the "search all" feature
    all_villages = [v1, v2, v3, v4, v5, v6, v7]
    
    # 3. Create the queue of villages from the list of all villages
    village_queue = collections.deque(all_villages)

    # 4. Initialize an empty list to store the names of saved villages
    saved_villages = []

    # 5. Create an instance of the Bag class for the player
    player_bag = Bag(capacity=10)

    # Return the new all_villages list as well
    return village_queue, saved_villages, player_bag, all_villages

# game_logic.py (continued)

class BSTNode:
    """
    Represents a node in the Binary Search Tree.
    Each node contains an Item object and pointers to its left and right children.
    """
    def __init__(self, item: Item):
        """
        Initializes a BSTNode.
        
        Args:
            item (Item): The Item object to be stored in this node.
        """
        self.item = item  # The data is the Item object itself
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    A Binary Search Tree (BST) data structure for efficient item searching and sorting.
    Items are inserted and sorted based on their name attribute.
    """
    def __init__(self):
        """
        Initializes an empty Binary Search Tree.
        """
        self.root = None

    def insert(self, item: Item):
        """
        Public method to insert an Item into the tree.
        """
        self.root = self._insert_recursive(self.root, item)

    def _insert_recursive(self, node: BSTNode, item: Item) -> BSTNode:
        """
        A recursive helper function to find the correct position and insert a new node.
        Items are sorted alphabetically by item.name.
        """
        if node is None:
            return BSTNode(item)
        
        if item.name < node.item.name:
            node.left = self._insert_recursive(node.left, item)
        elif item.name > node.item.name:
            node.right = self._insert_recursive(node.right, item)
        
        return node

    def search(self, item_name: str) -> bool:
        """
        Public method to search the tree for an item by its name.
        Returns True if the item is found, False otherwise.
        """
        return self._search_recursive(self.root, item_name)

    def _search_recursive(self, node: BSTNode, item_name: str) -> bool:
        """
        A recursive helper function to search for a specific item_name in the tree.
        """
        if node is None:
            return False
        
        if item_name == node.item.name:
            return True
        elif item_name < node.item.name:
            return self._search_recursive(node.left, item_name)
        else:
            return self._search_recursive(node.right, item_name)