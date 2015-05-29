from flask import Flask,render_template,redirect,url_for,flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET FOR JIYUN STRING'
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()
csrf.init_app(app)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("/index.html")

@app.route('/svg/test1/')
def svg_test1():
    return render_template("/svg/test1.html")

@app.route('/svg/test2/')
def svg_test2():
    return render_template("/svg/test2.html")

@app.route('/svg/test3/')
def svg_test3():
    return render_template("/svg/test3.html")

@app.route('/svg/test4/')
def svg_test4():
    return render_template("/svg/test4.html")

@app.route('/svg/test5/')
def svg_test5():
    return render_template("/svg/test5.html")

@app.route('/svg/test6/')
def svg_test6():
    return render_template("/svg/test6.html")

@app.route('/d3/learn1/')
def d3_learn1():
    return render_template("/d3_learn1/d3_learn1.html")

@app.route('/d3/learn2/')
def d3_learn2():
    return render_template("/d3_learn1/d3_learn2.html")

@app.route('/d3/learn3/')
def d3_learn3():
    return render_template("/d3_learn1/d3_learn3.html")

@app.route('/d3/learn4/')
def d3_learn4():
    return render_template("/d3_learn1/d3_learn4.html")

@app.route('/d3/learn5/')
def d3_learn5():
    return render_template("/d3_learn1/d3_learn5.html")

@app.route('/d3/json/learn5/')
def d3_learn5_json():
    return render_template("/d3_learn1/d3_learn5_json.json")

@app.route('/d3/learn6/')
def d3_learn6():
    return render_template("/d3_learn1/d3_learn6.html")

@app.route('/d3/learn7/')
def d3_learn7():
    return render_template("/d3_learn1/d3_learn7.html")

@app.route('/d3/learn8/')
def d3_learn8():
    return render_template("/d3_learn1/d3_learn8.html")

@app.route('/d3/prograssbar/')
def d3_prograssbar():
    return render_template("/d3_learn1/prograssbar.html")

@app.route('/d3/prograssbar/run/')
def d3_prograssbar_run():
    return render_template("/d3_learn1/prograssbar.json")

@app.route('/d3/relitu/')
def d3_relitu():
    return render_template("/d3_learn1/relitu.html")

@app.route('/histogram/')
def histogram():
    return render_template("/ch1/histogram.html")

@app.route('/histogram/json/')
def histogram_json():
    return render_template("/ch1/histogram-hours.json")

@app.route('/axes/')
def axes():
    return render_template("/ch2/axes.html")

@app.route('/colours/')
def colours():
    return render_template("/ch2/colours.html")

@app.route('/css/')
def css():
    return render_template("/ch2/css.html")

@app.route('/drwho/')
def drwho():
    return render_template("/ch2/drwho.html")

@app.route('/drwho/csv/')
def drwho_csv():
    return render_template("/ch2/villains.csv")

@app.route('/html/')
def html():
    return render_template("/ch2/html.html")


@app.route('/paths/')
def paths():
    return render_template("/ch2/paths.html")

@app.route('/svg/')
def svg():
    return render_template("/ch2/svg.html")

@app.route('/table/')
def table():
    return render_template("/ch2/table.html")

@app.route('/ch3/arrays/')
def ch3_arrays():
    return render_template("/ch3/arrays.html")

@app.route('/ch3/arrays/txt/primes-to-100k/')
def ch3_arrays_txt():
    return render_template("/ch3/primes-to-100k.txt")

@app.route('/ch3/geography/')
def ch3_geography():
    return render_template("/ch3/geography.html")

@app.route('/ch3/geography/water/')
def ch3_geography_data_water():
    return render_template("/ch3/data/water.json")

@app.route('/ch3/geography/land/')
def ch3_geography_data_land():
    return render_template("/ch3/data/land.json")

@app.route('/ch3/geography/cultural/')
def ch3_geography_data_cultural():
    return render_template("/ch3/data/cultural.json")

@app.route('/ch3/geography/airports/')
def ch3_geography_data_airports():
    return render_template("/ch3/data/airports.dat")

@app.route('/ch3/geography/routes/')
def ch3_geography_data_routes():
    return render_template("/ch3/data/routes.dat")

@app.route('/ch3/ordinal_scales/')
def ch3_ordinal_scales():
    return render_template("/ch3/ordinal_scales.html")

@app.route('/ch3/quantitative_scales/')
def ch3_quantitative_scales():
    return render_template("/ch3/quantitative_scales.html")


@app.route('/ch4/brushes/')
def ch4_brushes():
    return render_template("/ch4/brushes.html")


@app.route('/ch4/drag/')
def ch4_drag():
    return render_template("/ch4/drag.html")


@app.route('/ch4/drag/png/parallax_base/')
def ch4_drag_png_parallax_base():
    return render_template("/ch4/parallax_base.png")

@app.route('/ch4/easing/')
def ch4_easing():
    return render_template("/ch4/easing.html")

@app.route('/ch4/events/')
def ch4_events():
    return render_template("/ch4/events.html")

@app.route('/ch4/timers/')
def ch4_timers():
    return render_template("/ch4/timers.html")

@app.route('/ch4/zoom/')
def ch4_zoom():
    return render_template("/ch4/zoom.html")

@app.route('/ch5/chord/')
def ch5_chord():
    return render_template("/ch5/chord.html")

@app.route('/ch5/cluster/')
def ch5_cluster():
    return render_template("/ch5/cluster.html")

@app.route('/ch5/force/')
def ch5_force():
    return render_template("/ch5/force.html")

@app.route('/ch5/histogram/')
def ch5_histogram():
    return render_template("/ch5/histogram.html")

@app.route('/ch5/pack/')
def ch5_pack():
    return render_template("/ch5/pack.html")

@app.route('/ch5/partition/')
def ch5_partition():
    return render_template("/ch5/partition.html")

@app.route('/ch5/pie/')
def ch5_pie():
    return render_template("/ch5/pie.html")

@app.route('/ch5/stack/')
def ch5_stack():
    return render_template("/ch5/stack.html")

@app.route('/ch5/tree/')
def ch5_tree():
    return render_template("/ch5/tree.html")

@app.route('/ch5/treemap/')
def ch5_treemap():
    return render_template("/ch5/treemap.html")

@app.route('/ch5/treemap/json/karma_matrix/')
def ch5_treemap_json():
    return render_template("/ch5/data/karma_matrix.json")

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True, debug=True, port=6005)

