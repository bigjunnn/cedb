from Sci_Thai import Sci_Thai


class ML_Controller:
    def __init__(self):
        self.model = Sci_Thai("sci_thaiDB.csv")
        self.counter = 0

    def processUserData(self, gender, weight, height, fooditem):
        output_gender = -1
        output_fooditem = self.transformFoodToInt(fooditem)
        bmi = weight/height**2

        if gender == "M":
            output_gender = 1
        else:
            output_gender = 0

        return [[output_gender, weight, height, bmi, output_fooditem]]

    def provideRecommendation(self, gender, weight, height, fooditem):
        user_data = self.processUserData(gender, weight, height, fooditem)
        prediction = self.model.predict(user_data)
        if(prediction <= 6 and prediction >= 4):
            return "Just enough!"
        elif(prediction >= 2 and prediction < 4):
            return "Might want to size up 1/2 a portion!"
        elif(prediction > 6 and prediction <= 8):
            return "Might want to size down 1/2 a portion!"
        elif(prediction >= 0 and prediction <2):
            return "Might want to size up 1 portion!"
        elif(prediction > 8 and prediction <= 10):
            return "Might want to size down 1 portion!"

    #gender = String of either "Male"/"Female"
    #height = integer of height in cm
    #weight = integer of weight in kg
    #foodItem = String of "Basil Rice/Pineapple Fried Rice/Pad Thai"
    #fullness = integer of fullness no.
    def addUserReport(self, gender, height, weight, food, fullness):
        input_gender = ""
        input_height = 0
        if gender == "Male":
            input_gender = 1
        else:
            input_gender = 0
        
        input_height = height/100
        input_food = self.transformFoodToInt(food)

        self.model.add_user_data(input_gender, input_height, weight, input_food, fullness)
        self.counter = self.counter + 1

        if self.counter == 30:
            self.model.retrain()
            self.counter = 0
    
    def transformFoodToInt(self, food):
        output = -1
        if food == "Basil Rice":
            output = 0
        elif food == "Pineapple Fried Rice":
            output = 1
        elif food == "Pad Thai":
            output = 2
        
        return output





