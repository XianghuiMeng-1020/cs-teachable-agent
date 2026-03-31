```python
def find_creatures_by_attribute(file_path, attribute):
    creature_names = []
    with open(file_path, 'r') as f:
        content = f.read().strip()
    
    entries = content.split('\n\n')
    for entry in entries:
        parts = entry.strip().split('\n')
        if len(parts) < 2:
            continue
        
        name_line = parts[0]
        attributes_line = parts[1]
        
        if not attributes_line.startswith('Attributes:'):
            continue
        
        name = name_line.split(':')[0].strip()
        attributes = attributes_line[len('Attributes:'):].strip()
        attribute_list = [attr.strip() for attr in attributes.split(',')]
        
        if attribute in attribute_list:
            creature_names.append(name)

    return creature_names
```
