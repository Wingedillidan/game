import tools


class Controller(object):

    def _parse(self, input):
        """Takes the ui frame string and returns a list of variables used
        within the strings"""
        result = []
        count = 0

        while True:
            start = input.find('{', count)
            count += start - count

            # this accounts for possible format modifiers with ':'
            end2 = input.find(':', count)
            end = input.find('}', count)

            # terminates if there's no more
            if end == -1 or start == -1:
                break
            else:
                count += (end - start)

            # if a ':' was found, use it's position instead of '}'
            if end2 < end and not end2 == -1:
                end = end2

            result.append(input[start+1:end])

        return result

    def _mkdict(self):
        """Takes the list generated by _parse and creates a dictionary that
        fills in attributes from the player object or leaves a blank string
        if the variables don't match anything in player.contents"""
        # TO DO: This needs to be constantly run to update with the play object
        # needs to pass by reference somehow :/
        # Temp fix? Constant call whenever display() is needed
        result = {}
        fill = None

        for item in self.fstrings:
            fill = self.player.contents.get(item)

            if fill is None:
                fill = ""

            result[item] = fill

        self.fill = result

    def load(self):
        """Loads in the ui frame file, creates the dictionary, and prepares the UI for
        display formatting."""
        f = open(self.file, 'r')

        for l in f.readlines():
            self.frame += l

            for entry in self._parse(l):
                self.fstrings.append(entry)

        f.close()

        self._mkdict()

    def display(self, text, len=75, clear=50):
        """Takes a given prompt and fills the ui lines for proper printing."""
        # TO DO: Fix hardcoded numbers
        # This has to update player stats by rereading the whole dictionary
        # every time :/
        self._mkdict()
        tools.clear(clear)
        count = 1; find = 0; cont = False
        working = text

        while working:

            # find a line break (if any) including up to the very possible end,
            # hence the +1 anything beyond is certain to be a part of the next
            # line
            if '\n' in working[:len+1]:
                find = working.find('\n')
            else:
                find = len

            fillkey = 'line' + str(count)

            # set the line# with the string that should be under the max
            # character limit
            if self.fill.get(fillkey) == "":
                self.fill[fillkey] = working[:find]
            else:
                # if there is more text than available lines, we need
                # another box
                cont = True
                break

            # QUESTION, when break is called, it still removes the last
            # used statement, HOW?
            working = working[find:].lstrip('\n')
            count += 1

        print self.frame.format(**self.fill)

        if cont:
            tools.next()
            self.display(working)

    def __init__(self, player, file='ui.txt'):
        self.player = player
        self.file = file
        self.fill = {}
        self.frame = ""
        self.fstrings = []

        self.load()
