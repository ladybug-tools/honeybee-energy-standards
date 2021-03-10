import os
import json

from honeybee.model import Model

ref_blgd_folder = 'C:/Users/chris/simulation/Baseline_Models/hbjson'
output_file = 'honeybee_energy_standards/building_mix.json'

building_mix = {}

for hbjson_file in os.listdir(ref_blgd_folder):
    # load the model to python
    bldg_name = hbjson_file.replace('.hbjson', '')
    hbjson_path = os.path.join(ref_blgd_folder, hbjson_file)
    with open(hbjson_path) as inf:
        model_dict = json.load(inf)
    for room in model_dict['rooms']:
        room['identifier'] = room['identifier'].replace('/', '').replace(':', '')
        for face in room['faces']:
            if 'apertures' in face:
                for ap in face['apertures']:
                    ap['identifier'] = ap['identifier'].replace('/', '').replace(':', '')
            if 'doors' in face:
                for dr in face['doors']:
                    dr['identifier'] = dr['identifier'].replace('/', '').replace(':', '')
    model = Model.from_dict(model_dict)

    # collect the floor areas for each of the space types
    bld_area_dict = {}
    for room in model.rooms:
        if 'space_type' in room.user_data:
            space_type = room.user_data['space_type']
            try:
                bld_area_dict[space_type] += room.floor_area
            except KeyError:
                bld_area_dict[space_type] = room.floor_area

    # turn the floor areas into fractional values
    total_area = sum(bld_area_dict.values())
    bld_fraction_dict = {}
    for key, value in bld_area_dict.items():
        new_key = key.replace(bldg_name, '').strip()
        new_key = '2013::{}::{}'.format(bldg_name, new_key)
        bld_fraction_dict[new_key] = round(value / total_area, 6)
    building_mix[bldg_name] = bld_fraction_dict

# write the JSON into a file
with open(output_file, 'w') as fp:
    json.dump(building_mix, fp, indent=4)
