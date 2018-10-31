from trial import Trial

def analyze(trials_by_subject, control_by_subject):
	trials_by_subject = filter_over_four(trials_by_subject, control_by_subject)
	trials_by_subject = filter_letter_trials(trials_by_subject)




def filter_letter_trials(trials_by_subject):
	new_dictionary = {}
	for subject, trials in trials_by_subject.iteritems():
		new_dictionary[subject] = {}
		for trial, responses in trials:
			if not trial.is_letter_trial():
				new_dictionary[subject][trial] = responses

	return trials_by_subject

def filter_over_four(trials_by_subject, control_by_subject):
	amount_dropped = 0
	total = 0
	for subject, control in control_by_subject.iteritems():
		if int(control) >= 4:
			trials_by_subject.pop(subject)
			amount_dropped += 1
		else:
			total += int(control)

	mean = total/len(control_by_subject.values())

	print "Cantidad de sujetxs desechados: {}".format(amount_dropped)
	print "Promedio de visibilidad entre los sujetxs restantes: {}".format(mean)

	return trials_by_subject