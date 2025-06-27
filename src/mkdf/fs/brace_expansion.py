
def brace_expand(pattern: str) -> list[str]:
    """
    Correctly expand brace patterns, including nested and multiple groups.
    'myproject/{src,docs,tests}' should return:
    ['myproject/docs', 'myproject/src', 'myproject/tests']
    """
    if '{' not in pattern:
        return [pattern]

    # Find the first opening brace
    i = pattern.find('{')
    prefix = pattern[:i]
    
    # Find the matching closing brace, handling nested braces
    j = -1
    brace_level = 0
    for k in range(i + 1, len(pattern)):
        if pattern[k] == '{':
            brace_level += 1
        elif pattern[k] == '}':
            if brace_level == 0:
                j = k
                break
            else:
                brace_level -= 1
    
    if j == -1: # No matching closing brace
        return [pattern]

    middle = pattern[i+1:j]
    suffix = pattern[j+1:]

    # Split the middle part by commas, but only at the top level
    options = []
    part = ""
    inner_brace_level = 0
    for char in middle:
        if char == '{':
            inner_brace_level += 1
        elif char == '}':
            inner_brace_level -= 1
        elif char == ',' and inner_brace_level == 0:
            options.append(part)
            part = ""
            continue
        part += char
    options.append(part)

    results = []
    # Recursively expand the suffix first
    expanded_suffix = brace_expand(suffix)
    
    for option in options:
        # Recursively expand each option
        expanded_option = brace_expand(option)
        for o in expanded_option:
            for s in expanded_suffix:
                results.append(prefix + o + s)

    return sorted(list(set(results)))