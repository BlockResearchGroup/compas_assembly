import json
import pathlib


def data_2to3(filepath):
    with open(filepath) as fp:
        rawdata = json.load(fp)

    def replace_value_keys(dictitem):
        if "dtype" in dictitem and "value" in dictitem and "data" in dictitem["value"]:
            dictitem = {"dtype": dictitem["dtype"], "data": dictitem["value"]["data"]}

        for key in dictitem:
            value = dictitem[key]

            if key == "value":
                key = "data"
            elif key == "datatype":
                key = "dtype"

            data[key] = value

            if isinstance(value, dict):
                replace_value_keys(value)

    data = {}
    replace_value_keys(rawdata)

    with open(filepath, "w") as fp:
        json.dump(data, fp)


filepath = pathlib.Path(__file__).parent / "arch.json"

data_2to3(filepath)
