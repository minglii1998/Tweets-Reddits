import csv

# 文件头，一般就是数据名
fileHeader = ["name", "score",'sss']

# 假设我们要写入的是以下两行数据
d1 = ["Wang",'',"100"]
d2 = ["Li", "80"]

# 写入数据

csvFile = open("instance.csv", "a", newline='')
writer = csv.writer(csvFile)

# 写入的内容都是以列表的形式传入函数
writer.writerow(fileHeader)
writer.writerow(d1)
writer.writerow(d1)

csvFile.close()

pass