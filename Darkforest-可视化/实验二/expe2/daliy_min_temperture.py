import csv
import pyecharts.options as opts
from pyecharts.charts import Line3D, Bar3D

# 打开csv文件，进行简单的处理
opfile = open("daily-minimum-temperatures-in-me.csv", encoding="UTF-8")
lines = csv.reader(opfile)
data_origin = []
for line in lines:
    data_origin.append(line)
data_origin = data_origin[1:-3]

# 由数据获取x,y,z的值
data = []
x = []
y = []
for line in data_origin:
    year, month, day = line[0].split("-")
    mad = month + "/" + day
    if year not in x:
        x.append(year)
    if mad not in y:
        y.append(mad)
    data.append([year, mad, line[1]])

(
    Bar3D(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add(
        series_name="余宗源-18130500230",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(data=x, type_="category"),
        yaxis3d_opts=opts.Axis3DOpts(data=y, type_="category"),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=70, height=70, depth=150),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(subtitle="请手动刷一下右边的视觉映射条"),
        visualmap_opts=opts.VisualMapOpts(
            pos_top="40%",
            pos_left="10%",
            max_=25,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        )
    )
    .render("daliy_min_temperture.html")
)
