from ML_Controller import ML_Controller

if __name__ == "__main__":
    controller = ML_Controller()
    print(controller.provideRecommendation("F", 60, 1.5, "Pad Thai"))