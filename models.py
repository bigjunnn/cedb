class User:
    def __init__(self, id):
        self.id = id
        self.age = None
        self.gender = None
        self.height = None
        self.weight = None

    def __str__(self):
        details = "Chat ID: " + str(self.id) + "\nAge: " + str(self.age) + " years old\n" + "Gender: " + self.gender + \
        "\nHeight: " + str(self.height) + \
        " cm\nWeight: " + str(self.weight) + "kg"
        return details

class Report:
    def __init__(self, user_id):
        self.user_id = user_id
        self.canteen = None
        self.store = None
        self.fullness_rating = None

    def __str__(self):
        details = "Canteen: {}\nStore: {}\nFullness Rating: {}\n".format(self.canteen, self.store, str(self.fullness_rating))
        return details
        