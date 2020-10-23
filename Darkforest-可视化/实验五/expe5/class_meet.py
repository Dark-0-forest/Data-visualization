import pandas as pd
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import HeatMap, Tab, Bar

df1 = pd.read_excel("classifyday1.xlsx")
df2 = pd.read_excel("time_allocate_day1.xlsx")

tab = Tab()
# 用字典来对每种工作赋值
job = {'waiter': 0, 'vip': 1, 'participant': 2, 'meeting': 3, 'reporter': 4}
"""处理人员分类的热力图"""
# 获取两位的横坐标
x = []
for i in range(100):
        fmt = str("{:0>2d}".format(i))
        x.append(fmt)
# 对excel中的文件读取，获得画图用的坐标
classfication_origin = {}
classfication = []
for line in df1.groupby("id"):
    line_list = line[1].values
    job_num = job[line_list[0][1]]
    classfication_origin[line_list[0][0]] = line_list[0][1]
    classfication.append([int(str(line_list[0][0])[3:]), int(str(line_list[0][0])[:3]), job_num])
# 每个类别用不同的颜色标识
pieces = [
        {'max': 0, 'min': 0, 'label': 'waiter', 'color': '#228B22'},
        {'max': 1, 'min': 1, 'label': 'vip', 'color': '#FF0000'},
        {'max': 2, 'min': 2, 'label': 'participant', 'color': '#0099CC'},
        {'max': 3, 'min': 3, 'label': 'meeting', 'color': '#FF9966'},
        {'max': 4, 'min': 4, 'label': 'reporter', 'color': '#8B008B'}
    ]
# 创建热力图
heatmap = (
    HeatMap(init_opts=opts.InitOpts(width="1400px", height="1400px"))
    .add_xaxis(x)
    .add_yaxis(
        series_name="类别",
        yaxis_data=(range(100, 200)),
        value=classfication,
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces, pos_top="35%"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            axislabel_opts=opts.LabelOpts(
                font_size=8,
                interval=0
            )
        ),
        yaxis_opts=opts.AxisOpts(
            type_="category",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            axislabel_opts=opts.LabelOpts(
                font_size=8,
                interval=0
            )
        ),
    )
)
# 把热力图添加到整个tab上
tab.add(heatmap, "人员分类热力图")

"""每类人员在不同房间的停留时间比例的折线图"""
# test = pd.read_excel("time_allocate_day1 - test.xlsx")
room_stay_time = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
for line in df2.groupby("id"):
    line_list = line[1].values
    job_num = job[classfication_origin[line_list[0][0]]]
    room_stay_time[job_num][0] += line_list[0][6]
    room_stay_time[job_num][1] += line_list[0][7]
    room_stay_time[job_num][2] += line_list[0][8]
    room_stay_time[job_num][3] += line_list[0][9]
    room_stay_time[job_num][4] += line_list[0][10]
    room_stay_time[job_num][5] += line_list[0][11]

# 算出每个的比例
room_total_time = []
room_stay_time_rate = []
room_stay_time_thousand = []
data = []

# 计算每一列的和
for i in range(0, 6):
    room_total_time.append(sum(num[i] for num in room_stay_time))

for i in range(0, 5):
    num = sum(room_stay_time[i])
    rate = []
    thousand = []
    for j in range(0, 6):
        rate.append(round((room_stay_time[i][j] / room_total_time[j]), 3))
        thousand.append(room_stay_time[i][j] / 1000)
    room_stay_time_rate.append(rate)
    room_stay_time_thousand.append(thousand)

for i in range(0, 5):
    y = []
    for j in range(0, 6):
        y1 = {"value": room_stay_time_thousand[i][j], "percent": room_stay_time_rate[i][j]}
        y.append(y1)
    data.append(y)

room = ["room1", "room2", "room3", "room4", "room5", "room6"]
bar = (
    Bar(init_opts=opts.InitOpts(width="1400px", height="700px"))
    .add_xaxis(room)
    .add_yaxis("waiter", data[0], stack="stack1", category_gap="50%")
    .add_yaxis("vip", data[1], stack="stack1", category_gap="50%")
    .add_yaxis("participant", data[2], stack="stack1", category_gap="50%")
    .add_yaxis("meeting", data[3], stack="stack1", category_gap="50%")
    .add_yaxis("reporter", data[4], stack="stack1", category_gap="50%")
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="单位：千",
            name_textstyle_opts=opts.TextStyleOpts(font_size=15)
        ),

    )
    .set_series_opts(
        label_opts=opts.LabelOpts(
            position="right",
            formatter=JsCode(
                "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
            ),
        ),
    )
)
tab.add(bar, "room功能分析图")
tab.render("class_meet.html")

