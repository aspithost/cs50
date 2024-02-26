def main():
    userinput = input("Filename: ").strip().lower()

    _, separator, extension = userinput.rpartition(".")

    if not separator:
        print("application/octet-stream")
    else:
        match extension:
            case "gif":
                print("image/gif")
            case "jpg" | "jpeg":
                print("image/jpeg")
            case "png":
                print("image/png")
            case "pdf":
                print("application/pdf")
            case "txt":
                print("text/plain")
            case "zip":
                print("application/zip")
            case _:
                print("application/octet-stream")


main()