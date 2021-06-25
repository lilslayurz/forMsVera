class Rewards:
    count_id = 0

    def __init__(self, reward_code, description):
        Rewards.count_id += 1
        self.__reward_id = Rewards.count_id
        self.__reward_code = reward_code
        self.__description = description

    def get_reward_code(self):
        return self.__reward_code

    def get_reward_id(self):
        return self.__reward_id

    def get_description(self):
        return self.__description

    def set_reward_code(self, reward_code):
        self.__reward_code = reward_code

    def set_reward_id(self, reward_id):
        self.__reward_id = reward_id

    def set_description(self, description):
        self.__description = description
