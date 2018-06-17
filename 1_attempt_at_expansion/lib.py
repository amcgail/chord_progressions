MIDDLE_C = 0

class chord_sequence:
    def __init__(self, starting_chords = []):
        self.chords = starting_chords

    def add(self, c):
        self.chords.append(c)

    def distance(self, other):
        if len(other.chords) != len(self.chords):
            return float("inf")

        d = 0
        for i, oc in enumerate(other.chords):
            assert(isinstance(oc, chord))
            d += oc.distance( self.chords[i] )

        return d

    def relative_distance(self, other):
        if len(other.chords) != len(self.chords):
            return float("inf")
        if len(other.chords) == 0:
            return True

        transpose_amt = other.chords[0].root_note - self.chords[0].root_note

        for i, oc in enumerate(other.chords):
            assert(isinstance(oc, chord))
            assert (isinstance(self.chords[i], chord))
            print( oc, self.chords[i] )
            print(list(oc.permissible_notes.notes_mod_octave), list(self.chords[i].transpose(transpose_amt).permissible_notes.notes_mod_octave))

            if not self.chords[i].transpose(transpose_amt).isequivalentto( oc ):
                return float("inf")

        return 0

    def __repr__(self):
        return "[%s]" % ", ".join( x.__repr__() for x in self.chords )

class chord:
    def __init__(self, necessary_notes, permissible_notes, root_note, name):
        self.name = name

        self.root_note = root_note
        self.necessary_notes = note_set(necessary_notes, root_note=root_note)
        self.permissible_notes = note_set(permissible_notes, root_note=root_note)

    def transpose(self, offset, new_name="unnamed"):
        new_rn = self.root_note + offset

        return chord(
            necessary_notes = self.necessary_notes.transpose( offset ),
            permissible_notes = self.permissible_notes.transpose( offset ),
            root_note=new_rn,
            name=new_name
        )

    def isequivalentto(self, other):
        assert(isinstance(other, chord))

        return [ self.necessary_notes.notes_mod_octave, self.permissible_notes.notes_mod_octave, self.root_note%12 ] \
            == [ other.necessary_notes.notes_mod_octave, other.permissible_notes.notes_mod_octave, other.root_note%12 ]

    def istransposeof(self, other):
        if self.necessary_notes.transpose( -self.root_note ) == other.necessary_notes.transpose( -other.root_note ) and \
            self.permissible_notes.transpose(-self.root_note) == other.permissible_notes.transpose(-other.root_note):
            return True

        return False

    def distance(self, other):

        if self.isequivalentto(other):
            return 0

        return float("inf")

        """
        # if it subsumes, we'll say there's no distance...
        if self.necessary_notes.subsumes( other.necessary_notes ) and \
            self.permissible_notes.subsumes( other.permissible_notes ):

            return 0

        if other.necessary_notes.subsumes(self.necessary_notes) and \
            other.permissible_notes.subsumes(self.permissible_notes):

            return 0

        return float("inf")
        """

    def __repr__(self):
        return "%s" % self.name
    def __str__(self):
        return self.__repr__()


class mod_note_set:
    def __init__(self, notes):
        self.mod_notes = set([x % 12 for x in notes])

    def __eq__(self, other):
        return self.mod_notes == other.mod_notes

    def issuperset(self, other):
        return self.mod_notes.issuperset( other.mod_notes )

class note_set:
    def __init__(self, notes, root_note = MIDDLE_C):
        self.root_note = root_note

        self.notes = sorted(notes)

        self.notes_mod_octave = set([x % 12 for x in notes])
        self.notes_mod_key = set([(x-root_note) for x in notes])
        self.notes_mod_octave_key = set([(x - root_note) % 12 for x in notes])

    def __eq__(self, other):
        assert( isinstance(other, note_set) )
        return self.notes == other.notes

    def transpose(self, offset):
        return note_set(
            notes = [ (x + offset) for x in list(self.notes) ],
            root_note = self.root_note + offset
        )

    def issamechord(self, other):
        assert( isinstance(other, note_set) )

        """
        #too strict...
        self_move_notes = [x - self.notes[0] for x in self.notes]
        other_move_notes = [x - other.notes[0] for x in other.notes]

        return (self_move_notes == other_move_notes) and (self.notes[0]%12 == other.notes[0]%12)
        """
        return self.notes_mod_octave == other.notes_mod_octave and (self.notes[0] % 12 == other.notes[0] % 12)

    def subsumes(self, other):
        assert( isinstance(other, note_set) )

        # return self.mod_notes.issuperset( other.mod_notes ) and (self.notes[0]%12 == other.notes[0]%12)
        return self.notes_mod_octave.issuperset(other.notes_mod_octave)

    def __iter__(self):
        return iter(self.notes)

