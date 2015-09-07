__author__ = 'seanfitz'
import json

files =[
    '/media/seanfitz/DATA01/raw/assertions/part_00.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_01.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_02.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_03.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_04.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_05.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_06.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_07.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_08.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_09.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_10.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_11.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_12.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_13.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_14.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_15.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_16.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_17.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_18.jsons',
    '/media/seanfitz/DATA01/raw/assertions/part_19.jsons'
    ]



if __name__ == "__main__":
    output_file = None
    current_file_index = 0
    count = 0
    for f_name in files:
        f = open(f_name)
        for line in f.readlines():
            if not output_file:
                output_file_name = '/media/seanfitz/DATA01/facts/conceptnet-facts-%05d.json' % current_file_index
                output_file = open(output_file_name, 'wb')
                print("Writing to %s" % output_file_name)
            doc = json.loads(line)
            rel = doc.get("rel")
            start = doc.get('start')
            end = doc.get('end')
            if rel == "/r/IsA" or rel == "/r/HasA":
                parts = start.split("/")
                start_str = parts[3].replace('_', ' ')
                parts = end.split("/")
                end_str = parts[3].replace('_', ' ')

                relation_str = "IsA" if rel == "/r/IsA" else "HasA"

                output_file.write(json.dumps({
                    'start': start_str,
                    'rel': relation_str,
                    'end': end_str
                }) + '\n')
                count += 1

                if count == 100000:
                    count = 0
                    output_file.close()
                    output_file = None
                    current_file_index += 1