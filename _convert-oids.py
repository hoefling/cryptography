import os
from pathlib import Path

oids_spec = Path("gemspec-oid-v3.17.0-oids.txt")

lines = oids_spec.read_text(encoding='utf-8').split(os.linesep)
oid_names = []

class_attribute_lines = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith('#'):
        
    name, *_, oid = line.split()
    cryptography_const_name = name.upper().removeprefix('OID_').replace('-', '_')
    py_line = f'{cryptography_const_name} = ObjectIdentifier("{oid}")'
    if oid.lower() == 'tbd':
        py_line = f'# {py_line}'
    else:
        oid_names.append((cryptography_const_name, name))
    class_attribute_lines.append(f"    {py_line}")

print('class ProfessionOID:')
for line in sorted(class_attribute_lines):
    print(line)

print()

print('_OID_NAMES = {')
for (k, v) in sorted(oid_names):
    print(f'    ProfessionOID.{k}: "{v}",')
print('}')
