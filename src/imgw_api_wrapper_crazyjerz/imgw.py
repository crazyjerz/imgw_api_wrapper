from requests import Session
from datetime import datetime, timedelta
from enum import Enum

DIRECTIONS = {0: 'N', 90: 'E', 180: 'S', 270: 'W', 360: 'N'}

# SCENE/INCA unavailable - for now, undocumented API
class Model(Enum):
    AROME = 1
    WRF = 2
    COSMO2K8 = 3
    ALARO = 4
    COSMO7K0 = 5
    GFS = 6


class IMGWObject(dict):
    def __init__(self, wind_dir: int, temperature: float, surface_temperature: float, dewpoint_temperature: float,
                 snow: float, wind_speed: float, pressure: int, date: str, rain: float, cloud: int, humidity: int):
        super().__init__()
        self['wind_direction'] = wind_dir
        self['temperature'] = round(temperature - 273.15, 2)
        self['surface_temperature'] = round(surface_temperature - 273.15, 2)
        self['dewpoint_temperature'] = round(dewpoint_temperature - 273.15, 2)
        self['snow'] = snow
        self['wind_speed'] = wind_speed
        self['pressure'] = pressure
        self['date'] = datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]), int(date[17:19]))
        self['rain'] = rain
        self['cloud'] = cloud
        self['humidity'] = humidity

    def get_general_wind_direction(self) -> str:
        val = int((self['wind_direction'] / 22.5) + 0.5)  # code shamelessly stolen from stack overflow
        arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return arr[(val%16)]

    def get_total_precipitation(self) -> float:
        return self['snow']+self['rain']


class IMGWData:
    def __init__(self, data):
        self.location: tuple[float, float] = float(data['Location']['Lat']), float(data['Location']['Lon'])
        if data['Teryt']['County'] == '':
            self.teryt: int = 0
        else:
            self.teryt: int = int(data['Teryt']['County'])
        self.model: str = data['Model']
        self.data: list[IMGWObject] = []
        for i in data['Data']:
            self.data.append(IMGWObject(
                int(i['Wind_Dir']), float(i['Temperature']), float(i['Temperature_Surface']),
                float(i['Dewpoint_Temperature']), float(i['Snow']), float(i['Wind_Gust']), int(i['Pressure']),
                i['Date'], float(i['Rain']), int(i['Cloud']), int(i['Humidity'])))

    def get_info(self, date: datetime = datetime.now()) -> IMGWObject:
        best_difference = timedelta(days=365)
        best_index = 0
        for i in range(len(self.data)):
            current_difference: timedelta = abs(self.data[i]['date'] - date)
            if current_difference < best_difference:
                best_difference = current_difference
                best_index = i
        return self.data[best_index]


class IMGW(Session):
    def __init__(self):
        super().__init__()

    # most of the link's contents are undocumented, can result in unexpected behaviour
    def get_data(self, latitude: float, longitude: float, forecast_type: Model) -> IMGWData:
        url = f"https://forecastapi.imgw.pl/get?lat={latitude}&lon={longitude}&z=0&m={forecast_type.name.lower()}" \
              f"&lasttime=0&p=mobile&t=cf91c88878cda27ceria76da208a06aeb9"
        data = self.get(url).json()
        if str(data) == '{}':
            raise LookupError("Position not available.")
        return IMGWData(data)