# C_chords = [
#     ("C maj", [0, 4, 7]),
#     ("C min", [0, 3, 7]),
#     ("C aug", [0, 4, 8]),
#     ("C dim", [0, 3, 6]),
#     ("C min 6", [0, 3, 7, 9]),
#     ("C maj 6", [0, 4, 7, 9]),
#     ("Csus4", [0, 5, 7]),
#     ("C7 sus4", [0, 5, 7, 10]),
#
#     ("C halfdim 7", [0, 3, 6, 10]),
#     ("C7", [0, 4, 7, 10]),
#     ("Cmaj7", [0, 4, 7, 11]),
#     ("Cmin7", [0, 3, 7, 10]),
#     ("Cdim7", [0, 3, 6, 9]),
#     ("C7 #5", [0, 4, 8, 10]),
#     ("C7 b5", [0, 4, 5, 10]),
#     ("Cmaj7 b3", [0, 3, 7, 11]),
#     ("Cmin7 #5", [0, 3, 6, 10]),
#     ("C7 sus4", [0, 5, 7, 10]),
#
#     ("C 9", [0, 4, 7, 10, 14]),
#     ("C min 9", [0, 3, 7, 10, 14]),
#     ("C maj 9", [0, 4, 7, 11, 14]),
#     ("C 9 #5", [0, 4, 8, 10, 14]),
#     ("C 9 b5", [0, 4, 6, 10, 14]),
#     ("C 7 #9", [0, 4, 7, 10, 15]),
#     ("C 7 b9", [0, 4, 7, 10, 13]),
#     ("C6 add 9", [0, 4, 7, 9, 14]),
#
#     ("C 11", [0, 4, 7, 10, 14, 17]),
#     ("C #11", [0, 4, 7, 10, 14, 18]),
#
#     ("C 13", [0, 4, 7, 10, 14, 17, 21]),
#     ("C 13 b9", [0, 4, 7, 10, 13, 17, 21]),
#     ("C 13 b9 b5", [0, 4, 6, 10, 13, 17, 21]),
# ]

