"""
Guicheng Ma & Yuqing Li
CSE 163 Final Project
Title: Factors Affecting Tobacco Use Among Young People in the US.
In this program, we will ask users several questions in order to provide them
with the most useful and available suggestions(uncollected ) on tobacco
cessation. The answers will be gathered with their permission for future
research.
"""
import csv


def answers():
    """
    Asking users several questions about to track their tobacco using status
    in order to provide them with useful suggestions(unfinished)
    Gather their information in the data_process.csv file with their permission
    """
    user_input_list = []
    while True:
        print("\n")
        print("This is Cessation Helper. If you are trying to quit smoking, \
we are glad to help you.\n")
        print("By asking you several questions, we will provide most useful \
and available suggestions for you.")
        print("Before we move into next step, we need your confirmation.")
        print("We will ask you several questions about your smoking history, \
current location, age and so on to provide you with suggestions.\nThese \
information will not be used for any commercial purposes. But we will use \
them for research and analysis purposes, and the research\nresults will be \
provided to non-profit organizations to help more people quit smoking \
effectively.\n")
        print("Please confirm that you have read and agree to our terms.")
        print("Please enter 'yes' or 'no' below to confirm:")
        user_input = input()

        if user_input == "yes":
            print("Thank you for agreeing to our terms!")
        elif user_input == "no":
            print("We're sorry, but we need you to agree to our terms in order\
                to continue using our service.")
            print("If you want to leave, please input q")
            q_choice = input()
            if q_choice == 'q':
                print('Thank you for your time. Goodbye!')
                break
        else:
            print("Invalid input. Please enter 'yes' or 'no' to confirm your\
                agreement to our terms.")

        while True:
            try:
                age_input = int(input('Age: '))
                break
            except ValueError:
                print("Invalid Input. Your age should be an integer.\nPlease \
try again.")
        user_input_list.append(age_input)
        state_input = input("The state(full_name) you are currently living \
in: ")
        user_input_list.append(state_input)

        city_input = input("The city you are currently living in: ")
        user_input_list.append(city_input)

        gender_input = input("Your gender: ")
        user_input_list.append(gender_input)

        race_input = input("Your race: ")
        user_input_list.append(race_input)

        a = input("Do either of your parents smoke? (y/n)")

        if a == "y":
            parent_input = 1
        elif a == "n":
            parent_input = 0
        else:
            a = input("Invalid input. Please enter 'y' or 'n' to this \
question.")
        user_input_list.append(parent_input)

        while True:
            try:
                smoke_year = int(input("How long have you been using tobacco \
in years: "))
                break
            except ValueError:
                print("Invalid Input. Year should be an integer.\nPlease try \
again.")
        user_input_list.append(smoke_year)

        quited_or_not = input("Have you ever tried to quit smoking: y or n")
        while (quited_or_not != 'y') & (quited_or_not != 'n'):
            print('Invalid Input. You should input y(es) or n(o).')
            quited_or_not = input("Have you ever tried to quit smoking: y or \
n:")
        if quited_or_not == 'y':
            while True:
                try:
                    times_input = int(input("How many times have you tried: "))
                    break
                except ValueError:
                    print("Invalid Input. Times should be an integer.\nPlease \
try again.")
        elif quited_or_not == 'n':
            times_input = 0
        user_input_list.append(times_input)
        with open('data_collected.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(user_input_list)
        break


def main():
    answers()


if __name__ == '__main__':
    main()
