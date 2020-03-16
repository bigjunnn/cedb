class cedbDatabase:
    curr_database = {}

    def __init__(self):
        self.currDatabase = {}

    def put(self, user_id, user_info):
        if user_id not in self.curr_database:
            self.curr_database[user_id] = user_info

    def get(self, user_id):
        if user_id in self.curr_database:
            return self.curr_database.get(user_id)

    def is_first_time_user(self, user_id):
        if user_id in self.curr_database:
            return True
        else:
            return False