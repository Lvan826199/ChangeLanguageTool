import xlrd
import xlsxwriter

class rwExcel:


    def __init__(self):
        pass

    def readexcel(self):
        # todo 打开excle
        xl = xlrd.open_workbook(r'Test.xlsx')
        #print(xl.read())

        # todo 通过索引获取工作表
        table = xl.sheets()[0]
        print(table)

        # 获取一共多少行
        rows = table.nrows
        print(rows)


        # todo 获取第一行的内容,索引从0开始
        row = table.row_values(0)
        print(row)


        # todo 获取第一列的整列的内容
        col = table.col_values(0)
        print(col)

        # todo 获取单元格值，第几行第几个，索引从0开始
        data = table.cell(2, 2).value
        print(data)


    def writeexcel(self):

        # todo 创建excel文件
        xl = xlsxwriter.Workbook(r'../Excel_Report/test.xlsx')

        # todo 添加sheet
        sheet = xl.add_worksheet('sheet1')

        # todo 往单元格cell添加数据,索引写入
        sheet.write_string(0, 0, 'username')

        # todo 位置写入
        sheet.write_string('B1', 'password')

        # todo 设置单元格宽度大小
        sheet.set_column('A:B', 30)

        # todo 关闭文件
        xl.close()

if __name__ == '__main__':
    w= rwExcel()
    read = w.readexcel()
