
var width = 1200,
    height = 600,
    svg = d3.select('#graph')
        .append('svg')
        .attr({width: width,
               height: height});

var margins = {top: 10,
               right: 40,
               bottom: 100,
               left: 50};

function uniques(data, nick) {
        var uniques = [];

        data.forEach(function (d) {
            if (uniques.indexOf(nick(d)) < 0) {
                uniques.push(nick(d));
            }
        });

        return uniques;
    }

function nick_id (data, nick) {
        var uniques = helpers.uniques(data, nick);

        return d3.scale.ordinal()
            .domain(uniques)
            .range(d3.range(uniques.length));
    }

aaa = {

uniques:function (data, nick) {
        var uniques = [];

        data.forEach(function (d) {
            if (uniques.indexOf(nick(d)) < 0) {
                uniques.push(nick(d));
            }
        });

        return uniques;
    },

nick_id:function (data, nick) {
        var uniques = helpers.uniques(data, nick);

        return d3.scale.ordinal()
            .domain(uniques)
            .range(d3.range(uniques.length));
    }
}
d3.json('/d3/txt/variant_zhuzhuangtu/', function (data) {
    alert(data[0]);
    var nick_id = aaa.nick_id(data, function (d) { return d; });

    var histogram = d3.layout.histogram()
            .bins(nick_id.range())
            .value(function (d) { return nick_id(d); })(data);

    var x = d3.scale.linear()
            .domain([0, d3.max(histogram, function (d) { return d.x; })])
            .range([margins.left, width-margins.right]),
        y = d3.scale.log()
            .domain([1, d3.max(histogram, function (d) { return d.y; })])
            .range([height-margins.bottom, margins.top]);

    var yAxis = d3.svg.axis()
            .scale(y)
            .tickFormat(d3.format('f'))
            .orient('left');

    svg.append('g')
        .classed('axis', true)
        .attr('transform', 'translate(50, 0)')
        .call(yAxis);

    var bar = svg.selectAll('.bar')
            .data(histogram)
            .enter()
            .append('g')
            .classed('bar', true)
            .attr('transform', 
                  function (d) { return 'translate('+x(d.x)+', '+y(d.y)+')'; });

    bar.append('rect')
        .attr({x: 1,
               width: x(histogram[0].dx)-margins.left-1,
               height: function (d) { return height-margins.bottom-y(d.y); }
              });

    bar.append('text')
        .text(function (d) { return d[0]; })
        .attr({transform: function (d) {
                   var bar_height = height-margins.bottom-y(d.y);

                   return 'translate(0, '+(bar_height+7)+') rotate(60)'; }
        });
        
});
