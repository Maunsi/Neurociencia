def analyze(trials_by_subject, control_by_subject):
	#Elimino todos los trials del sujeto si el control me da >= 4. Existe algun motivo por el cual querriamos conservarlos?
	amount_dropped = 0
	total = 0
	for subject, control in control_by_subject.iteritems():
		if int(control) >= 4:
			trials_by_subject.pop(subject)
			amount_dropped += 1
		else:
			total += control

	mean = total/len(control_by_subject.values())

	print "Cantidad de sujetxs desechados: {}".format(amount_dropped)
	print "Promedio de visibilidad entre los sujetxs restantes: {}".format(mean)