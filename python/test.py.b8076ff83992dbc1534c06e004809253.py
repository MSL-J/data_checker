import sys, json




print("from Python to JS")

#스트링으로 받아온 값을 다시 dict로 parsing
print(json.loads(sys.argv[1]))

print(sys.argv[1])

