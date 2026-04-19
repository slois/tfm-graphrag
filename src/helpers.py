def insert_substring(source, insert, position):
    return source[:position] + " " + insert + source[position:]

def replace_substrings(text, replacements, insert_formatter):
    for rep in replacements:
        nchar = len(rep['mention'])
        pos = 0
        while pos >=0:
            print(pos)
            pos = text.find(rep['mention'], pos+nchar)
            if pos > 0:
                text = insert_substring(text, insert_formatter(rep), pos + nchar)
    return text