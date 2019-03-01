TGT_CPU=3
mkdir /dev/cpuset
mount -t cgroup -o cpuset cpuset /dev/cpuset
cd /dev/cpuset
mkdir cpu${TGT_CPU}
echo ${TGT_CPU} > cpu${TGT_CPU}/cpuset.cpus
echo 0 > cpu${TGT_CPU}/cpuset.mems
echo 1 > cpuset.cpu_exclusive
echo 0 > cpuset.sched_load_balance
echo 1 > cpu${TGT_CPU}/cpuset.cpu_exclusive
echo 1 > cpu${TGT_CPU}/cpuset.mem_exclusive
echo $$ > cpu${TGT_CPU}/tasks
