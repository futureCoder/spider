import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Bar

regions_dic = {'xierqi1': '西二旗', 'qinghe11': '清河', 'xibeiwang': '西北旺'}


def draw(xlist, ylist1, ylist2, ylist3):
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
        .add_xaxis(xlist)
        .add_yaxis("最低单价", ylist1)
        .add_yaxis("平均单价", ylist2)
        .add_yaxis("最高单价", ylist3)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="海淀各区最低/平均/最高房价单价情况直方图"),
        ).render('分析图表/' + "海淀各区最低-平均-最高房价单价情况直方图.html")
    )


def read_csv():
    regions = []
    min_price_list = []
    avg_price_list = []
    max_price_list = []

    filenames = os.listdir('./爬取结果/')  # 设定调用文件的相对路径
    for i in filenames:
        if '.csv' in str(i):
            regions.append(regions_dic[str(i).split('.')[0]])
            data = pd.read_csv('./爬取结果/' + str(i), encoding='gb18030', header=None)
            data.columns = ['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况',
                            '关注人数', '发布时间', '总价', '单价', '标签']
            data['单价'] = pd.to_numeric(data['单价'].replace('[,元/平]', '', regex=True), errors='coerce')
            min_price_list.append(min(data['单价']))
            avg_price_list.append(round(sum(data['单价']) / len(data), 2))
            max_price_list.append(max(data['单价']))
    draw(regions, min_price_list, avg_price_list, max_price_list)


if __name__ == '__main__':
    read_csv()
