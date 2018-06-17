"""

This file is amazing.
Currently it recognizes chords from MIDI input to the laptop,
and keeps track of transitions.

Then when you start a pattern, it suggests the next chord. From memory.

All I need to do is program a Markov-type memory, where it matters the whole sequence of chords beforehand :).

"""

from random import sample
import sys
import time
import numpy as np
import midi
import midi.sequencer as sequencer
from collections import Counter

from pymongo import MongoClient
db = MongoClient()["chord_recognizer"]

from lib import notes2chordName, chordName2chord

if len(sys.argv) != 3:
    print "Usage: {0} <client> <port>".format(sys.argv[0])
    exit(2)

client = sys.argv[1]
port = sys.argv[2]

midi_sequencer = sequencer.SequencerRead(sequencer_resolution=120)
midi_sequencer.subscribe_port(client, port)
midi_sequencer.start_sequencer()

"""
def flat( chord ):

def ():

= [ chr(x) for x in range(ord("A"),ord("H")) ]
+= [ x+"#" for x in chordNames ]
+= [ x+"#" for x in chordNames ]
"""

last_notes_pressed = []

last_time_played = None
transition_counter = Counter()

last_chords = []

debug = False

while True:
    time.sleep(0.01)

    event = midi_sequencer.event_read()
    if event is not None:
        if not isinstance(event, midi.NoteOnEvent):
            continue

        last_time_played = time.time()

        if debug:
            print event

        notePressed = event.data[0]
        now = event.tick

        last_notes_pressed.append((notePressed, now))

        # deletes notes that aren't recent, in terms of ticks

        last_notes_pressed = [x for x in last_notes_pressed if x[1] > now - 10]
        if debug:
            print last_notes_pressed

        if len(last_notes_pressed) < 3:
            continue

    # if it's been a sec since you played a note...
    if len(last_notes_pressed) and (1 > time.time() - last_time_played > 0.05):

        # extracts note numbers
        give_em = [note for (note, tick) in last_notes_pressed]

        # check from 20 notes ago to just now, see if anything matches...
        chordsToCheck = [
            give_em[x:]
            for x in range(-20, -2)
        ]

        matched = []
        for chord in chordsToCheck:
            matched = notes2chordName(chord)
            if matched != []:
                break

        """
        matched = notes2chordName( give_em )
        """

        if matched == []:
            # print("Chord not recognized...")
            continue

        matched = matched[0]

        if len(last_chords) == 0 or not chordName2chord(last_chords[-1]).subsumes(chordName2chord(matched)):

            last_chords.append(matched)

            # record this observation...

            min_markov_vision = 2
            max_markov_vision = 10
            my_markov_vision = min(max_markov_vision, len(last_chords))

            for i in range(min_markov_vision, my_markov_vision):
                # the sequence is the last `i` chords
                seq = last_chords[-i:]

                # and we insert what led up to the last chord
                db["next_decisions_played"].insert({
                    "prev": seq[:-1], # everything except last element
                    "next": seq[-1] # last element
                })


            # now predict what's gonna be next...

            decision_counter = Counter()

            for i in range(min_markov_vision, my_markov_vision):
                # the sequence is the last `i` chords
                seq = last_chords[-i:]

                been_here_before = db["next_decisions_played"].find({
                    "prev": seq  # everything
                })
                decision_counter += Counter({
                    x['next']: len(x['prev']) # weight observations by length
                    for x in been_here_before
                })

            # predict = list(filter(lambda x: x[1] > 2, predict))
            # predict = list(sorted(predict, key=lambda x: -x[1]))

            if not len(decision_counter):
                print "%s" % matched
            else:

                max_suggestions = 2
                num_suggestions = min(max_suggestions, len(decision_counter))

                probabilities = np.log( decision_counter.values() )
                probabilities = probabilities / np.sum(probabilities)

                suggestions = np.random.choice(
                    decision_counter.keys(),
                    size=num_suggestions,
                    replace=False,
                    p=probabilities
                )

                pstring = " OR ".join( suggestions )
                print "I hear '%s'. P" \
                      "" \
                      "lay %s" % (matched, pstring)