greeting = input("Greeting: ").lower()

# greeting = greeting.lower()

def check(greeting):
  if "hello" in greeting:
    print("$0")
  elif greeting.startswith("h"):
    print("$20")
  else:
    print("$100")

check(greeting)