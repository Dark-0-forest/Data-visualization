/**
 * @name        app.js
 * @author      Fu Ming
 * @Time        2020/10/13 18:49
 * @description 数据可视化实验一：Echarts.js使用示例
 */
var echarts = require('echarts');

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));
// 绘制图表
myChart.setOption({
    title: {
        text: '数据可视化实验一\n'
            + '付铭-18030400010'
    },
    tooltip: {},
    xAxis: {
        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    },
    yAxis: {},
    series: [{
        name: '销量',
        type: 'bar',
        data: [15, 20, 36, 10, 10, 20]
    }]
});