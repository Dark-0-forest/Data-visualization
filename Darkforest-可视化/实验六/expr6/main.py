import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph, Tree, Tab, WordCloud, Timeline

tab = Tab()

df = pd.read_excel("email_dev_inside.xlsx")
nodes = []
links = []

# 获取连接关系
for line in df.value_counts().index:
    link = {'source': line[6][:4], 'target': line[7][:4]}
    links.append(link)

# 获取节点
for index in df["from"].value_counts().index:
    node = {
        "name": index[:4],
        "symbolSize": 3,
        "value": 1,
        "draggable": "False",
        "category": ""
    }
    nodes.append(node)

# 画出关系图
graph = (
    Graph(init_opts=opts.InitOpts(width="1200px", height="700px"))
    .add(
        series_name="",
        nodes=nodes,
        links=links,
        is_draggable=True,
        repulsion=50,
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False),
    )
)
tab.add(graph, "研发部门人员关系图")

# 由画出的graph图中可知，其中有三个部门，这三部门的负责人为1007, 1059, 1068
head = ["1007", "1059", "1068"]
head_second = []
head_third = []

# 获取第二负责人
for head1 in head:
    head_2 = []
    for link in links:
        if link['source'] == head1:
            if link['target'] not in head_2:
                head_2.append(link['target'])
    head_second.append(head_2)

# 获取第三负责人
for head1 in head_second:
    head_3 = []
    for head2 in head1:
        head_3_2 = []
        for link in links:
            if link['source'] == head2:
                if link['target'] not in head_3_2:
                    head_3_2.append(link['target'])
        head_3.append(head_3_2)
    head_third.append(head_3)

# 由负责人关系，生成对应的树形图
tree = {"name": "root"}
children = []
for i in range(0, 3):
    head1 = {"name": head[i]}
    children1 = []
    for j in head_second[i]:
        head2 = {"name": j}
        children2 = []
        for k in head_third[i][head_second[i].index(j)]:
            head3 = {"name": k, "values": 1}
            children2.append(head3)
        head2["children"] = children2
        children1.append(head2)
    head1["children"] = children1
    children.append(head1)
tree["children"] = children

# 画出树形图
tree = (
    Tree(init_opts=opts.InitOpts(width="1500px", height="900px"))
    .add(
        "",
        [tree],
        collapse_interval=2,
        orient="TB",
        initial_tree_depth=-1,
        label_opts=opts.LabelOpts(
            font_size=10,
            position="top",
            horizontal_align="right",
            vertical_align="middle",
            rotate=-90,
        ),
    )
)
tab.add(tree, "研究部门层级关系树图")

# 生成词云数据
cloudword = []
for i in range(0, 3):
    for j in head_third[i]:
        word = {}
        words = []
        person = j
        person.append(head_second[i][head_third[i].index(j)])
        for line in df.value_counts().index:
            if line[6][:4] in person:
                if line[8] in word:
                    word[line[8]] += 1
                else:
                    word[line[8]] = 1
        for k in word.keys():
            words.append((k, word[k]))
        cloudword.append(words)
timeline = Timeline(init_opts=opts.InitOpts(width="1500px", height="550px"))
for i in range(0, 30):
    cw = (
        WordCloud()
        .add("", cloudword[i], word_size_range=[12, 55]))
    timeline.add(cw, "第{}部门".format(i))

tab.add(timeline, "部门主题词云图")
tab.render()

