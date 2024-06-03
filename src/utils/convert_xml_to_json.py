import json
import xmltodict

def convert_xml_to_json(input_path="data/hmdb_metabolites.xml", output_path="data/hmdb_metabolites.json"):
    """
    Convert an XML file to JSON format and save it to a specified output file path.

    Args:
        input_path (str): The file path of the input XML file. Default is "data/hmdb_metabolites.xml".
        output_path (str): The file path of the output JSON file. Default is "data/hmdb_metabolites.json".

    Returns:
        str: The file path of the output JSON file.
    """
    try:
        with open(input_path, "r") as f:
            xml_data = f.read()

        json_data = json.dumps(xmltodict.parse(xml_data),
                               sort_keys=False, indent=2)

        with open(output_path, "w") as f:
            f.write(json_data)

        print(f"Successfully converted {input_path} to {output_path}")
    except FileNotFoundError:
        print(f"Error: {input_path} not found")
    except Exception as e:
        print(f"Error: {e}")

    return output_path
