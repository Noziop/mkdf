def _expand_range(s: str) -> list[str]:
    """Expands a range like '1..3' or 'a..c'."""
    if '..' not in s:
        return [s]

    parts = s.split('..')
    if len(parts) != 2:
        return [s] # Not a valid range format

    start_str, end_str = parts

    # Numeric range
    if start_str.isdigit() and end_str.isdigit():
        start = int(start_str)
        end = int(end_str)
        if start <= end:
            return [str(i) for i in range(start, end + 1)]
        else:
            return [str(i) for i in range(start, end - 1, -1)]
    # Character range
    elif len(start_str) == 1 and len(end_str) == 1 and start_str.isalpha() and end_str.isalpha():
        start_ord = ord(start_str)
        end_ord = ord(end_str)
        if start_ord <= end_ord:
            return [chr(i) for i in range(start_ord, end_ord + 1)]
        else:
            return [chr(i) for i in range(start_ord, end_ord - 1, -1)]
    
    return [s] # Not a recognized range

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
        # Expand ranges within each option before further recursion
        range_expanded_options = _expand_range(option)
        for r_option in range_expanded_options:
            # Recursively expand each option
            expanded_option_recursive = brace_expand(r_option)
            for o in expanded_option_recursive:
                for s in expanded_suffix:
                    # Simple and robust path joining:
                    # - If option starts with "/", it's absolute from prefix
                    # - If prefix ends with "/" or is empty, concatenate directly
                    # - If both prefix and option exist and prefix doesn't end with "/", add separator
                    if o.startswith('/') or prefix.endswith('/') or not prefix:
                        combined = prefix + o + s
                    else:
                        # Check if this looks like a path context (contains / or ends with /)
                        # Only add / if we're in a path-like context
                        if ('/' in prefix or '/' in o or o.endswith('/') or 
                            # Special case: if option looks like a filename, we're likely in a directory context
                            ('.' in o and not o.startswith('.'))):
                            combined = prefix + '/' + o + s
                        else:
                            combined = prefix + o + s
                    results.append(combined)

    return sorted(list(set(results)))