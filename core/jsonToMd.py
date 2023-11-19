#!/usr/bin/env python

import json, pypandoc

def main():
    f = open('data.json')
    print(pypandoc.convert_text(f.read, 'json', 'md'))


if __name__ == "__main__":
    main()