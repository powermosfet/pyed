import ure 

class Edit():
    def __init__(self, edit, begin = 0, end = -1):
        if isinstance(edit, Edit):
            self.parent = edit
            self.filename = edit.filename
        else:
            self.filename = edit
            self.lines = open(self.filename).read().split('\n')
            self.parent = None
        self.begin = begin
        self.end = end
        self.tabstop = 4

    def __str__(self):
        return '\n'.join(prefix_number(self.get_lines())[self.begin:self.end])

    def __repr__(self):
        return str(self)

    def __getitem__(self, index):
        if isinstance(index, slice):
            (begin, end, step) = index.indices(len(self.get_lines()))
            return Edit(self, begin, end)
        else:
            return Edit(self, index, index + 1)

    def get_lines(self):
        if self.parent:
            return self.parent.get_lines()
        else:
            return self.lines

    def set_lines(self, lines):
        if self.parent:
            self.parent.set_lines(lines)
        else:
            self.lines = lines

    def insert(self, stuff):
        if isinstance(stuff, list):
            for line in stuff[::-1]:
                self.insert(line)
        else:
            before = self.get_lines()[:self.begin]
            after = self.get_lines()[self.begin:]
            self.set_lines(before + [ stuff ] + after)
        return self

    def delete(self):
        before = self.get_lines()[:self.begin]
        after = self.get_lines()[self.end:]
        self.set_lines(before + after)
        return self

    def move(self, new_begin):
        lines = self.get_lines()[self.begin:self.end]
        return self.delete()[new_begin].insert(lines)


    def indent(self, amount=1):
        before = self.get_lines()[:self.begin]
        lines = self.get_lines()[self.begin:self.end]
        after = self.get_lines()[self.end:]
        lines = [ indent_line(amount * self.tabstop, line) for line in lines ]
        self.set_lines(before + lines + after)
        return self

    def sub(self, pattern, replacement):
        before = self.get_lines()[:self.begin]
        lines = self.get_lines()[self.begin:self.end]
        after = self.get_lines()[self.end:]
        lines = [ ure.sub(pattern, replacement, line) for line in lines ]
        self.set_lines(before + lines + after)
        return self

    def save(self):
        f = open(self.filename, 'w')
        return f.write('\n'.join(self.get_lines()))

def prefix_number(lines):
    return [ line_number(i) + line for i, line in enumerate(lines) ]

def line_number(n):
    return ('   ' + str(n) + ': ')[-5:]

def indent_line(amount, line):
    spaces = abs(amount)
    if amount > 0:
        return ''.join(' ' for x in range(spaces)) + line
    else:
        return line[spaces:]
