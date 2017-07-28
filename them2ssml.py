import sys
import os
import string
import re
#import logging
from random import randint
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

fpath = sys.argv[1]
#ext = fpath.split(".")[-1]

infile = open(fpath,"r").read()

dictTags = {}
dictTags["pitch"] = {}
dictTags["pitch"]["T+9"] = 5
dictTags["pitch"]["T-9"] = 35
dictTags["pitch"]["R"] = 15
dictTags["pitch"]["SP"] = -15
dictTags["pitch"]["P"] = 5
dictTags["pitch"]["T(R)"] = 15
dictTags["pitch"]["T(T)"] = 25
dictTags["pitch"]["R(R)"] = -15
dictTags["pitch"]["R(T)"] = 35

dictTags["rate"] = {}
dictTags["rate"]["T+9"] = 15
dictTags["rate"]["T-9"] = 25
dictTags["rate"]["R"] = 10
dictTags["rate"]["SP"] = 35
dictTags["rate"]["P"] = -10
dictTags["rate"]["P"] = -10
dictTags["rate"]["T(R)"] = 50
dictTags["rate"]["T(T)"] = 15
dictTags["rate"]["R(R)"] = 25
dictTags["rate"]["R(T)"] = 45

dictTags["volume"] = {}
dictTags["volume"]["T+9"] = -20
dictTags["volume"]["T-9"] = 20
dictTags["volume"]["R"] = -5
dictTags["volume"]["SP"] = -10
dictTags["volume"]["P"] = 30
dictTags["volume"]["T(R)"] = 15
dictTags["volume"]["T(T)"] = 30
dictTags["volume"]["R(R)"] = -25
dictTags["volume"]["R(T)"] = 30

keysDict = dictTags.keys()

def getPlusValue(posVal):
	if posVal > 0:
		posVal = "+" + str(posVal)
	else:
		posVal = str(posVal)
	return posVal

def insertProsodyTag(value, result, token, pos, splitWith = "]"):
	vals = range(value-5, value+5, 5)
	randIdx = randint(0, len(vals)-1)
	randVal = vals[randIdx]
	plusValue = getPlusValue(randVal)
	label = "<prosody "+ key + "=\""+ plusValue + "%\">"
	result.insert(pos,label)
	wordend = token.split(splitWith)[0]
	result.append(wordend + "</prosody>")

#logging.debug("Processing txt file")
sentences = infile.split("\n\n")
result = []
checklist = ["[","{","}P2]","]T1","]R1","]SP1","]T1(T1)", "]R1(T1)", "]T1(R1)", "]R1(R1)", "}P"]

for sentence in sentences:
	tokens = sentence.split(" ")
	pos = 0
	idr = randint(0,len(keysDict)-1)
	key = keysDict[idr]
	for idx,token in enumerate(tokens, 1):
		#print idx, token
		# Find the begining of a thematicity span and store its position
		if token.find(checklist[0]) != -1:
			result.append(token[1:])
			pos = len(result) - 1
		# Apply prosody considering type of span (T, R, SP, P)		
		elif token.find(checklist[3]) != -1:
			# Check theme does not contain embedded spans
			if re.findall("\D\]T1",token):
				# Apply modifications accoring to theme length
				if idx >= 9: 
					val = dictTags[key]["T+9"]
					insertProsodyTag(val, result, token, pos)
				else:
					val = dictTags[key]["T-9"]
					insertProsodyTag(val, result, token, pos)
			elif re.findall("\d\]T1",token) and checklist[2] in token:
				val = dictTags[key]["P"]
				insertProsodyTag(val, result, token, pos, "}")

		elif token.find(checklist[4]) != -1:
			val = dictTags[key]["R"]
			insertProsodyTag(val, result, token, pos)

		elif token.find(checklist[5]) != -1:
			val = dictTags[key]["SP"]
			insertProsodyTag(val, result, token, pos)
		elif token.endswith("]T1(T1)"):
			print checklist[6]
			val = dictTags[key]["T(T)"]
			insertProsodyTag(val, result, token, pos)
		elif token.find(checklist[7]) != -1:
			val = dictTags[key]["R(T)"]
			insertProsodyTag(val, result, token, pos)
		elif token.find(checklist[8]) != -1:
			val = dictTags[key]["T(R)"]
			insertProsodyTag(val, result, token, pos)
		elif token.find(checklist[9]) != -1:
			val = dictTags[key]["R(R)"]
			insertProsodyTag(val, result, token, pos)
		elif checklist[10] in token:
			val = dictTags[key]["P"]
			insertProsodyTag(val, result, token, pos, "}")
	
		# Include words with no thematicity marker
		else:		
			found = False
			for c in checklist:
				if c in token:
					found = True
					break
			if checklist[1] in token:
				result.append(token[1:])
			if not found:
				result.append(token)
	result.append("\n\n")

print " ".join(result)
