from db_connection.connection import BaseDBView, fdb


class WeatherCity(BaseDBView):
     def get_all(self):
         self.connector.cursor.execute('''
            SELECT * FROM CITIES
        ''')
         result = self.connector.cursor.fetchallmap()
         self.connector.cursor.close()
         return result

class Weather(BaseDBView):
    def get_all(self):
        self.connector.cursor.execute('''
                     select 
            weather.id,
            cities.city_name,
            weather.avg_temp,
            weather.forecast_date,
            weather.avg_pressure,
            weather.avg_rainfall
         from weather, cities
        ''')
        result = self.connector.cursor.fetchallmap()
        self.connector.cursor.close()
        return result

    def get_by_id(self, w_id):
        self.connector.cursor.execute('''
    SELECT * FROM WEATHER
     WHERE id = ?
    ''', (w_id,))
        result = self.connector.cursor.fetchonemap()
        self.connector.cursor.close()
        return result
    def create (self, city_id, forecast_date, avg_temp, avg_pressure, avg_rainfall):
     try:
        print(city_id, forecast_date, avg_temp, avg_pressure, avg_rainfall)
        self.connector.cursor.execute('''
     INSERT INTO WEATHER (CITY_ID, FORECAST_DATE, AVG_TEMP, AVG_PRESSURE, AVG_RAINFALL) VALUES(?,?,?,?,?)
    ''', (city_id, forecast_date, avg_temp, avg_pressure, avg_rainfall))
        self.connector.dataset.commit()
        return True
     except fdb.Error as e:
        print(e)
        self.connector.dataset.rollback()

    def update(self, city_id, forecast_date, avg_temp, avg_pressure,
    avg_rainfall, id):
     try:
        self.connector.cursor.execute('''
     UPDATE WEATHER SET CITY_ID = ?, FORECAST_DATE = ?, AVG_TEMP = ?, AVG_PRESSURE = ?, AVG_RAINFALL = ?
     WHERE ID = ?
     ''', (city_id, forecast_date,
    avg_temp, avg_pressure, avg_rainfall, id))
        self.connector.dataset.commit()
        return True
     except fdb.Error as e:
        self.connector.dataset.rollback()

    def delete(self, id):
     try:
    #Спасибо Дмитрий Сергеевич
        self.connector.cursor.execute("DELETE FROM weather WHERE ID=?", (id,))
        self.connector.dataset.commit()
        return True
     except fdb.Error as e:
        self.connector.dataset.rollback()
