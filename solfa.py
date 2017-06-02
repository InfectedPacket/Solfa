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
SOLFA_DO = "d"
SOLFA_RE = "r"
SOLFA_MI = "m"
SOLFA_FA = "f"
SOLFA_SOL= "s"
SOLFA_LA = "l"
SOLFA_SI = "t"
SOLFA_SL = "z"
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

#////////////////////////////////////////////////////////////////////////////// 
# Code
#
class SolfaMatrix(object):

	def __init__(self, _matrix = ENGLISH_MATRIX):
		self.matrix = _matrix

	def __str__(self):
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
		for tone in self.matrix.keys():
			letters = self.matrix[tone]
			if _char in letters:
				return (tone,  letters.index(_char)+1)
		return ""
	
	def translate_string(self, _chars):
		cipher_chars = []
		for character in _chars:
			cipher_chars.append(self.translate_single_char(character))
		return cipher_chars
	
	def translate_single_note(self, _tone, _time):
		plain_char = ""
		index = int(_time) - 1
		if _tone in self.matrix.keys():
			if index >= 0 and index < len(self.matrix[SOLFA_DO]):
				plain_char = self.matrix[_tone][index]
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
		
	def __str__(self):
		if self.tonic != SOLFA_UNDEFINED:
			abc_format = "<Solfa Key [K:{tone:s} {mode:s} clef={clef:s}] [L:{rhythm:s}] [M:none]>"
			return abc_format.format(
				tone=self.tonic, 
				mode=self.mode,
				clef=self.clef,
				rhythm=self.rhythm_unit)
		else:
			abc_format = "<Solfa Key [K:{tone:s} clef={clef:s}] [L:{rhythm:s}] [M:none]>"
			return abc_format.format(
				tone=self.tonic,
				clef=self.clef,
				rhythm=self.rhythm_unit)	
	
def calculate_tonic(_key, _decoy_key):
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

def get_note(_note, _tonic):
	idx = (SOLFA_NOTES.index(_note[0])+1) % len(SOLFA_NOTES)
	return (SCALES[idx+_tonic], _note[1])	

def get_notes(_notes, _tonic):
	notes = []
	for note in _notes:
		notes.append(get_note(note, _tonic))
	return notes
	
def get_bar(_unit, _time):
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
	
def to_abc_notation(notes_and_beats, bar):

	notes_and_timings = []
	idx_note = 1
	dbt = 0
	nb_notes = len(notes_and_beats)
	(last_note, last_beat) = notes_and_beats[0]
	while idx_note < nb_notes:
		(note, beat) = notes_and_beats[idx_note]
		
		if last_beat == 1:
			if beat == 1:
				timing = 4
				if dbt == 0:
					dbt = 1
					cnt = 2
				elif cnt == bar and bar < 100: cnt = 1
				else: cnt += 1
			else:
				timing = beat-1
				if dbt == 0: cnt = 1
				dbt = 1
			notes_and_timings.append((last_note, timing))
		elif last_beat == 2:
			if beat <= 2:
				timing = 3
				notes_and_timings.append((last_note, timing))
				if beat == 2:
					notes_and_timings.append((SOLFA_SL, 1))
				if dbt == 0 and bar == 100:
					cnt = 1
					dbt = 1
				elif cnt == bar and bar < 100: cnt = 1
				else: cnt += 1
			else:
				timing = beat - 2
				notes_and_timings.append((last_note, timing))
		elif last_beat == 3:
			if beat <= 3:
				timing = 2
				notes_and_timings.append((last_note, timing))
				if beat >= 2:
					notes_and_timings.append((SOLFA_SL, beat-1))
				if dbt == 0 and bar == 100:
					cnt = 1
					dbt = 1
				elif cnt == bar and bar < 100: cnt = 1
				else: cnt += 1
			elif beat == 4:
				timing = 1
				notes_and_timings.append((last_note, timing))
		elif last_beat == 4:
			timing = 1
			notes_and_timings.append((last_note, timing))
			if beat >= 2:
				notes_and_timings.append((SOLFA_SL, beat-1))
			if dbt == 0 and bar == 100:
					cnt = 1
					dbt = 1
			elif cnt == bar and bar < 100: cnt = 1
			else: cnt += 1
				
		idx_note += 1
		last_note = note
		last_beat = beat
		
	return notes_and_timings
	
	
def test():
	message = "THEFIRSTHALFOFTHEFLAGISTHEWORDSUBDERMALCONCATENATEWITHTHESECONDHALFTOOBTAINACOMPLETEFLAGGLORYTORAO"
	tune = "d1 m3 s1 d4 r1 d3 f1 d1 m3 m1 l3 d4 t1 d4 d1 m3 s1 d4 z1 l3 m1 m4 r1 f1 d1 m3 s1 s4 t1 d3 z1 s3 f1 t3 l4 z1 s3 s1 d3 z1 f3 m1 l3 r3 t1 l1 r3 m1 d1 s1 l1 m1 d1 s1 s4 r1 d1 m3 d1 m3 s1 f1 s1 r3 t1 l1 s3 z1 m3 m1 l3 d4 d1 t1 t1 l4 d1 m1 r1 l1 m1 r3 t1 f3 f4 z1 l3 s1 d1 s1 d4 z1 l3 m1 m4 m4 z1 l3 t1 d3 r4 d1 t1 d3 m1 t1"
	
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
	tonic = calculate_tonic(solfa_key, decoy_key)
	
	plaintext = solfa_matrix.translate_multiple_notes(tune.split(" "))
	translated_notes = solfa_matrix.translate_string(message)
	notes_and_beats = get_notes(translated_notes, tonic)
	
	bar = get_bar(SOLFA_RHYTHM_EIGHTH, "4/4")

		
	ciphertext = to_abc_notation(notes_and_beats, bar)
	matrix_str = str(solfa_matrix)
	key = str(solfa_key)
	dkey = str(decoy_key)
	print "[=] Using the following matrix:"
	print matrix_str
	
	print "[=] Solfa Key: " + key
	print "[=] Decoy Key: " + dkey
	print "[=] Tonic: " + str(tonic)
	
	print "[=] Plaintext : " + plaintext
	print "[=] Ciphertext: " + ' '.join(
		["{n:s}{t:d}".format(n=note, t=time) for (note, time) in ciphertext])
	
#////////////////////////////////////////////////////////////////////////////// 
# Main
#
def main(args):
	test()
	
if __name__ == "__main__": 
	main(parser.parse_args())	