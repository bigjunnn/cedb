from ML_Controller import ML_Controller

if __name__ == "__main__":
    controller = ML_Controller()

    while True:
        gender = str(input("Male or Female"))
        height = int(input("Height in cm"))
        weight = int(input("Weight in kg"))
        food = str(input("Basil Rice/Pineapple Fried Rice/Pad Thai"))
        fullness = int(input("fullness"))

        controller.addUserReport(gender, height, weight, food, fullness)
