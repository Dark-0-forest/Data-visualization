/**
 * @name        spherical.js
 * @author      Fu Ming
 * @Time        2020/10/13 23:29
 * @description 绘制球面（半径为5）
 */
const echarts = require('echarts');
const echartsGL = require('echarts-gl');
// 基于准备好的dom，初始化echarts实例
const myChart = echarts.init(document.getElementById('main'));
option = {
    tooltip: {},
    visualMap: {
        show: false,
        dimension: 2,
        min: -1,
        max: 1,
        inRange: {
            color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        }
    },
    xAxis3D: {},
    yAxis3D: {},
    zAxis3D: {},
    grid3D: {},
    series: [{
        type: 'surface',
        parametric: true,
        // shading: 'albedo',
        parametricEquation: {
            u: {
                min: -Math.PI,
                max: Math.PI,
                step: Math.PI / 20
            },
            v: {
                min: 0,
                max: Math.PI,
                step: Math.PI / 20
            },
            x: function (u, v) {
                return 5 * Math.sin(v) * Math.sin(u);
            },
            y: function (u, v) {
                return 5 * Math.sin(v) * Math.cos(u);
            },
            z: function (u, v) {
                return 5 * Math.cos(v);
            }
        }
    }]
};
myChart.setOption(option);
