from re import match

def main():
    time = input("Time: ").strip()

    time = convert(time)

    if time >= 7 and time <= 8:
        print("breakfast time")
    elif time >= 12 and time <= 13:
        print("lunch time")
    elif time >= 18 and time <= 19:
        print("dinner time")


def convert(time):
    try:
        hours, minutes = time.split(":")
        hours = int(hours)
        if minutes.endswith("a.m."):
            minutes = minutes.split("a")[0]
            if hours == 12:
                hours = 0
        elif minutes.endswith("p.m."):
            minutes = minutes.split("p")[0]
            if hours != 12:
                hours += 12

        return hours + (int(minutes) / 60)


    except ValueError:
        print("Format: ##.##[, p/a.m.]")
        return


if __name__ == "__main__":
    main()

#:##
##:##

#:## a.m.
##:## a.m.

#:## p.m.
##:## p.m.
