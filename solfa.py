#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#////////////////////////////////////////////////////////////////////////////// 
# 
# Copyright (C) 2017 Jonathan Racicot 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http:#www.gnu.org/licenses/>. 
# 
# You are free to use and modify this code for your own software  
# as long as you retain information about the original author 
# in your code as shown below. 
# 
# <author>Jonathan Racicot</author> 
# <email>cyberrecce@gmail.com</email> 
# <date>2017-03-07</date> 
# <url>https://github.com/infectedpacket</url> 
#////////////////////////////////////////////////////////////////////////////// 
# Program Information 
# 
PROGRAM_NAME = "b" 
PROGRAM_DESC = "" 
PROGRAM_USAGE = '''
%(prog)s " 
'''

__version_info__ = ('0','1','0') 
__version__ = '.'.join(__version_info__) 
 
#////////////////////////////////////////////////////////////////////////////// 
# Imports Statements
import argparse
#
#//////////////////////////////////////////////////////////////////////////////
# Global variables and constants
#
SOLFA_DECRYPT = 0
SOLFA_ENCRYPT = 1

SOLFA_DO = "d"
SOLFA_RE = "r"
SOLFA_MI = "m"
SOLFA_FA = "f"
SOLFA_SOL= "s"
SOLFA_LA = "l"
SOLFA_SI = "t"
SOLFA_SL = "z"
SOLFA_BAR = "|"
SOLFA_NOTES = [
	SOLFA_DO,
	SOLFA_RE,
	SOLFA_MI,
	SOLFA_FA,
	SOLFA_SOL,
	SOLFA_LA,
	SOLFA_SI
]

SOLFA_CLEF_TREBLE = "treble"
SOLFA_CLEF_ALTO = "alto"
SOLFA_CLEF_BASS = "bass"
SOLFA_CLEFS = [
	SOLFA_CLEF_TREBLE,
	SOLFA_CLEF_ALTO,
	SOLFA_CLEF_BASS
]

SOLFA_MODE_MAJOR = "major"
SOLFA_MODE_DORIAN = "dorian"
SOLFA_MODE_PHRYGIAN = "phrygian"
SOLFA_MODE_LYDIAN = "lydian"
SOLFA_MODE_MIXOLYDIAN = "mixolydian"
SOLFA_MODE_MINOR = "minor"
SOLFA_MODE_LOCRIAN = "locrian"
SOLFA_MODES = [
	SOLFA_MODE_MAJOR,
	SOLFA_MODE_DORIAN,
	SOLFA_MODE_PHRYGIAN,
	SOLFA_MODE_LYDIAN,
	SOLFA_MODE_MIXOLYDIAN,
	SOLFA_MODE_MINOR,
	SOLFA_MODE_LOCRIAN
]

SOLFA_RHYTHM_QUARTER = "1/4"
SOLFA_RHYTHM_EIGHTH = "1/8"
SOLFA_RHYTHM_SIXTEEN = "1/16"
SOLFA_RHYTHMS = [
	SOLFA_RHYTHM_QUARTER,
	SOLFA_RHYTHM_EIGHTH,
	SOLFA_RHYTHM_SIXTEEN
]

SOLFA_UNDEFINED = "none"

SCALES = [
	'C,,', 'D,,', 'E,,', 'F,,', 'G,,', 'A,,', 'B,,',
	'C,' , 'D,' , 'E,' , 'F,' , 'G,' , 'A,' , 'B,',
	'C'  , 'D'  , 'E'  , 'F'  , 'G'  , 'A'  , 'B',
	'c'  , 'd ' , 'e'  , 'f ' , 'g'  , 'a'  , 'b',
	'c\'', 'd\''
	]
	
CHROMATIC_NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

