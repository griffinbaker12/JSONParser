def read_file(json_file):
    with open(json_file) as f:
        json_content = f.read()
    return json_content


def print_sandwich(s):
    print("-" * len(s))
    print(s)
    print("-" * len(s))
