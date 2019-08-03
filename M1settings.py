gen_prob = [0.4, 0.5, 0.6]
ratio = [0.3, 0.5, 0.7]

for g in gen_prob:
	for r in ratio:
		d = g - 0.1
		print('\t'.join([str(i) for i in (g, d, r)]))
		d = g - 0.2
		print('\t'.join([str(i) for i in (g, d, r)]))