ENGLISH_MATRIX = {
	SOLFA_DO	:	["T", "K", "R", "F"],
	SOLFA_RE	:	["I", "Z", "C", "Y"],
	SOLFA_MI	:	["A", "X", "H", "G"],
	SOLFA_FA	:	["S", "Q", "M", "P"],
	SOLFA_SOL	:	["E", "J", "D", "W"],
	SOLFA_LA	:	["N", "Å", "L", "B"],
	SOLFA_SI	:	["O", "Æ", "U", "V"]
}
#
#//////////////////////////////////////////////////////////////////////////////
#
#////////////////////////////////////////////////////////////////////////////// 
# Argument Parser Declaration 
# 
usage = PROGRAM_USAGE 
parser = argparse.ArgumentParser( 
	usage=usage,  
	prog=PROGRAM_NAME,  
	version="%(prog)s "+__version__,  
	description=PROGRAM_DESC) 

crypto_options =parser.add_argument_group("Crypto Options", "Options relating to the Solfa crypto")
crypto_options.add_argument("-m", "--msg", 
	dest="message", 
	required=True,
	help="Specifies the message to decrypt or encrypt.")
crypto_options.add_argument("-d", "--decrypt", 
	dest="do_decrypt", 
	action="store_true",
	help="Tells the program to decrypt the provided message. If not specified, the program will encrypt the provided message by default.")
	
#////////////////////////////////////////////////////////////////////////////// 
# Code
#
class SolfaMatrix(object):
	'''
	A SolfaMatrix regroups the variables and methods needed to translate
	between the alphabet of a natural language and musical notes and tempo.
	
	The matrix used for the Solfa cipher is a 4x7 matrix, i.e. 4 rows 
	representing the tempo and 7 columns for the 7 tone (Do, Re, Mi...).
	Each character of the alphabet is represented by a tuple of a tone and
	a tempo. For example, the letter T can be translate to (Do, 1).
	
	The standard matrix used for the English alphabet is the following:
	
          |  1  |  2  |  3  |  4  |
        --|-----|-----|-----|-----|
        d | T   | K   | R   | F   |
        f | S   | Q   | M   | P   |
        m | A   | X   | H   | G   |
        l | N   | ├à  | L   | B   |
        s | E   | J   | D   | W   |
        r | I   | Z   | C   | Y   |
        t | O   | ├å  | U   | V   |
        --|-----|-----|-----|-----|
		
	Where d = "Do", r = "Re", m = "Mi", f = "Fa", s = "Sol", l = "La", t = "Si".
	
	Customized matrix can be used as long as the receiving party of the encrypted
	message uses the same matrix.
	'''

	def __init__(self, _matrix = ENGLISH_MATRIX):
		'''
		Initializes the SolfaMatrix object using the specified translation
		matrix. If none is provided, the ENGLISH_MATRIX is used by default.
		
		@param _matrix The translation matrix to use.
		'''
		self.matrix = _matrix

	def __str__(self):
		'''
		Returns a string representation of the matrix defined.
		
		@return A string representing the matrix currently used
		by the object.
		'''
		matx_hdr = "\t  |  1  |  2  |  3  |  4  |\n"
		matx_ln  = "\t--|-----|-----|-----|-----|\n"
		line_fmt = "\t{t:s} | {c1: <4}| {c2: <4}| {c3: <4}| {c4: <4}|\n"
		
		s = matx_hdr
		s += matx_ln
		
		for tone in self.matrix.keys():
			tsln = self.matrix[tone]
			s += line_fmt.format(t=tone, c1=tsln[0], c2=tsln[1], c3=tsln[2], c4=tsln[3])
		s += matx_ln
		
		return s
		
	def translate_single_char(self, _char):
		'''
		Translate a single character from a natural language alphabet
		into a note.
		
		This function will take in a single character from a given alphabet
		and seek its position into the matrix. The function will return a tuple
		containing the solfege note and tempo corresponding to the character. If
		no matching character is found in the matrix, this function will return
		(None, None)
		
		Example:
		>> matrix = SolfaMatrix()
		>> (note, tempo) = matrix.translate_single_char("T")
		(note, tempo) = ("d", 1)
		
		@param _char The character to translate
		@return A tuple containing the note and tempo corresponding to the
		given character, or (None, None) if not found.
		'''
		for tone in self.matrix.keys():
			letters = self.matrix[tone]
			if _char in letters:
				return (tone,  letters.index(_char)+1)
		return (None, None)
	
	def translate_string(self, _chars):
		'''
		Translate a string into a list of corresponding notes and tempo for each
		character of the given string.
		
		This function simply uses the SolfaMatrix.translate_single_char on
		each character of the string. Each resulting tuple is appended to a list
		which is returned by this function.
		
		@param _chars A string to translate
		@return A list of tuples, each containing the note and tempo corresponding
		to a character in the string.
		'''
		cipher_chars = []
		for character in _chars:
			translation = self.translate_single_char(character)
			if translation[0] != None and translation[1] != None:
				cipher_chars.append(translation)
			else:
				raise Exception("Failed to translate character '{ch:s}'.".format(ch=character))
		return cipher_chars
	
	def translate_single_note(self, _note, _tempo):
		plain_char = ""
		index = int(_tempo) - 1
		if _note in self.matrix.keys():
			if index >= 0 and index < len(self.matrix[SOLFA_DO]):
				plain_char = self.matrix[_note][index]
		return plain_char		

	def translate_multiple_notes(self, _notes):
		plaintext = ""
		for note in _notes:
			if len(note) == 2:
				tone = note[0]
				time = note[1]
				plaintext += self.translate_single_note(tone, time)
		return plaintext
	
