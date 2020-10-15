street_type_mapping = {'AL': 'Alley', 'AV': 'Avenue',
                       'BA': 'Bay', 'BV': 'Boulevard',
                       'CA': 'Cape', 'CE': 'Centre', 'CI': 'Circle', 'CL': 'Close', 'CM': 'Common', 'CO': 'Court', 'CR': 'Crescent', 'CV': 'Cove',
                       'DR': 'Drive',
                       'GA': 'Gate', 'GD': 'Gardens', 'GR': 'Green', 'GV': 'Grove',
                       'HE': 'Heath', 'HI': 'Highway', 'HL': 'Hill', 'HT': 'Heights',
                       'IS': 'Island',
                       'LD': 'Landing', 'LI': 'Link', 'LN': 'Lane',
                       'ME': 'Mews', 'MR': 'Manor', 'MT': 'Mount',
                       'PA': 'Park', 'PH': 'Path', 'PL': 'Place', 'PR': 'Parade', 'PS': 'Passage', 'PT': 'Point', 'PY': 'Parkway', 'PZ': 'Plaza',
                       'RD': 'Road', 'RI': 'Rise', 'RO': 'Row',
                       'SQ': 'Square', 'ST': 'Street',
                       'TC': 'Terrace', 'TR': 'Trail',
                       'VI': 'Villas', 'VW': 'View',
                       'WK': 'Walk', ### UNCLEAN DATA! Be careful. Watch your WKs
                       'WK': 'Walkway',
                       'WY': 'Way'}

new_street_mapping = {}
for k,v in street_type_mapping.items():
    new_street_mapping[v] = k

print(new_street_mapping)