import os
from pathlib import Path
import re

section_pattern = re.compile(r".*\s\((?P<type>.*)\)")

oids_spec = Path("gemspec-oid-v3.17.0-oids.txt")

lines = oids_spec.read_text(encoding="utf-8").split(os.linesep)
oid_type2names = {}
oid_type = ""
names = []
class_attribute_lines = {}
attribute_lines = []

for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("#"):
        stored_names = oid_type2names.get(oid_type, [])
        stored_names.extend(names)
        oid_type2names[oid_type] = stored_names
        names.clear()

        stored_attribute_lines = class_attribute_lines.get(oid_type, [])
        stored_attribute_lines.extend(attribute_lines)
        class_attribute_lines[oid_type] = stored_attribute_lines
        attribute_lines.clear()

        oid_type = section_pattern.match(line).groupdict().get("type")
        continue

    name, *_, oid = line.split()
    cryptography_const_name = (
        name.upper().removeprefix("OID_").replace("-", "_")
    )
    py_line = f'{cryptography_const_name} = ObjectIdentifier("{oid}")'
    if oid.lower() == "tbd":
        py_line = f"# {py_line}"
    else:
        names.append((cryptography_const_name, name))
    attribute_lines.append(f"    {py_line}")


profession_oid_class = "ProfessionOID"
print(f"class {profession_oid_class}:")
for line in sorted(class_attribute_lines[profession_oid_class]):
    print(line)

print()

print("_OID_NAMES = {")
for k, v in sorted(oid_type2names[profession_oid_class]):
    print(f'    {profession_oid_class}.{k}: "{v}",')
print("}")
