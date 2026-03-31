```python
def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    
    # Open the file to read data
    with open(filename, 'r') as file:
        for line in file:
            # Split each line into creature name and characteristics
            name, characteristics = line.strip().split(': ')
            # Convert the characteristics into a list
            character_list = characteristics.split(', ')
            # Check if the desired characteristic is in the list
            if characteristic in character_list:
                creatures.append(name)
    
    return creatures
```
