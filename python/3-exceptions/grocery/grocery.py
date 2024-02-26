def main():
    shopping_list = {}
    while True:
        try:
            item = input().upper()
            try:
                shopping_list[item] += 1
            except KeyError:
                shopping_list[item] = 1
        except EOFError:
            ordered_list = sorted(list(shopping_list))
            for item in ordered_list:
                print(shopping_list[item], item)
            return


main()