import chardet

path = 'translations.txt'
with open(path, mode='rb') as f:
    binary = f.read()
    code = chardet.detect(binary)['encoding']
    print(code)

with open(path, encoding=code) as f:
    translation_lines = [x.strip('\n') for x in f.readlines() if x != '\n']

#print(translation_lines[:10])
print(len(translation_lines))

with open('originals.txt', encoding=code) as f:
    original_lines = [x.strip('\n') for x in f.readlines() if x != '\n']

#print(original_lines[:10])
print(len(original_lines))

for orig, tr in zip(original_lines, translation_lines):
    print(f'{orig}: {tr}')