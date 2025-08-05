# 🧠 CPU Scheduler — Python

## 📄 Description

This project, developed as part of the **Operating Systems I** course at the **Federal University of Paraíba (UFPB)**, is a CPU scheduling simulator. The program implements and compares three classic scheduling algorithms:
- **FCFS**: First-Come, First-Served 
- **SJF**: Shortest Job First (non-preemptive) 
- **RR**: Round Robin (with fixed quantum = 2) 

The program reads a list of processes from an input file and calculates performance metrics for each algorithm. The output includes the average turnaround time, average response time, and average waiting time, formatted with one decimal place and using a comma as the decimal separator. The input is a series of pairs of integers separated by a space, indicating the arrival time and duration of each process. The input ends with the end of the file.

---

## 📁 Project Structure

```
.
├── input.txt            # Input file with process data
├── main.py              # Main Python script with all logic
├── main.ipynb              # Main Jupyter script with all logic
├── README.md            # This file
```

---

## ▶️ How to Run

### 1. 💾 Add input data to `input.txt`

Each line must contain **two integers** separated by a space:

```
<arrival_time> <burst_time>
```

Example:

```
0 10
4 4
8 6
21 8
```

### 2. ▶️ Run the script using Python 3

```bash
python3 main.py
```

#### Running in Interactive Environments (Google Colab)
To run this project in Google Colab, you would need to implement an interactive upload method, as the environment does not directly support command-line file redirection.

---

## 📤 Sample Output

The output consists of lines, each containing the acronym of an algorithm and the values of the three requested metrics. The average values are presented with one decimal place and separated by a space, in this exact order: turnaround time, response time, and waiting time.
```
FCFS: 10,0 3,0 3,0
SJF: 10,0 3,0 3,0
RR: 11,0 0,5 4,0
```

Each line corresponds to one scheduling algorithm, followed by the **averages** in the following order:

1. ⏱ **Turnaround time**
2. 🎯 **Response time**
3. 🕓 **Waiting time**

---

## ⚙️ Implemented Algorithms

- ✅ FCFS: executes processes in order of arrival
- ✅ SJF (non-preemptive): picks the shortest job available
- ✅ RR with quantum = 2: executes time-sliced in round-robin order

All algorithms compute the metrics as follows:

- **Turnaround time** = completion time − arrival time
- **Waiting time** = turnaround time − burst time
- **Response time** = first execution time − arrival time

---

## ⚠️ Notes

- The file `input.txt` must be in the **same directory** as `main.py`.
- Invalid lines in the input are **ignored automatically**.
- Output format is strictly followed to match automatic grading requirements.
- No external libraries are used — fully written in pure Python.
