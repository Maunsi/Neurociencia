import random, sys, string

def generarMitadPrime(prime, start, end, input_list):
	mitad = (start + end)
	for i in range(start, end):
		print(i)
		left = random.randint(1,5)
		right = random.randint(1,5)
		res = 0
		if(i < mitad//4):
			res = left + right
		elif( i >= mitad//4 and i < mitad//2):
			res = random.randint(1,5)
			while ((res == (left + right)) or (res == left) or (res == right)):
				res = random.randint(1,5)
		else:
			res = random.choice(['A', 'B', 'C', 'D'])
		input_list.append((i, prime, left, right, res))

#genero los pares, los guardo en un diccionario y luego randomizo las keys para poder escribirlo ya "desordenado"
if(len(sys.argv) != 2):
	print("Este script toma como parametro la cantidad de estimulos a generar")
else:
	n = int(sys.argv[1])
	
	
	input_list = []
	#Esta mitad corresponde a sumar
	
	generarMitadPrime('sumar', 0, n//2, input_list)
	generarMitadPrime('representar', n//2, n, input_list)

	f = open("pairAndResInputs.txt", "w")
	for (i, prime, left, right, res) in input_list:
		s = str(i) + " " + prime + " " + str(left) + "," + str(right) + " " + str(res)
		f.write("%s\n" % s)
	f.close()


