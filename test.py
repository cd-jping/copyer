# import xml.etree.ElementTree as ET
import lxml.etree as ET

file = "/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347/appmap_20220922_115417.xml"
file2 = "/Users/WangChunsheng/PycharmProjects/copyer/IconRequest-20221001_122347/appmap_20221001_122343.xml"

xml_tree = ET.parse(file)
xml_root = xml_tree.getroot()
# print(xml_root.findall("."))

xml_tree2 = ET.parse(file2)
xml_root2 = xml_tree2.getroot()
# xml_root2.extend(xml_root.iter("appmap"))
pos_num = -1
for item in xml_root.iter("appmap"):
    # print(item)
    # if item != "appmap":
    #     print(item)
    # if item == "appmap":
    #     print("appmap")
    #     print(bool(item.tag == "appmap"))
    #     # pass
    # else:
    #     print(item)
    #     print(bool(item.tag == "appmap"))
    xml_root2.extend(item)

# xml_root2.extend(xml_root.findall("{*}*"))
# for item in xml_root.iter("*"):
#
#     xml_root2.insert(0, item)

# xml_root2.remove(xml_root2.find("appmap"))

xml_tree2.write(file2, encoding="utf-8", xml_declaration=True)
# print(xml_root2.findall("*"))
