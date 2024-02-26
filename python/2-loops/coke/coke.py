def main():
    total = 0
    while True:
        coin = int(input("Insert Coin: "))
        if coin == 5 or coin == 10 or coin == 25:
            total += coin
            if total >= 50:
                break
        print("Amount Due:", 50 - total)
    print("Change Owed:", total % 50)


main()