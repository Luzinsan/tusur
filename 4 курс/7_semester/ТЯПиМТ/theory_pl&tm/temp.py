import re

# (\s*
#   (?:(?P<type>float|int) |
#    (?P<id>[a-zA-Z_]\w*
#     (?P<op>\[\s*
#     (?:(?:[a-zA-Z_]\w*\[\d+\]|\d+)
#      (?:\s*,\s*(?:[a-zA-Z_]\w*\[\d+\]|\d+))*)
#     \s*\])?
#    )
#   \s*[,;])
# \s*)


input_string = ' float   b2 , sint , int_[sdf[3], ds[2]], int7  ; '
types = '|'.join(['int', 'double', 'float'])
pattern = re.compile(f"(\s*(?:(?P<type>{types})\\b|(?P<id>[a-zA-Z_]\w*(?P<op>\[\s*(?:(?:[a-zA-Z_]\w*\[\d+\]|\d+)(?:\s*,\s*(?:[a-zA-Z_]\w*\[\d+\]|\d+))*)\s*\])?)\s*[,;])\s*)")

if ''.join([match[0] for match in re.findall(pattern, input_string)]) != input_string:
    iterator = re.finditer(pattern, input_string)
    desired_type = next(iterator)
    index = desired_type.end()

    if desired_type['type'] not in types:
        raise TypeError(f"Invalid type on the row={1}; column={desired_type.start()}")
    for match in iterator:
        print(f"index in orig string: {index}\trest_str={input_string[index:]}")
        if not match['id']:
            raise KeyError("Using a reserved name in an identifier\n"
                           f" on the row={1}; column={match.start()}")
        print(f"index of match: {match.start()}\tmatch={match['id']}\n")
        if index != match.start():
            raise KeyError(f"Invalid id on the row={1}; column={index}\nmatch={match['id']}\trest_str={input_string[index:]}")
        else:
            index = match.end()
    if index != len(input_string)-1:
        raise SyntaxError("Reference to an unresolved external character\n"
                          f"on the row={1}; column={len(input_string)}")
