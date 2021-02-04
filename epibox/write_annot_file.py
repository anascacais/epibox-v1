import json

def write_annot_file(annot_file, annot):
    
    #annot_file.write('{}	{}\n'.format(annot[0], annot[1]))
    
    with open(annot_file, 'a') as file:
        file.write('{}	{}\n'.format(annot[0], annot[1]))
    
        