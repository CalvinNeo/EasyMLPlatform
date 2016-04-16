function getDataSource(cpuData, memoryData, cpuMax, memMax, url, index) {
    return function() {
        $.ajax({
            type: 'POST',
            url: url + "/v1/node/query",
            data: {
                id: index
            },
            success: function(d) {
                while (cpuData.length < cpuMax) {
                    cpuData.push(-1);
                }

                while (memoryData.length < memMax) {
                    memoryData.push(-1);
                }

                if (cpuData.length) {
                    cpuData = cpuData.slice(1);
                }

                if (memoryData.length) {
                    memoryData = memoryData.slice(1);
                }

                cpuData.push(d.Cpu);
                memoryData.push(d.Memory);
            },
            dataType: "json",
            async: false
        });

        var cpuRes = [];
        var memRes = [];
        for (var i = 0; i < cpuData.length; ++i) {
            cpuRes.push([i, cpuData[i]])
        }
        for (var i = 0; i < memoryData.length; ++i) {
            memRes.push([i, memoryData[i]])
        }
        return { Cpu: cpuRes, Mem: memRes };
    };
}

function startMointor(cpuId, memoryId, ip, index) {
    var cpuContainer = $("#" + cpuId);
    var memoryContainer = $("#" + memoryId);

    var cpuMax = cpuContainer.outerWidth() / 2 || 300;
    var memMax = memoryContainer.outerWidth() / 2 || 300;

    var cpuData = [];
    var memData = [];

    var dataSource = getDataSource(cpuData, memData, cpuMax, memMax, "http://" + ip, index);

    var dd = dataSource();

    cpuSeries = [{
        data: dd.Cpu,
        lines: {
            fill: true
        }
    }];
    memSeries = [{
        data: dd.Mem,
        lines: {
            fill: true
        }
    }];

    var cpuPlot = $.plot(cpuContainer, cpuSeries, {
        grid: {
            color: "#999999",
            tickColor: "#D4D4D4",
            borderWidth: 0,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#ffffff", "#ffffff"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "#fff"
                    });
                }
                return markings;
            }
        },
        colors: ["#1ab394"],
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 0,
            max: 100
        },
        legend: {
            show: true
        }
    });

    var memPlot = $.plot(memoryContainer, memSeries, {
        grid: {
            color: "#999999",
            tickColor: "#D4D4D4",
            borderWidth: 0,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#ffffff", "#ffffff"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "#fff"
                    });
                }
                return markings;
            }
        },
        colors: ["#1ab394"],
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 0,
            max: 1024 * 1024 * 32
        },
        legend: {
            show: true
        }
    });

    return setInterval(function updateDataSource() {
        dd = dataSource();

        cpuSeries[0].data = dd.Cpu;
        cpuPlot.setData(cpuSeries);
        cpuPlot.draw();

        memSeries[0].data = dd.Mem;
        memPlot.setData(memSeries);
        memPlot.draw();
    }, 500);
}


var timerId = 0;

$(function() {
    // timerId = startMointor("flot-line-chart-cpu", "flot-line-chart-memory", "localhost:8190", 4);
    //console.log(timerId);
    //setTimeout(function() {
    //    clearInterval(timerId);
    //}, 5000)
});
var ad = new Array();
$.ajax({
    type: 'POST',
    url: "http://localhost:8190" + "/v1/node/query/list",
    success: function(d) {
        for (var i=0; i<d.Objects.length; i++)
        {
            ad.push(d.Objects[i].Id)
            cloned = $("#prototype > .container").clone()
            cloned.find("#flot-line-chart-cpu").attr("id", "flot-line-chart-cpu-" + d.Objects[i].Id)
            cloned.find("#flot-line-chart-memory").attr("id", "flot-line-chart-memory-" + d.Objects[i].Id)
            cloned.find(".cpuname").text("Node " + d.Objects[i].Id + " CPU")
            cloned.find(".memname").text("Node " + d.Objects[i].Id + " Memory")
            $("#conlist").append(cloned)
            // startMointor("flot-line-chart-cpu-" + d.Objects[i].Id, "flot-line-chart-memory-" + d.Objects[i].Id, "localhost:8190", d.Objects[i].Id);
        }
    },
    dataType: "json",
    async: false
});
$(document).ready(function(){
    for (var i=0; i<ad.length; i++)
    {
        startMointor("flot-line-chart-cpu-" + ad[i], "flot-line-chart-memory-" + ad[i], "localhost:8190", ad[i]);
    }
})
