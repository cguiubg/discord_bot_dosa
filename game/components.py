class Character:
    '''
        A single playable character.
    '''

    def __init__(self, character_name: str, user_id: int):
        self.character_name = character_name
        self.user_id = user_id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.user_id.__hash__() ^ self.character_name.__hash__()


class Player:
    '''
        A player that contains a unique player id and a collection of their characters.
    '''

    def __init__(self, user_id):
        self.user_id = user_id
        self.characters = set()

    def add_character(self, character: Character):
        self.characters.add(character)

    def __eq__(self, other):
        return  self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.user_id.__hash__()


class Quest:
    '''
        Contains information on a quests name, description, and the giver of the quest
        by user id.
    '''

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
    '''
        A bulletin board of quests and the players that have accepted the quest.
    '''

    def __init__(self):
        self.quests_and_characters = {}

    def quest_on_board(self, quest):
        return quest in self.quests_and_characters

    def add_quest(self, new_quest: Quest):
        self.quests_and_characters[new_quest] = set()

    def remove_quest(self, quest: Quest):
        if not self.quest_on_board(quest):
            return False

        del self.quests_and_characters[quest]

        return  True

    def join_quest(self, quest: Quest, character: Character):
        if not self.quest_on_board(quest):
            return False

        if character in self.quests_and_characters[quest]:
            return False

        self.quests_and_characters[quest].add(character)

        return True

    def leave_quest(self, quest: Quest, character: Character):
        if not self.quest_on_board(quest):
            return False

        if character not in self.quests_and_characters[quest]:
            return False

        self.quests_and_characters[quest].remove(character)

        return True

    def get_quests_characters(self, quest: Quest):
        return [character for character in self.quests_and_characters[quest]]

    def get_characters_quests(self, character: Character):
        return [quest for quest, characters in self.quests_and_characters.items()
                if character in characters]

