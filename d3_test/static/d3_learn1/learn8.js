
function makeData(n){
    var arr = [];
    for (var i=0; i<n; i++){
        arr.push({
            x:Math.floor((Math.random() * 100) + 1),
            y:Math.floor((Math.random() * 100) + 1),
            width:Math.floor((Math.random() * 100) + 1),
            height:Math.floor((Math.random() * 100) + 1)
        });
    }
    return arr;
}

function new_arr_data(data,nick){
    var uniques = [];

    data.forEach(function (d) {
        //if (uniques.indexOf(nick(d)) < 0) {
        //    uniques.push(nick(d));
        //}
        var rect_width = nick(d);
        var size = 10;
        var num_rec = 0;
        var las_width = 0;
        if(rect_width > 0){
             num_rec = rect_width / (size+1);
             las_width = rect_width % (size+1);
        }

        for(var i=0;i < num_rec; i++){
             uniques.push({
                 x:Math.floor(i * size + 1),
                 y:Math.floor(rect_y  + 1),
                 width:Math.floor(size+ 1),
                 height:Math.floor(size + 1)
             });
        }

        if(las_width > 0){
             uniques.push({
                 x:Math.floor(num_rec * las_width + 1),
                 y:Math.floor(rect_y  + 1),
                 width:Math.floor(las_width+ 1),
                 height:Math.floor(las_width + 1)
             });
        }

    });

    return uniques;
}



var rectangles = function(svg) {
    var data = makeData(2);
    var rect = svg.selectAll('#rect').data(data);
    // Enter
    rect.enter().append('rect')
        .attr("class", "my_rect")
        .attr('test', function (d, i) {
            // Enter called 2 times only
            console.log('enter placing initial rectangle: ', i)
        });
    // Update
    rect.transition().duration(500).attr('x', function (d) {
        return d.x;
    })
        .attr('y', function (d) {
            return d.y;
        })
        .attr('width', function (d) {
            return d.width;
        })
        .attr('height', function (d) {
            return d.height;
        })
        .attr('test', function (d, i) {
            // update every data change
            console.log('updating x position to: ', d.x)
        });
};
var width = 900,
    height = 300,
    pad = 20,
    left_pad = 100;

//var x = d3.scale.ordinal().rangeRoundBands([left_pad, width-pad], 0.1);  //100  880  0.1
//var y = d3.scale.linear().range([height-pad, pad]);  // 280,20
var x = d3.scale.linear().range([left_pad,width]);  //100  880  0.1
var y = d3.scale.ordinal().rangeRoundBands([ pad,height-pad], 0.1);  // 280,20

var xAxis = d3.svg.axis().scale(x).orient("bottom");
var yAxis = d3.svg.axis().scale(y).orient("left");

var svg = d3.select("#graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

//根据柱形图的高度，对此进行划分成n个小的正方形进行显示
function makeData2(arr,rect_y,rect_width,size){
    //var arr = [];
    var num_rec = rect_width / (size+1);
    var las_width = rect_width % (size+1);

    for (var i=0; i<num_rec; i++){
        arr.push({
            x:Math.floor(i * size + 1),
            y:Math.floor(rect_y  + 1),
            width:Math.floor(size+ 1),
            height:Math.floor(size + 1)
        });
    }
    if(las_width > 0){
        arr.push({
            x:Math.floor(i * size + 1),
            y:Math.floor(las_width  + 1),
            width:Math.floor(size+ 1),
            height:Math.floor(size + 1)
        });
    }
    return arr;
}

d3.json('/d3/json/learn5/', function (data) {

    var data2 = [];
    data = d3.keys(data).map(function (key) {
         makeData2(data2,String(key),data[key],5);
        return {bucket: String(key),
                N: data[key]};
    });

    alert(data2.length);

    y = d3.scale.ordinal().domain(eases).rangeBands([50, 500]);
    // x.domain(data.map(function (d) { return d.bucket; }));
    // y.domain([0, d3.max(data, function (d) { return d.N })]);

    x.domain([0,d3.max(data, function (d) {
        return d.N })]);

    y.domain(data.map(function (d) { return d.bucket; }));

    var x_svg = svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0, "+(height-pad)+")")
        .call(xAxis);

    var y_svg = svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate("+(left_pad-pad)+", 0)")
        .call(yAxis);

    //makeData2(d.bucket, d.N,5)

    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', function(d){
            //根据值的不同设置不同的样式
            //alert(d.N);
            var age = d.N;
            if(age > 50){
                return 'bar';
            } else {
                return 'bar2'
            }
        })
        .attr('x', -width)        //柱形图移动从哪里开始
        .transition()
        //.delay(function (d) { return d.N*20; })
        .duration(800)
        .attr('x', function (d) { return x(
            0
        ); })
        .attr('width',  function (d) { return  x(d.N) - 100 } )
        .attr('id',  function (d) { return  'bar'+parseInt(x(d.N)/((width - pad)/ 150)) } )
        .attr('y', function (d) { return y(d.bucket); })
        .attr('height',  y.rangeBand());
    });
