
class Table():
    def __init__(self):
        self.field_names = []
        self.rows = []

    def add_row(self,row):
        self.rows.append(row)

    def __str__(self):
        final = ''

        sep = "+"
        field_line = ""
        field_length = []
        for i in range(len(self.field_names)):
            max = len(self.field_names[i])
            for r in [row[i] for row in self.rows]:
                if len(r) > max:
                    max = len(r)
            field_length.append(max+2)
        for length,field in zip(field_length,self.field_names):
            sep += '-'*(length)+'+'
            size = length - len(str(field))
            spacing1 = size//2
            spacing2 = spacing1+1 if size%2==1 else spacing1
            field_line += '|' + ' '*spacing1 + str(field) + ' '*spacing2
        field_line += '|\n'
        sep += '\n'

        final += sep + field_line + sep

        for row in self.rows:
            row_line = ''
            for i,(length,field) in enumerate(zip(field_length,self.field_names)):
                size = length - len(str(row[i]))
                spacing1 = size//2
                spacing2 = spacing1+1 if size%2==1 else spacing1
                row_line += '|'+' '*spacing1 + str(row[i]) + ' '*spacing2
            row_line += '|'
            final += row_line +'\n'

        final += sep
        return final
