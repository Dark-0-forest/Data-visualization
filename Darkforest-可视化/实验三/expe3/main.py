import math
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Surface3D, Line3D, Tab


# 1.螺旋曲线
data = []
# 循环生成螺旋线的坐标
for w in np.mgrid[0:60.1:0.1] * math.pi:
    x = 5 * math.cos(0.5 * w)
    y = 5 * math.sin(0.5 * w)
    z = 0.5 * w
    data.append([x, y, z])

helical_curve = (
    Line3D(init_opts=opts.InitOpts(width="1600px", height="700px"))
    .add(
        series_name="余宗源-18130500230",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=50, height=100, depth=50),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            pos_top="40%",
            pos_left="10%",
            dimension=2,
            max_=100,
            min_=0,
            range_color=["#a50026"],
        )
    )
)


# 2.二元正态分布曲面
x = np.mgrid[-2:2.01:0.01]
y = np.mgrid[-2:2.01:0.01]
data = []

for x0 in x:
    for y0 in y:
        z = (1 / 2 * math.pi * 3 ** 2) * np.exp((-(x0 ** 2 + y0 ** 2) / 2 * 3 ** 2))
        data.append([x0, y0, z])

bivariate_normal = (
    Line3D(init_opts=opts.InitOpts(width="1600px", height="700px"))
    .add(
        series_name="余宗源-18130500230",
        shading="color",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=80, height=80, depth=80),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            pos_top="40%",
            pos_left="10%",
            dimension=2,
            max_=15,
            min_=0,
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
)


# 3.球面
# 上半球的左边集合
data_top = []
# 下半球的左边集合
data_bottom = []

# 循环生成上半球坐标
for t0 in np.mgrid[0:2.01:0.01] * math.pi:
    s1 = t0
    for t1 in np.mgrid[0:1.01:0.01] * math.pi:
        s2 = t1
        x = 5 * math.sin(s2) * math.cos(s1)
        y = 5 * math.sin(s2) * math.sin(s1)
        z = 5 * math.cos(s2)
        if z >= 0:
            data_top.append([x, y, z])

# 由上半球坐标来得到下半球坐标
for [x, y, z] in data_top:
    data_bottom.append([x, y, -z])

sphere = (
    Surface3D(init_opts=opts.InitOpts(width="1600px", height="700px"))
    .add(
        series_name="余宗源-18130500230",
        shading="color",
        data=data_top,
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=80, height=80, depth=80),
    )
    .add(
        series_name="",
        shading="color",
        data=data_bottom,
        xaxis3d_opts=opts.Axis3DOpts(type_="value"),
        yaxis3d_opts=opts.Axis3DOpts(type_="value"),
        grid3d_opts=opts.Grid3DOpts(width=80, height=80, depth=80),
    )

    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            pos_top="40%",
            pos_left="10%",
            dimension=2,
            max_=6,
            min_=-6,
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
)

tab = Tab()
tab.add(helical_curve, "螺旋曲线")
tab.add(bivariate_normal, "二元正态曲面")
tab.add(sphere, "球面")
tab.render("3Dgraph.html")
