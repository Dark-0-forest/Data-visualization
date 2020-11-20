import pandas as pd
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Parallel, Tab, Bar

df1 = pd.read_excel("classifyday1.xlsx")
df2 = pd.read_excel("time_allocate_day1.xlsx")

# 选项卡
tab = Tab()
# 用字典来对每种工作赋值
job = {'waiter': 0, 'vip': 1, 'participant': 2, 'meeting': 3, 'reporter': 4}

"""1.处理人员分类的热力图"""
# 对excel中的文件读取，获得每个ID对应的类别
classfication_origin = {}
for line in df1.groupby("id"):
    line_list = line[1].values
    job_num = job[line_list[0][1]]
    classfication_origin[line_list[0][0]] = line_list[0][1]

scheme = [
            opts.ParallelAxisOpts(dim=0, name="分会场A"),
            opts.ParallelAxisOpts(dim=1, name="分会场B"),
            opts.ParallelAxisOpts(dim=2, name="分会场C"),
            opts.ParallelAxisOpts(dim=3, name="分会场D"),
            opts.ParallelAxisOpts(dim=4, name="主会场"),
            opts.ParallelAxisOpts(dim=5, name="room1"),
            opts.ParallelAxisOpts(dim=6, name="room2"),
            opts.ParallelAxisOpts(dim=7, name="room3"),
            opts.ParallelAxisOpts(dim=8, name="room4"),
            opts.ParallelAxisOpts(dim=9, name="room5"),
            opts.ParallelAxisOpts(dim=10, name="room6"),
            opts.ParallelAxisOpts(dim=11, name="餐厅"),
            opts.ParallelAxisOpts(dim=12, name="厕所1"),
            opts.ParallelAxisOpts(dim=13, name="厕所2"),
            opts.ParallelAxisOpts(dim=14, name="厕所3"),
            opts.ParallelAxisOpts(dim=15, name="服务台"),
            opts.ParallelAxisOpts(dim=16, name="过道1楼"),
            opts.ParallelAxisOpts(dim=17, name="过道2楼"),
            opts.ParallelAxisOpts(dim=18, name="楼梯"),
            opts.ParallelAxisOpts(dim=19, name="海报区"),
            opts.ParallelAxisOpts(dim=20, name="签到处"),
            opts.ParallelAxisOpts(dim=21, name="休息处"), ]

# 获取不同类别人员id的数据信息
data_all = []
data_meeting = []
data_participant = []
data_vip = []
data_waiter = []
data_reporter = []
for line in df2.value_counts().index:
    data_all.append(line[1:])
    if classfication_origin[line[0]] == "meeting":
        data_meeting.append(line[1:])
    elif classfication_origin[line[0]] == "participant":
        data_participant.append(line[1:])
    elif classfication_origin[line[0]] == "vip":
        data_vip.append(line[1:])
    elif classfication_origin[line[0]] == "waiter":
        data_waiter.append(line[1:])
    elif classfication_origin[line[0]] == "reporter":
        data_reporter.append(line[1:])

parallel1 = (
    Parallel(init_opts=opts.InitOpts(width="1600px", height="700px"))
    .add_schema(scheme)
    .add("data", data_all, linestyle_opts=opts.LineStyleOpts(opacity=0.05))
)

parallel2 = (
    Parallel(init_opts=opts.InitOpts(width="1600px", height="700px"))
    .add_schema(scheme)
    .add("reporter", data_reporter, linestyle_opts=opts.LineStyleOpts(opacity=0.3))
    .add("waiter", data_waiter, linestyle_opts=opts.LineStyleOpts(opacity=0.3))
    .add("vip", data_vip, linestyle_opts=opts.LineStyleOpts(opacity=0.2))
    .add("meeting", data_meeting, linestyle_opts=opts.LineStyleOpts(opacity=0.1))
    .add("participant", data_participant, linestyle_opts=opts.LineStyleOpts(opacity=0.2))
)

tab.add(parallel1, "人员类别分析图(无类别)")
tab.add(parallel2, "人员类别分析图(有类别)")


"""2.每类人员在不同房间的停留时间比例的折线图"""
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

# 求出每一种人员对于room的访问时间占比，同时将其访问时间按比例缩小1000
for i in range(0, 5):
    num = sum(room_stay_time[i])
    rate = []
    thousand = []
    for j in range(0, 6):
        rate.append(round((room_stay_time[i][j] / room_total_time[j]), 3))
        thousand.append(room_stay_time[i][j] / 1000)
    room_stay_time_rate.append(rate)
    room_stay_time_thousand.append(thousand)

# 为bar填充数据，同时保存其值和对应的占比
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

