from collections import defaultdict

def main():
	if(len(sys.argv) != 2):
		print("Este script toma como parametro la cantidad de estimulos por experimento")
	else:
		n = int(sys.argv[1])
		trial_results_by_index = defaultdict(list) #Este tiene los resultados para cada trial
		#Tambien podriamos tener un diccionario con claves del tipo de trial
		trial_results_by_type = defaultdict(list)
		lines = [line.rstrip('\n') for line in open("results.txt")]
		while len(lines) != 0:
			#Si no guardo los resultados de las letras el n es distinto al de generadorDePares
			for i in range(n):
				trial_id, prime, pair, res, keys = line.split(" ")
				left, right = pair.split(",")
				trial_results_by_index[trial_id].append(keys)

				key = prime

				if(res.isalpha()):
					key = key + "letra"
				elif int(left) + int(right) == int(res)
					key = key + "correcto"
				else:
					key = key + "incorrecto"
				trial_results_by_type[key].append(keys)
		results.close()

		#Esto lo vamos a cambiar, es para mostrar que podemos ir agrupando los valores como querramos
		with open("resultsByTrial.txt", "w") as f:
			for trial_id, keys in trial_results_by_index
				s = "Trial id: {}, Keys: {} ".format(trial_id, keys)
				f.write("%s\n" % s)
		f.close()

		with open("resultsByType", "w") as f:
			for trial_type, keys in trial_results_by_index
				s = "Trial id: {}, Keys: {} ".format(trial_type, keys)
				f.write("%s\n" % s)
		f.close()	

if __name__ == '__main__':
	main()
