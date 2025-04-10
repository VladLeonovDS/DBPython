from flask import render_template
from .models import Weather, WeatherCity
from flask import request, redirect, url_for
from datetime import datetime
def init_routes(app):
    @app.route('/')
    @app.route('/index')
    def index():
        param = Weather().get_all()
        city_list = WeatherCity().get_all()
        date_now = datetime.now().date()
        return render_template('index.html', weather_list=param,
                               city_list = city_list,
                               date_now = date_now)

    @app.route('/create_record', methods=["POST"])
    def create_record():
        city_id = request.form.get('city')
        forecast_date = datetime.strptime(request.form.get('forecast_date'), "%Y-%m-%d")
        avg_temp = request.form.get('avg_temp')
        avg_pressure = request.form.get('avg_pressure')
        avg_rainfall = request.form.get('avg_rainfall')
        Weather().create(city_id, forecast_date.date(), avg_temp, avg_pressure, avg_rainfall)
        return redirect(url_for('index'))
    @app.route('/record_detail/<int:w_id>', methods=["GET"])
    def record_detail(w_id):
        record = Weather().get_by_id(w_id)
        city_list = WeatherCity().get_all()
        return render_template('update-record.html', record=record, city_list=city_list)

    @app.route('/update_record', methods=["POST"])
    def update_record():
        id = request.form.get('id')
        city_id = request.form.get('city')
        forecast_date = datetime.strptime(request.form.get('forecast_date'), "%Y-%m-%d")
        avg_temp = request.form.get('avg_temp')
        avg_pressure = request.form.get('avg_pressure')
        avg_rainfall = request.form.get('avg_rainfall')
        Weather().update(city_id, forecast_date.date(), avg_temp, avg_pressure, avg_rainfall, id)
        return redirect(url_for('record_detail',w_id=id))

    @app.route('/delete_record', methods=["POST"])
    def delete_record():
        id = request.form.get('id')
        Weather().delete(id)
        return redirect(url_for('index'))