class SolfaKey(object):

	def __init__(self, _clef, _tonic, _mode, _rhythm):
		self.clef = _clef
		self.tonic = _tonic
		self.mode = _mode
		self.rhythm_unit = _rhythm
		self.meter = "4/4"
		
	def __str__(self):
		key = self.mode
		if self.tonic != SOLFA_UNDEFINED:
			key = "{md:s} {tn:s}".format(md=self.mode, tn=self.tonic)
			
		abc_format = "[K:{k:s} clef={clef:s}] [L:{rhythm:s}] [M:{meter:s}]"
		return abc_format.format(
			k=key,
			clef=self.clef,
			rhythm=self.rhythm_unit,
			meter=self.meter)
	
	@staticmethod
	def empty_key():
		'''
		Generates an empty Solfa key.
		
		This static function can be called to create a Solfa key in which
		all properties are set to SOLFA_UNDEFINED.
		
		@return A SolfaKey object in which all properties are set to SOLFA_UNDEFINED
		'''
		return SolfaKey(
			_clef = SOLFA_UNDEFINED, 
			_tonic = SOLFA_UNDEFINED,
			_mode = SOLFA_UNDEFINED, 
			_rhythm = SOLFA_UNDEFINED)
		
class SolfaMessage(object):

	def __init__(self, _message):
		self.message = _message
		self.key = None
		
	def __str__(self):
		return self.message

			
class SolfaCipherMessage(SolfaMessage):

	def __init__(self, _ciphertext):
		super(SolfaCipherMessage, self).__init__(_ciphertext)
			
	def decrypt(self, _solfa_key, _matrix = None):
		self.key = _solfa_key
		self.matrix = _matrix
		if self.matrix == None: self.matrix = SolfaMatrix()
	
