from Sci_Thai import Sci_Thai


class ML_Controller:
    def __init__(self):
        self.model = Sci_Thai("sci_thaiDB.csv")

    def processUserData(self, gender, weight, height, fooditem):
        output_gender = -1
        output_fooditem = -1
        bmi = weight/height**2

        if gender == "M":
            output_gender = 1
        else:
            output_gender = 0

        if fooditem == "Basil Rice":
            output_fooditem = 0
        elif fooditem == "Pineapple Fried Rice":
            output_fooditem = 1
        elif fooditem == "Pad Thai":
            output_fooditem = 2


        return [[output_gender, weight, height, bmi, output_fooditem]]

    def provideRecommendation(self, gender, weight, height, fooditem):
        user_data = self.processUserData(gender, weight, height, fooditem)
        prediction = self.model.predict(user_data)
        if(prediction <= 6 and prediction >= 4):
            return "Just enough!"
        elif(prediction >= 2 and prediction < 4):
            return "Might want to size up 1/4 portion!"
        elif(prediction > 6 and prediction <= 8):
            return "Might want to size down 1/4 portion!"
        elif(prediction >= 0 and prediction <2):
            return "Might want to size up 1/2 a portion!"
        elif(prediction > 8 and prediction <= 10):
            return "Might want to size down 1/2 a portion!"

