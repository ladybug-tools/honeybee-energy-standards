import os
import json

from honeybee.model import Model

ref_blgd_folder = 'G:/My Drive/LadybugTools/Baseline_Models/hbjson'
output_file = 'honeybee_energy_standards/building_mix.json'

# programs to exclude
EX_PROGRAM =(
    'Outpatient Hall_infil',
    'LargeHotel Corridor2',
    'LargeHotel Retail2'
)

building_mix = {}

for hbjson_file in os.listdir(ref_blgd_folder):
    # load the model to python
    bldg_name = hbjson_file.replace('.hbjson', '')
    hbjson_path = os.path.join(ref_blgd_folder, hbjson_file)
    model = Model.from_hbjson(hbjson_path)

    # collect the floor areas for each of the space types
    bld_area_dict = {}
    for room in model.rooms:
        if 'space_type' in room.user_data and not room.exclude_floor_area:
            space_type = room.user_data['space_type']
            if space_type.startswith('SmallHotel'):
                space_type = space_type.replace('123', '').replace('4', '')
                space_type = space_type.replace('Front', '').replace('Rear', '')
            elif space_type.startswith('StripMall'):
                space_type = space_type.replace('Strip mall', '').replace('type', 'Type')
            elif space_type.startswith('MidriseApartment') or space_type.startswith('HighriseApartment'):
                space_type = space_type.replace('_topfloor', '').replace('_NS', '').replace('_WE', '')

            if space_type not in EX_PROGRAM:
                try:
                    bld_area_dict[space_type] += room.floor_area * room.multiplier
                except KeyError:
                    bld_area_dict[space_type] = room.floor_area * room.multiplier

    # turn the floor areas into fractional values
    total_area = sum(bld_area_dict.values())
    bld_fraction_dict = {}
    for key, value in bld_area_dict.items():
        new_key = key.replace(bldg_name, '', 1).replace('-', '').strip()
        new_key = '2013::{}::{}'.format(bldg_name, new_key)
        bld_fraction_dict[new_key] = round(value / total_area, 6)
    building_mix[bldg_name] = bld_fraction_dict

# write the JSON into a file
with open(output_file, 'w') as fp:
    json.dump(building_mix, fp, indent=4)
