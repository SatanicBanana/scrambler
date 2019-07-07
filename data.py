class Colour:
    def __init__(self, r, g=None, b=None):
        if g is None:
            self.r = r[0]
            self.g = r[1]
            self.b = r[2]
        else:
            self.r = r
            self.g = g
            self.b = b

        self.colour_tuple = (self.r, self.g, self.b)

    def __eq__(self, other):
        return all(self.colour_tuple[i] == other.colour_tuple[i] for i in range(2))


class FlagInfo:
    def __init__(self, name, segments):
        self.name = name
        self.segments = segments


class FlagSegment:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour


burger_list = {
    "ham": 24,
    "b": 14,
    "u": 4,
    "r": 15,
    "ger": 18
}


flag_list = (
    FlagInfo("Belgium",
             (
                 FlagSegment("bel", Colour(0, 0, 0)),
                 FlagSegment("gi", Colour(250, 224, 66)),
                 FlagSegment("um", Colour(237, 41, 57))
             )
             ),

    FlagInfo("France",
             (
                 FlagSegment("fr", Colour(0, 35, 149)),
                 FlagSegment("an", Colour(255, 255, 255)),
                 FlagSegment("ce", Colour(237, 41, 57))
             )
             ),

    FlagInfo("Ireland",
             (
                 FlagSegment("ire", Colour(22, 155, 98)),
                 FlagSegment("lan", Colour(255, 255, 255)),
                 FlagSegment("d", Colour(255, 136, 62))
             )
             ),

    FlagInfo("Italy",
             (
                 FlagSegment("it", Colour(0, 146, 70)),
                 FlagSegment("a", Colour(255, 255, 255)),
                 FlagSegment("ly", Colour(206, 43, 55))
             )
             ),

    FlagInfo("Romania",
             (
                 FlagSegment("rom", Colour(0, 43, 127)),
                 FlagSegment("an", Colour(252, 209, 22)),
                 FlagSegment("ia", Colour(206, 17, 38))
             )
             ),
)

whites = []
for flag in flag_list:
    for segment in flag.segments:
        if segment.colour == Colour(255, 255, 255):
            whites.append(segment)
