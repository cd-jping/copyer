# import xml.etree.ElementTree as ET
import lxml.etree as lxmlET
import xml.dom.minidom as domxml

file = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347/drawable.xml"
file2 = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347/appmap_20221001_122343.xml"
# parser = ET.XMLParser(encoding="utf-8", strip_cdata=False, remove_blank_text=True)
xml_tree = lxmlET.parse(file, parser=lxmlET.XMLParser(encoding="utf-8", remove_blank_text=True))
xml_root = xml_tree.getroot()
# print(xml_root.findall("."))
# sasaass=domxml.Document()
item = lxmlET.Element("item", nsmap=None)
item1 = lxmlET.Element("item", nsmap=None)
item2 = lxmlET.Element("item", nsmap=None)
item3 = lxmlET.Element("item", nsmap=None)
item.set("drawable", "TEST_Text")
s = xml_root.find("./category/[@title='System ICONS']")
print(type(s))
s.addnext(item)

# item.text = str("sdiad")
# item = ET.Element()
# print(lxmlET.tostring(item, pretty_print=True))
# xml_root.append(item)
# xml_root.append(item1)
# xml_root.append(item2)
# xml_root.append(item3)
# print(lxmlET.tostring(xml_root, pretty_print=True))
# b = ET.SubElement(a, 'b')
# c = ET.SubElement(a, 'c')
# d = ET.SubElement(c, 'd')
# sa = xml_root.find("./string-array/[@name='icons_preview']")
test = ["asd", "das", "asda", "asda"]
print(len(test))

if xml_root.find("./category/[@title='System ICONS']") is None:
    tar_tag = lxmlET.Element("category", name="System ICONS")
    xml_root.append(tar_tag)
    print("if")
else:
    tar_tag = xml_root.find("./category/[@title='System ICONS']")
    print("eles")

print(type(tar_tag))
# xml_root.find("./category/[@name='System ICONS']").addnext(item)

# print(sa)
# doc = domxml.Document()
# item = doc.createElement("item")
# item.appendChild(doc.createTextNode("str(i)"))

number = 12
comments = lxmlET.Comment(f"⬇ {number} icons updated ⬇")
tar_tag.addnext(comments)
# comments.tail = "\n"
# tar_tag.addnext(comments)
# xml_root
# xml_root.appendChild(item)
# sa.appendChild(item)
xml_tree2 = lxmlET.parse(file2)
xml_root2 = xml_tree2.getroot()
# xml_root2.extend(xml_root.iter("appmap"))
# pos_num = -1
#
# for item in xml_root.iter("appmap"):
#     # print(item)
#     # if item != "appmap":
#     #     print(item)
#     # if item == "appmap":
#     #     print("appmap")
#     #     print(bool(item.tag == "appmap"))
#     #     # pass
#     # else:
#     #     print(item)
#     #     print(bool(item.tag == "appmap"))
#     comments = ET.Comment("comments")
#     comments.tail = "\n"
#     xml_root2.append(comments)
#     # xml_root2.extend(item)

# xml_root2.extend(xml_root.findall("{*}*"))
# for item in xml_root.iter("*"):
#
#     xml_root2.insert(0, item)

# xml_root2.remove(xml_root2.find("appmap"))

xml_tree.write(file, encoding="utf-8", xml_declaration=True, pretty_print=True)
# print(xml_root2.findall("*"))
