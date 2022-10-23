import xml.dom.minidom as minidom

file = "/Users/wangjiping/PycharmProjects/copyer/IconRequest-20221001_122347/appfilter_20220922_115417.xml"

doc = minidom.parse(file)
print(doc)
root = doc.documentElement
root = root.Comment
print(root)