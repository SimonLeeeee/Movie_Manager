document.addEventListener("DOMContentLoaded", function () {
    // 获取所有 class 为 'barChart' 的 canvas 元素
    var charts = document.getElementsByClassName("barChart");

    // 循环遍历每个 canvas 元素并绘制柱状图
    for (var i = 0; i < charts.length; i++) {
        var ctx = charts[i].getContext('2d');
        var value = parseFloat(charts[i].getAttribute('data-value'));
        
        // 使用 Chart.js 绘制简单的柱状图
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['票房'],
                datasets: [{
                    label: '票房（亿万元）',
                    data: [value],
                    backgroundColor: 'rgba(0, 100, 0, 0.6)',
                    borderColor: 'rgba(0, 100, 0, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                scales: {
                   xAxis: {  // 修改这里的配置
                        beginAtZero: true,
                        max: 60  // 设置最大值
                    }
                }
            }
        });
    }
});
