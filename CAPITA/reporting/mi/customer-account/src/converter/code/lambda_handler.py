import csv
''' simple passthrough '''


def handler(event, __context):
    print(f"received event: {event}")
    result = {
        "records": [
            handle_record(record) for record in event.get("records")
        ]
    }
    print(f"Result: {str(result)}")
    return result


def handle_record(record):
    print(f"handle_record: {str(record)}")
    return {
        "recordId": record.get("recordId"),
        "result": "Ok",
        "data": record.get("data")
    }


def convert_csv_to_json(csv_text):
    reader = csv.DictReader(csv_text.split('\n'), delimiter=',')
    entries = []
    for row in reader:
        entry = {}
        for fld, val in row.items():
            typed_val = conv_type(val)
            entry[fld.lower()] = typed_val
        entries.append(entry)
    return entries


def conv_type(txt):
    try:
        return int(txt)
    except ValueError:
        pass
    try:
        return float(txt)
    except ValueError:
        return txt
