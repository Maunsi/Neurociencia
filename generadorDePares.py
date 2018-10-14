import random, sys, string


#genero los pares, los guardo en un diccionario y luego randomizo las keys para poder escribirlo ya "desordenado"
if(len(sys.argv) != 2):
	print("Este script toma como parametro la cantidad de estimulos a generar")
else:
	n = int(sys.argv[1])
	inputList = []
	for i in range(n):
		print(i)
		left = random.randint(1,5)
		right = random.randint(1,5)
		res = 0
		if(i < n//4):
			res = left + right
		elif( i >= n//4 and i < n//2):
			res = random.randint(1,5)
			while ((res == (left + right)) or (res == left) or (res == right)):
				res = random.randint(1,5)
		else:
			res = random.choice(string.ascii_uppercase)
		inputList.append(((left, right), res))

	print(inputList)
	random.shuffle(inputList)
	print(inputList)
	f = open("pairAndResInputs.txt", "w")
	for ((left, right), res) in inputList:
		s = str(left) + "," + str(right) + " " + str(res)
		f.write("%s\n" % s)
	f.close()


