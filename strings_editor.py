#! /usr/bin/env python3

def encode(data):
	for i in range(10):
		data = data.replace(str(i).encode(), bytes((i, )))
	for i in range(0xa, 0x24):
		data = data.replace(chr(ord('A') + i - 0xa).encode(), bytes((i, )))
	data = data.replace(b' ', b'$')
	data = data.replace(b';', b'(')
	data = data.replace(b'.', b'&')
	return data

def decode(data):
	for i in range(10):
		data = data.replace(bytes((i, )), str(i).encode())
	for i in range(0xa, 0x24):
		data = data.replace(bytes((i, )), chr(ord('A') + i - 0xa).encode())
	data = data.replace(b'$', b' ')
	data = data.replace(b'(', b';')
	data = data.replace(b'&', b'.')
	return data


def search_words(data, word):
	offset = -1
	resault = []

	while True:
		offset = data.find(encode(word), offset + 1)
		if offset == -1:
			for offset in resault:
				print (decode(data[offset - 3 : offset + len(word) + 3]))
			return resault
		resault.append(offset)

def replace_word(data, english_word, hebrew_word):
	hebrew_word = hebrew_word.ljust(len(english_word))
	assert not len(hebrew_word) > len(english_word)
	for offset in search_words(data, english_word):
		data = data[: offset] + encode(hebrew_word[::-1]) + data[offset + len(english_word) :]
	return data

def main():
	with open('mario_bros.nes', 'rb') as fd:
		data = fd.read()

	data = replace_word(data, b'1 PLAYER GAME A', b'AJEI TJS NAJE T')
	data = replace_word(data, b'1 PLAYER GAME B', b'AJEI TJS NAJE C')
	data = replace_word(data, b'2 PLAYER GAME A', b'AJEI ABH NAJE T')
	data = replace_word(data, b'2 PLAYER GAME B', b'AJEI ABH NAJE C')
	data = replace_word(data, b'MARIO GAME OVER', b'NRHU VPXHS')
	data = replace_word(data, b'LUIGI GAME OVER', b'KTHDH VPXHS') # Note that we wrote here לואיגי without all the characters.
	data = replace_word(data, b'NO BONUS', b'THI CUBX') # Note that we wrote here בונוס without all the characters.
	data = replace_word(data, b'GAME', b'NAJE')
	data = replace_word(data, b'PERFECT', b'NUAKO')
	data = replace_word(data, b' NINTENDO CO;LTD.', b'   BHBYBSU CGN')
	data = replace_word(data, b'MADE IN JAPAN', b'BUMR CHPI')
	data = replace_word(data, b'IN', b'C')
	data = replace_word(data, b'JAPAN', b'HPI')
	data = replace_word(data, b'MADE', b'BUMR')
	data = replace_word(data, b'MARIO', b'NRHU')
	data = replace_word(data, b'NINTENDO', b'BHBYBSU')
	data = replace_word(data, b'OVER', b'BDNR')
	data = replace_word(data, b'PHASE', b'JKE')
	data = replace_word(data, b'TOP', b'AHT')
	data = replace_word(data, b'PLAYER', b'AJEI')
	data = replace_word(data, b'TEST YOUR SKILL', b'CJI TQ HFUKQL')
	data = replace_word(data, b'LUIGI', b'KTHDH') # Note that we wrote here לואיגי without all the characters.

	with open('mario_bros.modified.nes', 'wb') as fd:
		fd.write(data)

if __name__ == '__main__':
	main()


