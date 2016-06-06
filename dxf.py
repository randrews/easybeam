def parse(filename):
    "Parse a DXF file, returning a list of dictionaries for the lines / arcs"
    dxf = _file_tuples(filename)
    entities = []
    for section in _sections(dxf):
        if _entity_section(section):
            entities.extend(_entities(section))
    return entities

##################################################

def _file_tuples(filename):
    "Read a DXF file and return an array of (group_code, value) tuples"
    f = open(filename, 'r')
    tuples = []
    code = None
    for line in f:
        if code:
            tuples.append((code, line.strip()))
            code = None
        else:
            code = line.strip()

    return tuples

def _sections(tuples):
    "Take an array of tuples and partition it into sections, returning an array of sections"
    sections_list = []
    curr_section = []
    in_section = False
    for t in tuples:
        if in_section:
            # Check for a section end
            if t[0] == '0' and t[1] == 'ENDSEC':
                sections_list.append(curr_section)
                in_section = False
            else:
                curr_section.append(t)
        else:
            # Check for a section start
            if t[0] == '0' and t[1] == 'SECTION':
                curr_section = []
                in_section = True
    return sections_list

def _entity_section(section):
    "Predicate for if an array of tuples is an 'entities' section"
    names = (tuple[1] for tuple in section if tuple[0] == '2')
    return next(names, False) == 'ENTITIES'

def _entities(section):
    "Take an array of tuples from an 'entities' section, return an array of dictionaries for lines and arcs"
    entities = []
    current_entity = None
    mode = None
    for t in section:
        if t[0] == '0' and t[1] == 'LINE':
            mode = 'line'
            current_entity = {'type': 'line'}
            entities.append(current_entity)
        elif t[0] == '0' and t[1] == 'ARC':
            mode = 'arc'
            current_entity = {'type': 'arc'}
            entities.append(current_entity)
        elif mode == 'line':
            if t[0] == '8': current_entity['layer'] = int(t[1])
            if t[0] == '10': current_entity['x1'] = float(t[1])
            if t[0] == '20': current_entity['y1'] = float(t[1])
            if t[0] == '11': current_entity['x2'] = float(t[1])
            if t[0] == '21': current_entity['y2'] = float(t[1])
        elif mode == 'arc':
            if t[0] == '8': current_entity['layer'] = int(t[1])
            if t[0] == '10': current_entity['x'] = float(t[1])
            if t[0] == '20': current_entity['y'] = float(t[1])
            if t[0] == '40': current_entity['r'] = float(t[1])
            if t[0] == '50': current_entity['a1'] = float(t[1])
            if t[0] == '51': current_entity['a2'] = float(t[1])
    return entities
