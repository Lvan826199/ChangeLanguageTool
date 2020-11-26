import xlrd

class RWExcel:

    def __init__(self):
        # todo 打开excle
        self.xl = xlrd.open_workbook(r'Test.xlsx')

        # todo 通过索引获取工作表
        self.table = self.xl.sheet_by_index(0)
        # print("工作表的名字为：{}".format(self.table.name))

        # 获取一共多少行
        self.rows = self.table.nrows
        # 获取一共有多少列
        self.cols = self.table.ncols
        # print("当前表一共有"+str(self.rows) +"行,"+ str(self.cols) + "列")

        # for i in range(rows):
        #     print(table.cell(i,0))   #打印第一列

    def getSelect(self):
        """
        :return: 获取表中select为1的行数（下标从0开始）
        """
        #读取表格第一列除去第一行的值
        self.fristcol = self.table.col_values(0)
        fristcol_list = []
        fristcol_list.append(self.table.cell(0,0).value) #把第一行第一列的值加进去
        for i  in range(1,len(self.fristcol)) :
            # 把除去第一行的第一列的0和1强转为int类型的数值，并且加入到列表里面(第一行的值最后也在，目的是为了后面通过下标找对应的行)
            fristcol_list.append(int(self.fristcol[i]))
        #print("当前表第一列的值为:{}".format(fristcol_list))

        #获取fristcol_list中为1的下标,同时用一个列表存储这些下标
        indexlist = []

        for  i in range(len(fristcol_list)) :
            if fristcol_list[i] == 1 :  #如果为1，那就是需要运行这一行的代码，此时获取下标，就相当于是获取第几行
                indexlist.append(i)  # i就是下标
        #print("当前表中select是1的行数为：{}".format(indexlist))
        return indexlist

    def selectLanguage(self):
        """

        :return: 获取表格中select为1所对应的语言列表
        """

        indexlist = self.getSelect()  #获取select为1的列
        print("第二个方法里面的Select为1的行数{}".format(indexlist))
        print("---------------------------------")
        languagelist = []
        for  i in  indexlist:
            #获取对应select为1的平台切换语言列表（第4列）
            language = self.table.cell(i,3).value
            languagelist.append(language)  #获取select为1对应的平板切换语言
        print("当前表中select为1对应的切换语言为：{}".format(languagelist))

        return languagelist

    def list_dic(self):
        '''
        two lists merge a dict,a list as key,other list as value
        把select为1的行数作为键，把要切换的语言作为值
        :return:dict
        '''

        list1 = self.getSelect()
        list2 = self.selectLanguage()
        dic = dict(map(lambda x, y: [x, y], list1, list2))
        return dic


    def differ(self,index):
        i = self.table.cell(index,2).value
        j = self.table.cell(index,4).value
        if i == j :
            print("一样")
            print(i)
            print("--------------------------------------")
            print(j)
            return "PASS"

        if i != j :
            print("不一样")
            return "FAILED"




