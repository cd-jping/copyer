import os

for root, dirs, files in os.walk("/Users/wangjiping/Downloads/demo"):
    for name in files:
        if "app" in name:
            print(name, os.path.join(root,name))
        # print(name)
    # for name in dirs:
    #     print(os.path.join(root, name))