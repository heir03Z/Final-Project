# import datetime
# import turtle

# currentTime = datetime.datetime.now()
# print(currentTime.hour)
# if currentTime.hour < 17:
#     screen.bgcolor("white")
# elif 17 <= currentTime.hour < 20:
#     screen.bgcolor("purple")
# else:
#     screen.bgcolor("black")



    # screen = turtle.Screen()

def get(time):

    if time == 'day':
        print(1)
    elif time == 'evening':
        print(2)
    elif time == 'night':
        print(3)
    
print(get('day'))