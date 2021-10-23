import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from subprocess import Popen, PIPE, STDOUT

n = input("please input n: ")
testcase = input("please input testcase: ")

def print_command(p):
  for line in p.stdout:
    print(line.strip())

p = Popen(["make clean"], shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
print_command(p)

p = Popen(["make"], shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
print_command(p)

'''for different node with total 12 process experiment'''
result_cpu = list()
result_comm = list()
result_io = list()
node_num = [1, 2, 3, 4]

for node in tqdm(node_num):
  min_node = int(12 / node)
  cmd = f"srun -N{node} -n12 --mincpus={min_node} ./hw1 {n} {testcase}.in {testcase}.out"
  p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
  line = [i for i in p.stdout]
  result_cpu.append(float(line[0]))
  result_comm.append(float(line[1]))
  result_io.append(float(line[2]))

labels = [str(i) for i in node_num]

# bar chart for different process number's CPU, COMM, IO time
fig, ax = plt.subplots()
ax.bar(labels, result_cpu, label='CPU_time')
ax.bar(labels, result_comm, bottom=result_cpu, label='COMM_time')
ax.bar(labels, result_io, bottom=np.array(result_cpu)+np.array(result_comm), label='IO_time')
ax.set_xlabel("process number")
ax.set_ylabel("runtime (seconds)")
ax.set_title(f"multi node with same process performance")
ax.legend(loc="upper right")
fig.savefig(f"./images/{testcase}_multi_node_same_proc_bar.png")

# line chart for speed up factor
results = [result_cpu[i]+result_comm[i]+result_io[i] for i in range(len(node_num))]
total = [results[0]/results[i] for i in range(len(node_num))]
plt.figure(dpi=100, linewidth=2)
plt.plot(node_num, total, 'o-', color='g')
plt.xlabel('node number')
plt.xticks(np.arange(1, 5, 1))
plt.ylabel('Speedup Factor')
plt.title(f"multi node with same process speedup factor")
plt.savefig(f"./images/{testcase}_multi_node_same_pro_line.png")