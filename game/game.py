from collections import defaultdict


# TODO: Refractor game logic...

class Game:

    current_quest_id = 0

    def __init__(self):
        self.bulletin_board = BulletinBoard()
        self.all_characters = defaultdict(lambda : set())
        self.current_characters = defaultdict(lambda : None)

    # Quest Management
    @classmethod
    def _inc_quest_id(cls):
        cls.current_quest_id += 1
        return cls.current_quest_id

    def new_quest(self, quest_name, quest_description, user_id):
        new_quest_id = self._inc_quest_id()
        new_quest = Quest(quest_name, quest_description, new_quest_id, user_id)
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

