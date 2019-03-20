events=("sched_switch" "sched_wakeup" "sched_wakeup_new")
debugfs_path=/sys/kernel/debug
trace_path=${debugfs_path}/tracing
sched_events_path=${trace_path}/events/sched

enable_tracing () {
	echo > ${trace_path}/trace
	echo 1 > ${trace_path}/tracing_on
	for event in ${events[@]}; do
		echo 1 > ${sched_events_path}/${event}/enable
	done
}

disable_tracing () {
	for event in ${events[@]}; do
		echo 0 > ${sched_events_path}/${event}/enable
	done
	echo 0 > ${trace_path}/tracing_on
}

enable_tracing
# ./test_deadline
echo $$ >> cpuset/cpu3/tasks
tau_1 -u 20  -d 100 -m 32 -t 10 &
# echo $$ >> cpuset/cpu4/tasks
tau_2 -u 40  -d 150 -m 32 -t 10 &
# echo $$ >> cpuset/cpu5/tasks
tau_3 -u 100 -d 350 -m 32 -t 10
disable_tracing
cp ${trace_path}/trace profile.dat
