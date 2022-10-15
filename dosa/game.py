from collections import defaultdict

class Character:
    def __init__(self, character_name: str, user_id: str):
        self.character_name = character_name
        self.user_id = user_id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.user_id.__hash__()


class Quest:
    def __init__(self, name: str, description: str, id: int):
        self.name = name
        self.description = description
        self.quest_id = id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.quest_id.__hash__()

    def __str__(self):
        return f"__**Quest:**__ *{self.name}* #{self.quest_id}\n\n `{self.description}`"


class BulletinBoard:
    def __init__(self):
        self.quests_and_players = defaultdict(lambda : set())
        self.all_quests = defaultdict(lambda : None)

    def add_quest(self, new_quest: Quest):
        self.all_quests[new_quest.quest_id] = new_quest # type: ignore

    def remove_quest(self, quest: Quest):
        if quest not in self.quests_and_players:
            return False, "Error: Quest not found."
        else:
            del self.quests_and_players[quest]
            del self.all_quests[quest.quest_id]
            return  True, f"Deleted quest *{quest.name}*"

    def enlist_to_quest(self, quest_id: int, character: Character):
        if quest_id not in self.all_quests:
            return False, "Error: Quest not found."
        quest: Quest = self.all_quests[quest_id] # type: ignore

        if character in self.quests_and_players[quest]:
            return False, "You are already enlisted to this quest."

        self.quests_and_players[quest].add(character)
        return True, f"*{character.character_name}* has joined *{quest.name}*!"

    def leave_quest(self, quest_id: int, user_id: int):
        if quest_id not in self.all_quests:
            return False, "Error: Quest not found"
        quest: Quest = self.all_quests[quest_id] # type: ignore

        if user_id not in self.quests_and_players[quest]:
            return False, f"You are not enlisted in *{quest.name}"
        else:
            character_name = self.quests_and_players[quest].intersection({user_id}).pop().character_name
            self.quests_and_players[quest].remove(user_id)
            return True, f"You have left *{quest.name}* as character {character_name}"

    def get_quests_players(self, quest: Quest):
        return self.quests_and_players[quest]


class Game:

    current_quest_id = 0

    def __init__(self):
        self.bulletin_board = BulletinBoard()
        self.all_characters = defaultdict(lambda : set())
        self.current_characters = defaultdict(lambda : None)

    @staticmethod
    def inc_quest_id():
        Game.current_quest_id += 1
        return Game.current_quest_id

    def new_quest(self, quest_name, quest_description):
        new_quest = Quest(quest_name, quest_description, Game.inc_quest_id())
        self.bulletin_board.add_quest(new_quest)
        return True, str(new_quest)

    def join_quest(self, user_id, quest_id):
        character = self.current_characters[user_id]
        if not character:
            return False, "Error: Please register a character."

        return self.bulletin_board.enlist_to_quest(quest_id, character)

    def leave_quest(self, user_id, quest_id):
        return self.bulletin_board.leave_quest(quest_id, user_id)


    def get_current_character(self, user_id):
        return self.all_characters[user_id]

    def new_character(self, character_name, user_id):
        if character_name in self.all_characters[character_name]:
            return False, "You alread have a character with this name."

        new_character = Character(character_name, user_id)
        self.all_characters[user_id].add(new_character)
        return True, f"The world welcome {character_name}!\n To join quests with this character use `/switch_character {character_name}`."

    def switch_character(self, user_id, character_name):
        if character_name not in self.all_characters[user_id]:
            return False, f"You do not have a character named *{character_name}*."
        else:
            return True, f"You are now playing as *{character_name}*."
