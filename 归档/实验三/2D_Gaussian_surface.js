/**
 * @name        2D_Gaussian_surface.js
 * @author      Fu Ming
 * @Time        2020/10/13 23:49
 * @description 绘制二元正态分布曲面
 */
const echarts = require('echarts');
const echartsGL = require('echarts-gl');
// 基于准备好的dom，初始化echarts实例
const myChart = echarts.init(document.getElementById('main'));

function makeGaussian(amplitude, x0, y0, sigmaX, sigmaY) {
    return function (amplitude, x0, y0, sigmaX, sigmaY, x, y) {
        const exponent = -(
            (Math.pow(x - x0, 2) / (2 * Math.pow(sigmaX, 2)))
            + (Math.pow(y - y0, 2) / (2 * Math.pow(sigmaY, 2)))
        );
        return amplitude * Math.pow(Math.E, exponent);
    }.bind(null, amplitude, x0, y0, sigmaX, sigmaY);
}

// 创建一个高斯分布函数
const gaussian = makeGaussian(50, 0, 0, 20, 20);
const data = [];
// 曲面图要求给入的数据是网格形式按顺序分布。
for (let y = -50; y <= 50; y++) {
    for (let x = -50; x <= 50; x++) {
        const z = gaussian(x, y);
        data.push([x, y, z]);
    }
}
option = {
    grid3D: {},
    xAxis3D: {},
    yAxis3D: {},
    zAxis3D: {max: 60},
    series: [{
        type: 'surface',
        data: data
    }]
}
myChart.setOption(option);