C_chords = [
        chord(
                necessary_notes = [0, 4, 7],
                permissible_notes = [0, 4, 7],
                root_note = 0,
                name = "C maj"
        ),
        chord(
                necessary_notes = [0, 3, 7],
                permissible_notes = [0, 3, 7],
                root_note = 0,
                name = "C min"
        ),
        chord(
                necessary_notes = [0, 4, 8],
                permissible_notes = [0, 4, 8],
                root_note = 0,
                name = "C aug"
        ),
        chord(
                necessary_notes = [0, 3, 6],
                permissible_notes = [0, 3, 6],
                root_note = 0,
                name = "C dim"
        ),
        chord(
                necessary_notes = [0, 3, 7, 9],
                permissible_notes = [0, 3, 7, 9],
                root_note = 0,
                name = "C min 6"
        ),
        chord(
                necessary_notes = [0, 4, 7, 9],
                permissible_notes = [0, 4, 7, 9],
                root_note = 0,
                name = "C maj 6"
        ),
        chord(
                necessary_notes = [0, 5, 7],
                permissible_notes = [0, 5, 7],
                root_note = 0,
                name = "Csus4"
        ),
        chord(
                necessary_notes = [0, 5, 7, 10],
                permissible_notes = [0, 5, 7, 10],
                root_note = 0,
                name = "C7 sus4"
        ),

        chord(
                necessary_notes = [0, 3, 6, 10],
                permissible_notes = [0, 3, 6, 10],
                root_note = 0,
                name = "C halfdim 7"
        ),
        chord(
                necessary_notes = [0, 4, 7, 10],
                permissible_notes = [0, 4, 7, 10],
                root_note = 0,
                name = "C7"
        ),
        chord(
                necessary_notes = [0, 4, 7, 11],
                permissible_notes = [0, 4, 7, 11],
                root_note = 0,
                name = "Cmaj7"
        ),
        chord(
                necessary_notes = [0, 3, 7, 10],
                permissible_notes = [0, 3, 7, 10],
                root_note = 0,
                name = "Cmin7"
        ),
        chord(
                necessary_notes = [0, 3, 6, 9],
                permissible_notes = [0, 3, 6, 9],
                root_note = 0,
                name = "Cdim7"
        ),
        chord(
                necessary_notes = [0, 4, 8, 10],
                permissible_notes = [0, 4, 8, 10],
                root_note = 0,
                name = "C7 #5"
        ),
        chord(
                necessary_notes = [0, 4, 5, 10],
                permissible_notes = [0, 4, 5, 10],
                root_note = 0,
                name = "C7 b5"
        ),
        chord(
                necessary_notes = [0, 3, 7, 11],
                permissible_notes = [0, 3, 7, 11],
                root_note = 0,
                name = "Cmaj7 b3"
        ),
        chord(
                necessary_notes = [0, 3, 6, 10],
                permissible_notes = [0, 3, 6, 10],
                root_note = 0,
                name = "Cmin7 #5"
        ),
        chord(
                necessary_notes = [0, 5, 7, 10],
                permissible_notes = [0, 5, 7, 10],
                root_note = 0,
                name = "C7 sus4"
        ),

        chord(
                necessary_notes = [0, 4, 7, 10, 14],
                permissible_notes = [0, 4, 7, 10, 14],
                root_note = 0,
                name = "C 9"
        ),
        chord(
                necessary_notes = [0, 3, 7, 10, 14],
                permissible_notes = [0, 3, 7, 10, 14],
                root_note = 0,
                name = "C min 9"
        ),
        chord(
                necessary_notes = [0, 4, 7, 11, 14],
                permissible_notes = [0, 4, 7, 11, 14],
                root_note = 0,
                name = "C maj 9"
        ),
        chord(
                necessary_notes = [0, 4, 8, 10, 14],
                permissible_notes = [0, 4, 8, 10, 14],
                root_note = 0,
                name = "C 9 #5"
        ),
        chord(
                necessary_notes = [0, 4, 6, 10, 14],
                permissible_notes = [0, 4, 6, 10, 14],
                root_note = 0,
                name = "C 9 b5"
        ),
        chord(
                necessary_notes = [0, 4, 7, 10, 15],
                permissible_notes = [0, 4, 7, 10, 15],
                root_note = 0,
                name = "C 7 #9"
        ),
        chord(
                necessary_notes = [0, 4, 7, 10, 13],
                permissible_notes = [0, 4, 7, 10, 13],
                root_note = 0,
                name = "C 7 b9"
        ),
        chord(
                necessary_notes = [0, 4, 7, 9, 14],
                permissible_notes = [0, 4, 7, 9, 14],
                root_note = 0,
                name = "C6 add 9"
        ),

        chord(
                necessary_notes = [0, 4, 7, 10, 14, 17],
                permissible_notes = [0, 4, 7, 10, 14, 17],
                root_note = 0,
                name = "C 11"
        ),
        chord(
                necessary_notes = [0, 4, 7, 10, 14, 18],
                permissible_notes = [0, 4, 7, 10, 14, 18],
                root_note = 0,
                name = "C #11"
        ),

        chord(
                necessary_notes = [0, 4, 7, 10, 14, 17, 21],
                permissible_notes = [0, 4, 7, 10, 14, 17, 21],
                root_note = 0,
                name = "C 13"
        ),
        chord(
                necessary_notes = [0, 4, 7, 10, 13, 17, 21],
                permissible_notes = [0, 4, 7, 10, 13, 17, 21],
                root_note = 0,
                name = "C 13 b9"
        ),
        chord(
                necessary_notes = [0, 4, 6, 10, 13, 17, 21],
                permissible_notes = [0, 4, 6, 10, 13, 17, 21],
                root_note = 0,
                name = "C 13 b9 b5"
        )
]



def new_letter(letter, offset):
    new_cs = []
    for c in C_chords:
        new_cs.append( c.transpose(
            offset=offset,
            new_name=c.name.replace("C", letter)
        ) )
    return new_cs


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

cname = {}

for c in chords:
    cname[ c.name] = c

print cname["G#maj7"].isequivalentto(cname["Abmaj7"])
a = chord_sequence([
    cname["C maj"],
    cname["F maj"],
    cname["G maj"],
])

b = chord_sequence([
    cname["F maj"],
    cname["Bb maj"],
    cname["C maj"]
])

print a.relative_distance(b)
print a
print str(b)