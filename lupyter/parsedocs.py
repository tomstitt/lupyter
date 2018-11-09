import re
import requests
import json

doc_url = "http://www.lua.org/manual/{}/manual.html"

def parse_from_url(version):
    req = requests.get(doc_url.format(version))
    lines = req.text.split('\n')
    docs = parse_docs(lines)


def parse_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    docs = parse_docs(lines)


def parse_docs(lines, verbose=False, json_path=None):
    pattern = re.compile('.*(<h3><a name="pdf-([a-z\.]+)"><code>.+</code></a></h3>)')

    docs = {}
    for i in range(len(lines)):
        line = lines[i]
        m = pattern.match(line)
        if m:
            grps = m.groups()
            body = ""
            for j in range(i+1, len(lines)):
                line = lines[j]
                if not line.startswith('<hr>'):
                    body += line
                else:
                    i -= 1
                    break
            docs[grps[1]] = {
                "heading": grps[0],
                "body": re.sub("(\n)+", "\n", body.strip())
            }

    if verbose:
        print("parsed:")
        print("  " + "\n  ".join(docs.keys()))

    if json_path:
        with open(json_path, 'w') as f:
            json.dump(docs, f, indent=2)

    return docs
