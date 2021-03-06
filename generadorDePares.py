import random, sys, string

def generarMitadPrime(prime, mitad, input_list):
	for i in range(mitad):
		left = random.randint(1,5)
		right = random.randint(1,5)
		res = 0
		if(i < mitad//4):
			res = left + right
			while res > 6:
				left = random.randint(1,5)
				right = random.randint(1,5)
				res = left + right
		elif( mitad//4 <= i and i < mitad//2):
			res = random.randint(1,5)
			while ((res == (left + right)) or (res == left) or (res == right)):
				res = random.randint(1,5)
		else:
			res = random.choice(['A', 'B', 'C', 'D'])
		input_list.append((prime, left, right, res))

def main():
	if(len(sys.argv) != 2):
		print("Este script toma como parametro la cantidad de estimulos a generar")
	else:
		n = int(sys.argv[1])
	
		input_list = []

		#En caso de que n sea impar, nos gustaria que sumar tenga mas que representar
		mitad = n//2 if(n % 2 == 0) else (n//2+1)
		generarMitadPrime('sumar', mitad, input_list)
		generarMitadPrime('representar', n-mitad, input_list)

		f = open("pairAndResInputs.txt", "w")
		for (prime, left, right, res) in input_list:
			s = "{} {},{} {}".format(prime, left, right, res)
			f.write("%s\n" % s)
		f.close()

if __name__ == '__main__':
	main()


