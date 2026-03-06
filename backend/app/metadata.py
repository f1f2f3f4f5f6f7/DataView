import exiftool

def extract_metadata(file_path):

    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file_path)

    data = metadata[0]

    table = []

    for key, value in data.items():
        table.append({
            "tag": key,
            "value": str(value)
        })

    return table
