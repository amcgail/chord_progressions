class note_set:

    def __init__(self, notes):
        self.notes = sorted(notes)
        self.mod_notes = set([x % 12 for x in notes])

    def __eq__(self, other):
        return self.notes == other.notes

    def issamechord(self, other):
        """
        #too strict...
        self_move_notes = [x - self.notes[0] for x in self.notes]
        other_move_notes = [x - other.notes[0] for x in other.notes]

        return (self_move_notes == other_move_notes) and (self.notes[0]%12 == other.notes[0]%12)
        """
        return self.mod_notes == other.mod_notes and (self.notes[0] % 12 == other.notes[0] % 12)

    def subsumes(self, other):
        # return self.mod_notes.issuperset( other.mod_notes ) and (self.notes[0]%12 == other.notes[0]%12)
        return self.mod_notes.issuperset(other.mod_notes)


MIDDLE_C = 0
C_chords = [
    ("C maj", [0, 4, 7]),
    ("C min", [0, 3, 7]),
    ("C aug", [0, 4, 8]),
    ("C dim", [0, 3, 6]),
    ("C min 6", [0, 3, 7, 9]),
    ("C maj 6", [0, 4, 7, 9]),
    ("Csus4", [0, 5, 7]),
    ("C7 sus4", [0, 5, 7, 10]),

    ("C halfdim 7", [0, 3, 6, 10]),
    ("C7", [0, 4, 7, 10]),
    ("Cmaj7", [0, 4, 7, 11]),
    ("Cmin7", [0, 3, 7, 10]),
    ("Cdim7", [0, 3, 6, 9]),
    ("C7 #5", [0, 4, 8, 10]),
    ("C7 b5", [0, 4, 5, 10]),
    ("Cmaj7 b3", [0, 3, 7, 11]),
    ("Cmin7 #5", [0, 3, 6, 10]),
    ("C7 sus4", [0, 5, 7, 10]),

    ("C 9", [0, 4, 7, 10, 14]),
    ("C min 9", [0, 3, 7, 10, 14]),
    ("C maj 9", [0, 4, 7, 11, 14]),
    ("C 9 #5", [0, 4, 8, 10, 14]),
    ("C 9 b5", [0, 4, 6, 10, 14]),
    ("C 7 #9", [0, 4, 7, 10, 15]),
    ("C 7 b9", [0, 4, 7, 10, 13]),
    ("C6 add 9", [0, 4, 7, 9, 14]),

    ("C 11", [0, 4, 7, 10, 14, 17]),
    ("C #11", [0, 4, 7, 10, 14, 18]),

    ("C 13", [0, 4, 7, 10, 14, 17, 21]),
    ("C 13 b9", [0, 4, 7, 10, 13, 17, 21]),
    ("C 13 b9 b5", [0, 4, 6, 10, 13, 17, 21]),
]


def new_letter(letter, offset):
    return [
        (name.replace("C", letter), [note + offset for note in notes])
        for (name, notes) in C_chords
    ]


def notes2chordName(notes):
    names = []

    ns = note_set(notes)
    for name, ns_match in chords:
        if ns_match.issamechord(ns):
            names.append(name)

    return names


def chordName2chord(name):
    for name_match, ns in chords:
        if name == name_match:
            return ns
    raise Exception("Can't find %s" % name)


chords = list(C_chords)

chords += new_letter("D", 2)
chords += new_letter("E", 4)
chords += new_letter("F", 5)
chords += new_letter("G", 7)
chords += new_letter("A", 9)
chords += new_letter("B", 11)

chords += new_letter("Cb", -1)
chords += new_letter("Db", 1)
chords += new_letter("Eb", 3)
chords += new_letter("Fb", 4)
chords += new_letter("Gb", 6)
chords += new_letter("Ab", 8)
chords += new_letter("Bb", 10)

chords += new_letter("C#", 1)
chords += new_letter("D#", 3)
chords += new_letter("E#", 5)
chords += new_letter("F#", 6)
chords += new_letter("G#", 8)
chords += new_letter("A#", 10)
chords += new_letter("B#", 0)

chords = [
    (name, note_set(notes))
    for (name, notes) in chords
]