class SolfaPlainMessage(SolfaMessage):

	def __init__(self, _plaintext):
		super(SolfaPlainMessage, self).__init__(_plaintext.upper())

	def encrypt(self, _solfa_key, _decoy_key = None, _matrix = None):
		self.key = _solfa_key
		self.matrix = _matrix
		self.decoy_key = _decoy_key
		if self.matrix == None: 
			self.matrix = SolfaMatrix()
		if self.decoy_key == None: 
			self.decoy_key = self._generate_default_decoy_key()
		
		# Translate plain text message into a solfege note and a timing,
		# ex. T -> ("d", 1)
		translated_notes = self.matrix.translate_string(self.message)
		
		tonic = self._calculate_delta_tonic(self.key, self.decoy_key)
		
		# Convert the solfege notes into the chromatic scale
		chromatic_notes_and_beats = self._translate_to_chromatic_notes(
			translated_notes, tonic)
			
		# Add a terminator to the melody
		chromatic_notes_and_beats.append((SOLFA_BAR, 1))
		
		bar_value = self._bar_value(self.key.rhythm_unit, self.key.meter)
		
		# Converts the melody into the ABC notation so it can be 
		# translated into other formats.
		ciphertext = self._to_abc_notation(chromatic_notes_and_beats, bar_value)
		ciphertext = ' '.join(
		["{n:s}{t:d}".format(n=note, t=time) for (note, time) in ciphertext])
		return SolfaCipherMessage(ciphertext)
		
	def _generate_default_decoy_key():
		'''
		Generates a default decoy key to be included in the encrypted
		message.
		
		By default, the decoy key generated is empty, i.e. all properties
		of the key are set to SOLFA_UNDEFINED.
		
		@return A SolfaKey object with all properties set to SOLFA_UNDEFINED
		'''
		return SolfaKey(
			_clef = SOLFA_UNDEFINED, 
			_tonic = SOLFA_UNDEFINED,
			_mode = SOLFA_UNDEFINED, 
			_rhythm = SOLFA_UNDEFINED)
	
	def _calculate_delta_tonic(self, _key, _decoy_key):
		shift = 0
		tonic = 0
		
		if _key.clef == SOLFA_CLEF_TREBLE:
			if _decoy_key.clef == SOLFA_CLEF_ALTO:
				shift = -6
			elif _decoy_key.clef == SOLFA_CLEF_BASS:
				shift = -12
		elif _key.clef == SOLFA_CLEF_ALTO:
			if _decoy_key.clef == SOLFA_UNDEFINED or _decoy_key.clef == SOLFA_CLEF_TREBLE:
				shift = 6
			elif _decoy_key.clef == SOLFA_CLEF_BASS:
				shift = -6
		elif _key.clef == SOLFA_CLEF_BASS:
			if _decoy_key.clef == SOLFA_UNDEFINED or _decoy_key.clef == SOLFA_CLEF_TREBLE:
				shift = 12
			elif _decoy_key.clef == SOLFA_CLEF_ALTO:
				shift = 6
		
		if _key.tonic[0] == "C":
			if _key.clef == SOLFA_CLEF_TREBLE or _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 13
			elif _key.clef == SOLFA_CLEF_BASS:
				tonic = shift + 6
		elif _key.tonic[0] == "D":
			if _key.clef == SOLFA_CLEF_TREBLE or _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 14
			elif _key.clef == SOLFA_CLEF_BASS:
				tonic = shift + 7
		elif _key.tonic[0] == "E":
			if _key.clef == SOLFA_CLEF_TREBLE:
				tonic = shift + 15
			elif _key.clef == SOLFA_CLEF_BASS or _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 8
		elif _key.tonic[0] == "F":
			if _key.clef == SOLFA_CLEF_TREBLE:
				tonic = shift + 16
			elif _key.clef == SOLFA_CLEF_BASS or _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 9	
		elif _key.tonic[0] == "G":
			if _key.clef == SOLFA_CLEF_TREBLE:
				tonic = shift + 18
			elif _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 10
			elif _key.clef == SOLFA_CLEF_BASS:
				tonic = shift + 3
		elif _key.tonic[0] == "A":
			if _key.clef == SOLFA_CLEF_TREBLE:
				tonic = shift + 18
			elif _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 11
			elif _key.clef == SOLFA_CLEF_BASS:
				tonic = shift + 4
		elif _key.tonic[0] == "B":
			if _key.clef == SOLFA_CLEF_TREBLE:
				tonic = shift + 19
			elif _key.clef == SOLFA_CLEF_ALTO:
				tonic = shift + 12
			elif _key.clef == SOLFA_CLEF_BASS:
				tonic = shift + 5
		return tonic
	
	def _translate_to_chromatic_note(self, _note, _tonic):
		'''
		Converts a solfege note into a chromatic note.
		
		This function will accept a note such as "Do", "Re", "Mi" etc...
		and convert it to its equivalent on the chromatic scale ("C", "E", "F" etc...)
		The function will return a tuple containing the chromatic note and its
		tempo. For example:
		
		>> (cnote, tempo) = solfa_msg._translate_to_chromatic_note("d1")

		@param _note The solfege note to convert.
		@param _tonic The tone of the note.
		@return A tuple containing the chromatic note and its tempo.
		'''
		if _note[0] in SOLFA_NOTES:
			idx = (SOLFA_NOTES.index(_note[0])+1) % len(SOLFA_NOTES)
			return (SCALES[idx+_tonic], _note[1])
		else:
			raise Exception("Unknown note received: {n:s}".format(n=_note))
	
	def _translate_to_chromatic_notes(self, _notes, _tonic):
		'''
		
		'''
		notes = []
		for note in _notes:
			notes.append(self._translate_to_chromatic_note(note, _tonic))
		return notes
	
	def _bar_value(self, _unit, _time):
		if _unit == SOLFA_RHYTHM_SIXTEEN:
			return int(_time[0])
		elif _unit == SOLFA_RHYTHM_EIGHTH:
			if _time[0] == "2":
				return 1
			elif _time[0] == "3":
				return 100
			elif _time[0] == "4":
				return 2
		elif _unit == SOLFA_RHYTHM_QUARTER:
			return 1
		else:
			return 0
	
	def _to_abc_notation(self, _chromatic_notes_and_beats, _bar_value):

		notes_and_timings = []
		idx_note = 0
		bar = _bar_value
		dbt = 0
		cnt = bar
		nb_notes = len(_chromatic_notes_and_beats)
		#(cur_note, cur_beat) = notes_and_beats[0]
		
		while idx_note < nb_notes-1:
			(note, beat) = _chromatic_notes_and_beats[idx_note]
			idx_note += 1
			(next_note, next_beat) = _chromatic_notes_and_beats[idx_note]
			
			#print "[{idx:d}] (note, beat): ({nt:s}, {bt:d})".format(idx=idx_note, nt=note, bt=beat)
			#print "[{idx:d}] (next_note, next_beat): ({nt:s}, {bt:d})".format(idx=idx_note, nt=next_note, bt=next_beat)
			timing = -1
			if beat == 1:
				if next_beat == 1:
					timing = 4
					if dbt == 0:
						dbt = 1
						cnt = 2
					elif cnt == bar and bar < 100: cnt = 1
					else: cnt += 1
				else:
					timing = next_beat-1
					if dbt == 0: cnt = 1
					dbt = 1
				notes_and_timings.append((note, timing))
			elif beat == 2:
				if next_beat <= 2:
					timing = 3
					notes_and_timings.append((note, timing))
					if next_beat == 2:
						notes_and_timings.append((SOLFA_SL, 1))
					if dbt == 0 and bar == 100:
						cnt = 1
						dbt = 1
					elif cnt == bar and bar < 100: cnt = 1
					else: cnt += 1
				else:
					timing = beat - 2
					notes_and_timings.append((note, timing))
			elif beat == 3:
				if next_beat <= 3:
					timing = 2
					notes_and_timings.append((note, timing))
					if next_beat >= 2:
						notes_and_timings.append((SOLFA_SL, next_beat-1))
					if dbt == 0 and bar == 100:
						cnt = 1
						dbt = 1
					elif cnt == bar and bar < 100: cnt = 1
					else: cnt += 1
				elif next_beat == 4:
					timing = 1
					notes_and_timings.append((note, timing))
			elif beat == 4:
				timing = 1
				notes_and_timings.append((note, timing))
				if next_beat >= 2:
					notes_and_timings.append((SOLFA_SL, next_beat-1))
				if dbt == 0 and bar == 100:
					cnt = 1
					dbt = 1
				elif cnt == bar and bar < 100: cnt = 1
				else: cnt += 1
				
			#print "\t>(note, timing) = ({ln:s}, {tim:d})".format(ln=note, tim=timing)
	#		idx_note += 1
	#		last_note = note
	#		last_beat = beat
		return notes_and_timings
	
