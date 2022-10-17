from collections import defaultdict

class Character:
    def __init__(self, character_name: str, user_id: int):
        self.character_name = character_name
        self.user_id = user_id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.user_id.__hash__() ^ self.character_name.__hash__()


class Quest:
    def __init__(self, name: str, description: str, id: int, user_id: int):
        self.name = name
        self.description = description
        self.quest_id = id
        self.user_id = user_id

    def can_edit(self, user_id: int):
        return self.user_id == user_id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.quest_id.__hash__()

    def __str__(self):
        return f"#{self.quest_id} __**Quest:**__ *{self.name}*\n\n `{self.description}`"


class BulletinBoard:
    def __init__(self):
        self.quests_and_characters = defaultdict(lambda : defaultdict(lambda : Character("Default", 0)))
        self.all_quests = defaultdict(lambda : Quest("Default", "Default", 0, 0))

    def add_quest(self, new_quest: Quest):
        self.all_quests[new_quest.quest_id] = new_quest # type: ignore
        return True, str(new_quest)

    def remove_quest(self, quest_id: int, user_id: int):
        print(f"{quest_id} by {user_id}")
        for k,v in self.all_quests.items():
            print(k)
        if quest_id not in self.all_quests:
            return False, "Error: Quest not found."

        quest = self.all_quests[quest_id]
        if not quest.can_edit(user_id):
            return False, "You cannot takedown other's quests."
        else:
            if quest_id in self.quests_and_characters:
                del self.quests_and_characters[quest_id]
            del self.all_quests[quest_id]
            return  True, f"Deleted quest *{quest.name}*."

    def enlist_to_quest(self, quest_id: int, character: Character):
        if quest_id not in self.all_quests:
            return False, "Error: Quest not found."

        quest: Quest = self.all_quests[quest_id] # type: ignore
        if character.user_id in self.quests_and_characters[quest_id]:
            return False, "You are already enlisted to this quest."

        self.quests_and_characters[quest_id][character.user_id] = character
        return True, f"*{character.character_name}* has joined *{quest.name}*!"

    def leave_quest(self, quest_id: int, user_id: int):
        if quest_id not in self.all_quests:
            return False, "Error: Quest not found."
        quest: Quest = self.all_quests[quest_id] # type: ignore
        if user_id not in self.quests_and_characters[quest_id]:
            return False, f"You are not enlisted in *{quest.name}"
        else:
            character_name = self.quests_and_characters[quest_id][user_id].character_name
            del self.quests_and_characters[quest_id][user_id]
            return True, f"You have left *{quest.name}* as character {character_name}"

    def get_quests_players(self, quest_id: int):
        return [c.character_name for c in self.quests_and_characters[quest_id].values()]


class Game:

    def __init__(self):
        self.bulletin_board = BulletinBoard()
        self.all_characters = defaultdict(lambda : set())
        self.current_characters = defaultdict(lambda : None)
        self.current_quest_id = 0

    # Quest Management
    def inc_quest_id(self):
        self.current_quest_id += 1
        return self.current_quest_id

    def new_quest(self, quest_name, quest_description, user_id):
        new_quest = Quest(quest_name, quest_description, self.inc_quest_id(), user_id)
        return self.bulletin_board.add_quest(new_quest)

    def remove_quest(self, quest_id, user_id):
        return self.bulletin_board.remove_quest(quest_id, user_id)

    def join_quest_by_id(self, quest_id, user_id):
        character = self.current_characters[user_id]
        if not character:
            return False, "Error: Not currently playing as a character, switch to one of your registered characters."

        return self.bulletin_board.enlist_to_quest(quest_id, character)

    def join_quest_by_character(self, quest_id, user_id, character_name):
        characters = self.all_characters[user_id]
        for character in characters:
            if character.character_name == character_name:
                return self.bulletin_board.enlist_to_quest(quest_id, character)

        return False, f"Character {character_name} not found in your registered characters."

    def leave_quest(self, user_id, quest_id):
        return self.bulletin_board.leave_quest(quest_id, user_id)

    ## Character Management
    def new_character(self, user_id, character_name):
        for character in self.all_characters[user_id]:
            if character_name == character.character_name:
                return False, "You alread have a character with this name."

        new_character = Character(character_name, user_id)
        self.all_characters[user_id].add(new_character)
        return True, f"The world welcome {character_name}!\n To join quests with this character use `/switch_character {character_name}`."

    def remove_character(self, user_id, character_name):
        for character in self.all_characters[user_id]:
            if character_name == character.character_name:
                self.all_characters[user_id].remove(character)
                if self.current_characters[user_id].character_name == character.character_name: # type: ignore
                    del self.current_characters[user_id]
                return True, f"*{character.character_name}* has been removed from your registered characters."

        return False, f"You do not have a character named *{character_name}*."

    def switch_character(self, user_id, character_name):
        for character in self.all_characters[user_id]:
            if character_name == character.character_name:
                self.current_characters[user_id] = character
                return True, f"You are now playing as *{character_name}*."

        return False, f"You do not have a character named *{character_name}*."

    def list_characters(self, user_id):
        response = "Your characters:\n`"
        user_characters = self.all_characters[user_id]
        
        if not len(user_characters) > 0:
            response += "No registered characters.`\n"
            return True, response

        for character in user_characters:
            response += f"  * {character.character_name}\n"
        response += "`"
        return True, response

    
