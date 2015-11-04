import sys

if __name__ == "__main__":
   patterns = ["YARN-", "MAPREDUCE-", "HADOOP-", "BUG-"]
   for line in sys.stdin:
        for p in patterns:
                start = 0
		while line.find(p, start) != -1:
                        start  = line.find(p, start)
			t = start + len(p)
			while line[t].isdigit():
				t = t + 1
			print line[start:t]
			start = start + t
	