def test():
	test_abcde_treble_major_eight()
	test_hello_alto_minor_quarter()
	test_secret_bass_phrygian_sixteen_decoy_1()

def test_abcde_treble_major_eight():

	message = "ABCDE"
	solfa_matrix = SolfaMatrix()
	solfa_key = SolfaKey(
		_clef = SOLFA_CLEF_TREBLE, 
		_tonic = "C",
		_mode = SOLFA_MODE_MAJOR, 
		_rhythm = SOLFA_RHYTHM_EIGHTH)
	decoy_key = SolfaKey(
		_clef = SOLFA_UNDEFINED, 
		_tonic = SOLFA_UNDEFINED,
		_mode = SOLFA_UNDEFINED, 
		_rhythm = SOLFA_UNDEFINED)
	
	solfa_plain_msg = SolfaPlainMessage(message)
	solfa_cipher_msg = solfa_plain_msg.encrypt(solfa_key, decoy_key)
	ciphertext = str(solfa_cipher_msg)
	test_result = (ciphertext == "E3 A1 z2 D2 z2 G2 G4")
	
	print "[<] {pt:s}".format(pt=message)
	print "[>] {ct:s}".format(ct=ciphertext)
	print "[=] {rs:s}".format(rs=str(test_result))
	assert test_result

