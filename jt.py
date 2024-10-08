import sys
import json
import argh
from tabulate import tabulate


def flatten_dict(d, parent_key="", sep="."):
    """
    Recursively flattens a nested dictionary, including lists of dictionaries.
    """
    items = {}
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten_dict(v, new_key, sep=sep))
    elif isinstance(d, list):
        if all(isinstance(elem, dict) for elem in d):
            temp = {}
            for elem in d:
                elem_items = flatten_dict(elem, "", sep=sep)
                for k, v in elem_items.items():
                    temp.setdefault(k, []).append(v)
            for k, v_list in temp.items():
                combined_key = f"{parent_key}{sep}{k}" if parent_key else k
                items[combined_key] = ", ".join(map(str, v_list))
        else:
            items[parent_key] = ", ".join(map(str, d))
    else:
        items[parent_key] = d
    return items


@argh.arg("--sep", default=".", help="Separator for nested keys")
@argh.arg(
    "--columns",
    help='Comma-separated list of columns to output. Optionally rename columns using "column_path=new_name"',
)
@argh.arg("--tablefmt", default="orgtbl", help="Table format for tabulate")
def main(sep=".", columns=None, tablefmt="orgtbl"):
    """
    Reads a JSON string from stdin and outputs a flattened table.
    """
    input_data = sys.stdin.read()
    data = json.loads(input_data)
    if not isinstance(data, list):
        data = [data]
    flattened_data = [flatten_dict(d, sep=sep) for d in data]

    header_mappings = {}
    if columns:
        headers = []
        for col in columns.split(","):
            col = col.strip()
            if "=" in col:
                col_path, col_name = col.split("=", 1)
                col_path = col_path.strip()
                col_name = col_name.strip()
                headers.append(col_path)
                header_mappings[col_path] = col_name
            else:
                headers.append(col)
    else:
        headers = sorted({key for item in flattened_data for key in item.keys()})
        header_mappings = {}

    table = [[item.get(header, "") for header in headers] for item in flattened_data]
    output_headers = [header_mappings.get(header, header) for header in headers]
    print(tabulate(table, headers=output_headers, tablefmt=tablefmt))


@argh.arg("--sep", default=".", help="Separator for nested keys")
def list_columns(sep="."):
    """
    Reads a JSON string from stdin and outputs the list of available columns.
    """
    input_data = sys.stdin.read()
    data = json.loads(input_data)
    if not isinstance(data, list):
        data = [data]
    flattened_data = [flatten_dict(d, sep=sep) for d in data]
    columns = sorted({key for item in flattened_data for key in item.keys()})
    for col in columns:
        print(col)


if __name__ == "__main__":
    argh.dispatch_commands([main, list_columns])
