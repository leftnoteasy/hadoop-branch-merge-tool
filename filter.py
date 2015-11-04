import sys

if __name__ == "__main__":
	dict1 = set()
        for line in open(sys.argv[1]):
		dict1.add(line)

        for line in open(sys.argv[2]):
             if dict1.__contains__(line):
                dict1.remove(line)

        for line in dict1:
		print line.strip()
        