def test_hello_alto_minor_quarter():
	message = "HELLO"
	solfa_matrix = SolfaMatrix()
	solfa_key = SolfaKey(
		_clef = SOLFA_CLEF_ALTO, 
		_tonic = "E",
		_mode = SOLFA_MODE_MINOR, 
		_rhythm = SOLFA_RHYTHM_QUARTER)
	decoy_key = SolfaKey(
		_clef = SOLFA_UNDEFINED, 
		_tonic = SOLFA_UNDEFINED,
		_mode = SOLFA_UNDEFINED, 
		_rhythm = SOLFA_UNDEFINED)

	solfa_plain_msg = SolfaPlainMessage(message)
	solfa_cipher_msg = solfa_plain_msg.encrypt(solfa_key, decoy_key)
	ciphertext = str(solfa_cipher_msg)
	test_result = (ciphertext == "F2 A2 B2 z2 B2 C4")
	print "[<] {pt:s}".format(pt=message)
	print "[>] {ct:s}".format(ct=ciphertext)
	print "[=] {rs:s}".format(rs=str(test_result))
	assert test_result
	
def test_secret_bass_phrygian_sixteen_decoy_1():
	message = "Secret"
	solfa_matrix = SolfaMatrix()
	solfa_key = SolfaKey(
		_clef = SOLFA_CLEF_BASS, 
		_tonic = "A",
		_mode = SOLFA_MODE_PHRYGIAN, 
		_rhythm = SOLFA_RHYTHM_SIXTEEN)
	decoy_key = SolfaKey(
		_clef = SOLFA_CLEF_TREBLE, 
		_tonic = "D",
		_mode = SOLFA_MODE_MAJOR, 
		_rhythm = SOLFA_UNDEFINED)

	solfa_plain_msg = SolfaPlainMessage(message)
	solfa_cipher_msg = solfa_plain_msg.encrypt(solfa_key, decoy_key)
	ciphertext = str(solfa_cipher_msg)
	test_result = (ciphertext == "B4 c2 G2 z2 F2 c4 F4")
	print "[<] {pt:s}".format(pt=message)
	print "[>] {ct:s}".format(ct=ciphertext)
	print "[=] {rs:s}".format(rs=str(test_result))
	assert test_result

#////////////////////////////////////////////////////////////////////////////// 
# Main
#
def main(args):
	test()
	
if __name__ == "__main__": 
	main(parser.parse_args())	