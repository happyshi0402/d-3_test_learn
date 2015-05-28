
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

d3.json('/d3/json/learn5/', function (data) {

    data = d3.keys(data).map(function (key) {
        return {bucket: String(key),
                N: data[key]};
    });

   // x.domain(data.map(function (d) { return d.bucket; }));
    //y.domain([0, d3.max(data, function (d) { return d.N })]);

    x.domain([0,d3.max(data, function (d) { return d.N })]);
    y.domain(data.map(function (d) { return d.bucket; }));

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0, "+(height-pad)+")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate("+(left_pad-pad)+", 0)")
        .call(yAxis);

    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', -width)
        .transition()
        //.delay(function (d) { return d.N*20; })
        .duration(800)
        .attr('x', function (d) { return x(
           0
         ); })
        .attr('width',  function (d) { return  x(d.N) } )
        .attr('y', function (d) { return y(d.bucket); })
        .attr('height',  y.rangeBand());
});
