from cs50 import get_string

greeting = get_string("Greeting: ")

greeting = greeting.lower()

print(f"greeting: " + greeting)

def check(greeting):
  if "hello" in greeting:
    print("$0")
  elif greeting.startswith("h"):
    print("$20")
  else:
    print("$100")

check(greeting)