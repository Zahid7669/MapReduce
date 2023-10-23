import xml.etree.ElementTree as ET
from collections import defaultdict
import os

# Function to parse an input XML file and create another output XML with the specified structure
def mapper(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    people = root.findall("person")

    map = ET.Element("map")

    for person in people:
        name = person.find("name").text

        item = ET.Element("item")
        names = ET.SubElement(item, "names")
        values = ET.SubElement(item, "values")

        names.text = name
        values.text = "1"

        map.append(item)

    output_tree = ET.ElementTree(map)
    output_tree.write(output_file)

# Function to reduce the output XML file by counting the same names
def reducer(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    items = root.findall("item")

    name_counts = defaultdict(int)

    for item in items:
        name = item.find("names").text
        count = int(item.find("values").text)
        name_counts[name] += count

    reduce = ET.Element("reduce")

    for name, count in name_counts.items():
        item = ET.Element("item")
        names = ET.SubElement(item, "names")
        values = ET.SubElement(item, "values")

        names.text = name
        values.text = str(count)

        reduce.append(item)

    output_tree = ET.ElementTree(reduce)
    output_tree.write(output_file)

def final_reducer(input_files, mapper_output_files, reducer_output_files, final_output_file):
    # Generate mapper output files
    for input_file, mapper_output in zip(input_files, mapper_output_files):
        mapper(input_file, mapper_output)
        print(f"Created mapper output from {input_file}")

    # Reduce the mapper output files and create separate reducer output files
    for mapper_output, reducer_output in zip(mapper_output_files, reducer_output_files):
        reducer(mapper_output, reducer_output)
        print(f"Reduced {mapper_output} and created {reducer_output}")

# Function to calculate the total counts from the reducer output files
def calculate_total_counts(reducer_output_files):
    total_counts = defaultdict(int)
    for reducer_output in reducer_output_files:
        tree = ET.parse(reducer_output)
        root = tree.getroot()
        items = root.findall("item")
        for item in items:
            name = item.find("names").text
            count = int(item.find("values").text)
            total_counts[name] += count
    return total_counts

# Function to create the final output XML with total counts
def generate_final_output(total_counts, final_output_file):
    final_output = ET.Element("final_output")
    for name, count in total_counts.items():
        item = ET.Element("item")
        names = ET.SubElement(item, "names")
        values = ET.SubElement(item, "values")
        names.text = name
        values.text = str(count)
        final_output.append(item)

    output_tree = ET.ElementTree(final_output)
    output_tree.write(final_output_file)
    print(f"Created final output file {final_output_file}")

# Input and output file paths
input_files = ['People1.xml', 'People2.xml', 'People3.xml']
mapper_output_files = ['mapper_People1.xml', 'mapper_People2.xml', 'mapper_People3.xml']
reducer_output_files = ['reducer_People1.xml', 'reducer_People2.xml', 'reducer_People3.xml']
final_output_file = 'final_output.xml'

# Call the final_reducer function to process and reduce the files
final_reducer(input_files, mapper_output_files, reducer_output_files, final_output_file)

# Calculate total counts and generate the final output
total_counts = calculate_total_counts(reducer_output_files)
generate_final_output(total_counts, final_output_file)
