file = open("/projectnb/ec504/students/bmahabir/FinalProject/src/text.txt", "r")
start = input("Enter start index of word: ")
end = input("Enter end index of word: ")
if int(start) != 0:
	file.read(int(start))
word = file.read(int(end)-int(start)+1)
print("Your word is "+word)
