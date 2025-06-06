# app.py

import streamlit as st
from game_logic import initialize_game, Village, Item, Bag, BinarySearchTree

# --- Game State Initialization ---
if 'game_initialized' not in st.session_state:
    village_queue, saved_villages, player_bag, all_villages = initialize_game()
    
    st.session_state.village_queue = village_queue
    st.session_state.saved_villages = saved_villages
    st.session_state.player_bag = player_bag
    st.session_state.all_villages = all_villages 
    st.session_state.game_initialized = True

# --- UI Layout ---
st.title("Village Rescue Game")

# --- Sidebar ---
with st.sidebar:
    st.header("Çanta (Inventory)")
    inventory_items = st.session_state.player_bag.view()
    
    if not inventory_items:
        st.write("Your bag is empty.")
    else:
        for item_name in inventory_items:
            st.write(f"- {item_name}")
            
    st.write("---")
    st.write(f"Capacity: {st.session_state.player_bag.size} / {st.session_state.player_bag.capacity}")

    st.header("Actions")
    if st.button("Çantadan Son Öğeyi Çıkar (Pop)"):
        popped_item = st.session_state.player_bag.pop()
        if popped_item:
            st.success(f"Removed item: {popped_item.name}")
        else:
            st.warning("Your bag is already empty.")
        st.rerun()

    st.header("Use an Item")
    if inventory_items:
        selected_item = st.selectbox("Choose an item to use:", options=inventory_items, key="use_item_select")
        if st.button("Seçili Öğeyi Kullan"):
            st.session_state.player_bag.useItem(selected_item)
            st.success(f"You used the item: {selected_item}")
            st.rerun()
    else:
        st.write("No items to use.")

# --- Main Content Columns ---
left_col, right_col = st.columns(2)

with left_col:
    # --- Main Game Area ---
    st.header("Game Status")

    if st.session_state.village_queue:
        current_village = st.session_state.village_queue[0]
        st.subheader(f"You are at: {current_village.name}")
        st.write(f"Items available in this village: {[item.name for item in current_village.items]}")
        st.write("---")

        if st.button("Sıradaki Köyü Kurtar"):
            can_save = True
            if current_village.name == "Nisan":
                if st.session_state.player_bag.contains("balta") and st.session_state.player_bag.contains("iksir"):
                    st.info("Required items 'balta' and 'iksir' were used to save Nisan.")
                    st.session_state.player_bag.useItem("balta")
                    st.session_state.player_bag.useItem("iksir")
                else:
                    st.error("5. Köyü kurtarmak için çantanızda bir balta ve bir iksir olmalıdır.")
                    can_save = False
            
            if can_save:
                saved_village = st.session_state.village_queue.popleft()
                st.session_state.saved_villages.append(saved_village.name)
                st.success(f"You have saved {saved_village.name}!")
                items_not_added = []
                for item in saved_village.items:
                    success = st.session_state.player_bag.push(item)
                    if not success:
                        items_not_added.append(item.name)
                if items_not_added:
                    st.warning(f"Your bag was full! Could not collect: {', '.join(items_not_added)}")
                st.rerun()
    else:
        st.success("Congratulations! You have saved all the villages!")
        st.balloons()

    # --- Search Feature ---
    st.write("---")
    st.header("Search for an Item")
    search_term = st.text_input("Aramak istediğiniz öğenin adı:", key="search_input").lower()
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        if st.button("Çantamda Ara"):
            if search_term:
                bst = BinarySearchTree()
                all_items_in_bag = st.session_state.player_bag.get_all_items()
                for item in all_items_in_bag:
                    bst.insert(item)
                if bst.search(search_term):
                    st.success(f"Found '{search_term}' in your bag!")
                else:
                    st.error(f"Could not find '{search_term}' in your bag.")
            else:
                st.warning("Please enter an item name to search.")
    with search_col2:
        if st.button("Tüm Köylerde Ara"):
            if search_term:
                found_in_villages = []
                for village in st.session_state.all_villages:
                    village_bst = BinarySearchTree()
                    for item in village.items:
                        village_bst.insert(item)
                    if village_bst.search(search_term):
                        found_in_villages.append(village.name)
                if found_in_villages:
                    st.success(f"Found '{search_term}' in the following village(s): {', '.join(found_in_villages)}")
                else:
                    st.error(f"Could not find '{search_term}' in any village.")
            else:
                st.warning("Please enter an item name to search.")

with right_col:
    # --- 9. Game Progress Display Module ---
    st.header("Oyun İçi İlerleme Kontrolü")

    # Question 1: "Kurtarılması gereken köyler hangileridir?" 
    st.subheader("Villages to be Rescued")
    remaining_villages = [village.name for village in st.session_state.village_queue]
    if remaining_villages:
        st.write(remaining_villages)
    else:
        st.write("All villages have been rescued!")

    # Question 2: "Şu an hangi köydeyim ve hangilerini kurtardım?" 
    st.subheader("Current Status")
    # "Şu anki köy" 
    if st.session_state.village_queue:
        st.write(f"**Current Village:** {st.session_state.village_queue[0].name}")
    else:
        st.write("**Current Village:** None. The quest is complete!")
    # "Kurtarılan köyler" 
    if st.session_state.saved_villages:
        st.write(f"**Rescued Villages:** {', '.join(st.session_state.saved_villages)}")
    else:
        st.write("**Rescued Villages:** None yet.")

    # Question 3: "Hangi köyde hangi envanterler var?" 
    st.subheader("Village Inventories")
    # Use an st.expander for each village 
    for village in st.session_state.all_villages:
        with st.expander(f"See items in {village.name}"):
            village_items = [item.name for item in village.items]
            if village_items:
                for item_name in village_items:
                    st.write(f"- {item_name}")
            else:
                st.write("This village has no items.")