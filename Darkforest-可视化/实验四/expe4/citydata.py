import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline

df = pd.read_excel("CityData.xlsx")

data = []
dates = []

for line in df.groupby(["updateTime", "provinceName"]):
    line_list = line[1].values
    data.append([line_list[0][1], str(line_list[0][7]).split(" ")[0], line[1].city_confirmedCount.sum()])
    date = str(line_list[0][7]).split(" ")[0]
    if date not in dates:
        dates.append(date)

num_last = []
for i in data:
    if i[0] not in (line[0] for line in num_last):
        num_last.append([i[0], 0])
for i in num_last:
    i[0] = i[0].split("市")[0]
    i[0] = i[0].split("省")[0]
    i[0] = i[0].split("维吾尔自治区")[0]
    i[0] = i[0].split("回族自治区")[0]
    i[0] = i[0].split("壮族自治区")[0]
    i[0] = i[0].split("自治区")[0]

t = Timeline(init_opts=opts.InitOpts(width="1400px", height="700px"))
t.add_schema(play_interval=500)

pieces = [
        {'max': 1, 'label': '0', 'color': 'white'},
        {'min': 1, 'max': 20, 'label': '1-20', 'color': '#FFFAFA'},
        {'min': 20, 'max': 50, 'label': '20-50', 'color': '#FAF0E6'},
        {'min': 50, 'max': 100, 'label': '50-100', 'color': '#FFEFD5'},
        {'min': 100, 'max': 200, 'label': '100-200', 'color': '#FFDAB9'},
        {'min': 200, 'max': 500, 'label': '200-500', 'color': '#FFB6C1'},
        {'min': 500, 'max': 1000, 'label': '500-1000', 'color': '#FF69B4'},
        {'min': 1000, 'max': 5000, 'label': '1000-5000', 'color': '#FF4500'},
        {'min': 5000, 'max': 10000, 'label': '5000-10000', 'color': '#DC143C'},
        {'min': 10000, 'max': 50000, 'label': '10000-50000', 'color': '#B22222'},
        {'min': 50000, 'max': 100000, 'label': '50000-100000', 'color': '#800000'}
    ]

for date in dates:
    num = num_last
    for i in data:
        i[0] = i[0].split("市")[0]
        i[0] = i[0].split("省")[0]
        i[0] = i[0].split("维吾尔自治区")[0]
        i[0] = i[0].split("回族自治区")[0]
        i[0] = i[0].split("壮族自治区")[0]
        i[0] = i[0].split("自治区")[0]
        for line in num:
            if i[1] == date and line[0] == i[0]:
                line[1] = int(i[2])
    m = (
        Map()
        .add(series_name=date, data_pair=num, maptype="china", is_map_symbol_show=False)
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces, pos_top="25%", pos_left="3%"),
        )
    )
    t.add(m, date)
    num_last = list(num)

t.render("citydata.html")

