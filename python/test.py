import sys, json




print("from Python to JS")

#스트링으로 받아온 값을 다시 dict로 parsing
print(json.loads(sys.argv[2]))

print(sys.argv[2])

sys.stdout.flush()