Solfa
=====

Introduction
------------

The *solfa* program is an implementation of the Solfa cipher, which a symmetric encryption mechanism to transform plain text messages from a natural language into musical notation. The encrypted message can then be transfered via sound to the recipient, whom have been given the key to decrypt back the melody into the original message.

Usage
-----

```
usage:
solfa -m <message> [--decrypt]
        -kc [treble|alto|bass]
        -kt [C|C#|Db|D|Eb|E|F|F#|Gb|G|Ab|A|Bb|B]
        -km [major|minor|dorian|phrygian|lydian|mixolydian|locrian]
        -kr [1/4|1/8|1/16]

Encrypts and decrypts messages using the Solfa cipher.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Crypto Options:
  Options relating to the message

  -m MESSAGE, --msg MESSAGE
                        Specifies the message to decrypt or encrypt.
  -d, --decrypt         Tells the program to decrypt the provided message. If
                        not specified, the program will encrypt the provided
                        message by default.

Key Options:
  Options relating to the encryption key

  -kc {treble,alto,bass}, --clef {treble,alto,bass}
                        Specifies the clef of the encryption key.
  -kt {C,C#,Db,D,Eb,E,F,F#,Gb,G,Ab,A,Bb,B}, --tonic {C,C#,Db,D,Eb,E,F,F#,Gb,G,Ab,A,Bb,B}
                        Specifies the tonic of the key.
  -km {major,dorian,phrygian,lydian,mixolydian,minor,locrian}, --mode {major,dorian,phrygian,lydian,mixolydian,minor,locrian}
                        Specifies the mode of the encryption key.
  -kr {1/4,1/8,1/16}, --rhythm {1/4,1/8,1/16}
                        Specifies the rhythm of the key.

Decoy Key Options:
  Options relating to the decoy key

  -dc {treble,alto,bass,none}, --decoy-clef {treble,alto,bass,none}
                        Specifies the clef of the decoy key.
  -dt {C,C#,Db,D,Eb,E,F,F#,Gb,G,Ab,A,Bb,B,none}, --decoy-tonic {C,C#,Db,D,Eb,E,F,F#,Gb,G,Ab,A,Bb,B,none}
                        Specifies the tonic of the decoy key.
  -dm {major,dorian,phrygian,lydian,mixolydian,minor,locrian,none}, --decoy-mode {major,dorian,phrygian,lydian,mixolydian,minor,locrian,none}
                        Specifies the mode of the decoy key.
  -dr {1/4,1/8,1/16,none}, --decoy-rhythm {1/4,1/8,1/16,none}
                        Specifies the rhythm of the decoy key.

Program Options:
  Options relating to execution of the program

  --test                Initiates testing of the application.
  
 ```

Examples
--------

This section will present some examples on how to use the Solfa encryption/decryption script.

```
.\solfa.py -m "hello world" -kt A -km lydian -kc bass -kr 1/4
```

The typical example of the *solfa* program is to specify a message to encrypt using the `-m` or `--message` option and specifying key parameters using the `-kc`, `-kt`, `-km` and `-kr` options. In the example above, we are encrypting the plain text message "hello world" using a *A lydian* mode using a *bass* clef on a *quarter* (1/4) rhythm. Running this program will output the following result:

```
[K:none clef=none] [L:none] [M:4/4] A2 | c2 d2 | z2 d2 | E3 c1 | E2 F2 | z2 d2 | z2 c2 |
```

You can also include a decoy key, which will further obfuscate the resulting cipher text by shifting the tone of the melody based on the original encryption key. Consider the example below.

```
.\solfa.py -m 12345 -kt C -km major -kc treble -kr 1/8 -dt E -dm minor -dc alto
```

In the case aboce, we use an additional decoy in *C minor* on the *alto* key using the `-dt`, `-dm` and `-dc` parameters. You can also specify a decoy rhythm using the `-dr` parameter. 

Known Issues
------------

- Decryption is currently not working.
- Needs some cleanup: a lot of useless code.

Future Features
---------------

- Output into a MIDI file.
- Output into an image file.

References
----------

The Solfa Cipher, http://www.wmich.edu/mus-theo/solfa-cipher/, last visited on 10 Jun 17
