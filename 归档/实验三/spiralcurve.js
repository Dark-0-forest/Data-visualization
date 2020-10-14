/**
 * @name        spiralcurve.js
 * @author      Fu Ming
 * @Time        2020/10/13 23:10
 * @description 绘制螺旋曲线（半径为5，每旋转一周z坐标增加π）
 */
const echarts = require('echarts');
const echartsGL = require('echarts-gl');
// 基于准备好的dom，初始化echarts实例
const myChart = echarts.init(document.getElementById('main'));

// r为螺旋线半径 k为比例因子 k*w为角速度
function spiral(r, k, w) {
    return [r * Math.cos(k * w), r * Math.sin(k * w), k * w]
}

const data = [];
for (let w = 0; w < 30 * Math.PI; w += 0.1)
    data.push(spiral(5, 0.5, w));//构造一个半径为5，每转一周高度增加π的螺旋线
option = {
    grid3D: {},
    xAxis3D: {},
    yAxis3D: {},
    zAxis3D: {max: 60},
    series: [{
        type: 'line3D',
        data: data,
    }]
}
myChart.setOption(option);
