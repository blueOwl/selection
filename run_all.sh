work_dir='./slurms/m1'
cd $work_dir
for i in `ls ./`; do
 sbatch $i
done
