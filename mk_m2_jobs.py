gen_prob = [0.4, 0.5, 0.6]
ratios = [0.3, 0.5, 0.7]
model = 'm1.py'
slurm_dir = './slurms/m1/'

temp = open('scripts/sbatch.temp').read()
id = 0
for g in gen_prob:
        for r in ratios:
                d = g - 0.1
                args = ' '.join([str(i) for i in (g, d, r)])
                f = open(slurm_dir + str(id) + '.sbatch', 'w')
                f.write(temp.format(model=model, args=args))
                id += 1

                d = g - 0.2
                args = ' '.join([str(i) for i in (g, d, r)])
                f = open(slurm_dir + str(id) + '.sbatch', 'w')
                f.write(temp.format(model=model, args=args))
                id += 1
