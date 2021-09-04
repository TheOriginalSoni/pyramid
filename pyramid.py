import itertools

allwords=[]
f = open("/home/soni/coding/pyramid/enablewordlist.txt", "r")

max_len = 0
for x in f:
	allwords.append(x.strip())
	max_len=max(max_len,len(x.strip()))
f.close()

wordsbylen = []
for i in range(max_len+1):
	wordsbylen.append(set())

for x in allwords:
	l = len(x)
	wordsbylen[l].add(x)

#for j in wordsbylen:
#	print (f"{len(j)} \t")

print(f"All words = {len(allwords)}")

def caesar(word,n):
	 z = "".join(list(map(lambda x: chr(ord(x)+n) if ord(x) + n <=122 else chr(ord(x)+n-26), [char for char in word])))
	 return z

def caesarable_helper(words):
	caesarable = set()
	k=0
	for x in words:
		if (x not in caesarable):
			#if(k%10==0):
			#	print(k)
			for i in range(1,26):
				x2 = caesar(x,i)
				if(x2 in words and x<x2):
					caesarable.add(x)
					caesarable.add(x2)
		k=k+1
	return caesarable

def list_caesarable(wordsbylen):
	cs = set()
	for j in wordsbylen:
		cs1 = caesarable_helper(j)
		#print(f"{len(j)} - {len(cs1)}")
		cs.update(cs1)
	return cs

caesarable_words = list_caesarable(wordsbylen)
print(f"Caesarable = {len(caesarable_words)}")

def filter_caesar(words,yn):
	fs = set()
	if(yn):
		for w in words:
			if w in caesarable_words:
				fs.add(w)
	else:
		for w in words:
			if w not in caesarable_words:
				fs.add(w)
	return fs

def scrabble_score(word):
	scores = {"a":1, "e":1, "i":1, "o":1, "u":1, "l":1, "n":1, "s":1, "t":1, "r":1, "d":2, "g":2, "b":3, "c":3, "m":3, "p":3, "f":4, "h":4, "v":4, "w":4, "y":4, "k":5, "j":8, "x":8, "q":10, "z":10}
	x = sum(list(map(lambda x:scores[x],[char for char in word])))
	return x

def filter_scrabble_score(words, n):
	lsc = set()
	for x in words:
		if(scrabble_score(x)==n):
			lsc.add(x)
	return lsc

def sortedchars_helper(words):
	allsorted = {}
	for x in words:
		sx = "".join(sorted(x))
		if sx in allsorted:
			allsorted[sx].add(x)
		else:
			allsorted[sx]=set()
			allsorted[sx].add(x)
	return allsorted

def list_sortedchars(wordsbylen):
	cs = []
	for i in range(max_len+1):
		cs_by_len = sortedchars_helper(wordsbylen[i])
		cs.append(cs_by_len)
	return cs

sorted_letters_by_len = list_sortedchars(wordsbylen)

def list_anagrams_plus_n(listwords,sortedwords,n):
	l_anag = set()
	y = list(itertools.permutations(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],n))
	a = list(map(lambda x:"".join(x),y))
	for x in listwords:
		for xadd in a:
			sx = "".join(sorted(x+xadd))
			if sx in sortedwords:
				if(n==0):
					if(len(sortedwords[sx])>1):
						l_anag.add(x)
				else:
					l_anag.add(x)
	return l_anag

def list_anagrams(wordsbylen,sorted_letters_by_len,n):
	ans = set()
	for i in range(max_len+1-n):
		ang_s = list_anagrams_plus_n(wordsbylen[i],sorted_letters_by_len[i+n],n)
		ans.update(ang_s)
	return ans

anagrammable_words = list_anagrams(wordsbylen,sorted_letters_by_len,0)

print(f"Anagrammable = {len(anagrammable_words)}")

anagrammable_words_plus1 = list_anagrams(wordsbylen,sorted_letters_by_len,1)

print(f"Anagrammable + 1 = {len(anagrammable_words_plus1)}")

anagrammable_words_plus2 = list_anagrams(wordsbylen,sorted_letters_by_len,2)

print(f"Anagrammable + 2 = {len(anagrammable_words_plus2)}")

def filter_anagrams(words,yn,n):
	fs = set()
	mainset = set()
	if(n==0):
		mainset = anagrammable_words
	elif(n==1):
		mainset = anagrammable_words_plus1
	elif(n==2):
		mainset = anagrammable_words_plus2
	if(yn):
		for w in words:
			if w in mainset:
				fs.add(w)
	else:
		for w in words:
			if w not in mainset:
				fs.add(w)
	return fs

f = open("/home/soni/coding/pyramid/words_anagram.txt", "a")
for j in sorted(list(anagrammable_words_plus2)):
	f.write(f"{j}\n")
	pass
f.close()
