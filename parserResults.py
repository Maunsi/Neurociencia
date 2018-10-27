from collections import defaultdict

#ABANDONAMOS ESTE ARCHIVO
def main():
	trial_results_by_index = defaultdict(list) #Este tiene los resultados para cada trial
	trials_by_subject_id = defaultdict(list) #Para cada sujeto tenemos todos sus trials
	#Tambien podriamos tener un diccionario con claves del tipo de trial
	trial_results_by_type = defaultdict(list)
	lines = [line.rstrip('\n') for line in open("results.txt")]
	subject_id = 0
	i = 0
	
	while i < len(lines):
		line = lines[i]
		while line != "*":
			print(line)
			#Todas estas lineas son para un sujeto
			trial_id, prime, pair, res, keys = line.split(" ", 4)
			
			trials_by_subject_id[i].append((trial_id, prime, pair, res, keys))
			print "Sujeto {}, trial {} {} {} {} {}".format(subject_id, trial_id, prime, pair, res, keys)
			i += 1
			line = lines[i]
		i += 1
		subject_id += 1
	return trials_by_subject_id
	
# separa las clasificaciones correctas de las incorrectas.
#  Left -> Letra, Right -> Numero
def split_by_class(trials_by_subject_id):
	correct = []
	incorrect = []
	for subj_id, trial in trials_by_subject_id:
		(trial_id, prime, pair, res, keys) = trial
		
			
	# while len(lines) != 0:
		# #Si no guardo los resultados de las letras el n es distinto al de generadorDePares
		# for i in range(n):
			# trial_id, prime, pair, res, keys = line.split(" ")
			# left, right = pair.split(",")
			# trial_results_by_index[trial_id].append(keys)

			# key = prime

			# if(res.isalpha()):
				# key = key + "letra"
			# elif int(left) + int(right) == int(res)
				# key = key + "correcto"
			# else:
				# key = key + "incorrecto"
			# trial_results_by_type[key].append(keys)
	# results.close()

	#Esto lo vamos a cambiar, es para mostrar que podemos ir agrupando los valores como querramos
	# with open("resultsByTrial.txt", "w") as f:
		# for trial_id, keys in trial_results_by_index
			# s = "Trial id: {}, Keys: {} ".format(trial_id, keys)
			# f.write("%s\n" % s)
	# f.close()

	# with open("resultsByType", "w") as f:
		# for trial_type, keys in trial_results_by_index
			# s = "Trial id: {}, Keys: {} ".format(trial_type, keys)
			# f.write("%s\n" % s)
	# f.close()	

if __name__ == '__main__':
	trials_by_subject_id = main()
	split_by_class()
	