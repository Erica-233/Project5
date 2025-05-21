import requests
import configparser
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

class WeatherFetcher:
    API_BASE = "http://api.openweathermap.org/data/2.5/weather"
    FORECAST_API = "http://api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key):
        self.api_key = api_key
        self.history = []

    def _get_data(self, url, params):
        params['appid'] = self.api_key
        params['units'] = 'metric'
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_current_weather(self, city):
        params = {'q': city}
        data = self._get_data(self.API_BASE, params)
        record = {
            'city': data['name'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'condition': data['weather'][0]['main'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.history.append(record)
        return record

    def get_forecast(self, city):
        params = {'q': city}
        data = self._get_data(self.FORECAST_API, params)
        return [
            {
                'datetime': item['dt_txt'],
                'temp': item['main']['temp'],
                'condition': item['weather'][0]['main']
            }
            for item in data['list'][:8]  # 未来24小时预报（每3小时一条）
        ]

class WeatherVisualizer:
    @staticmethod
    def plot_temperature_comparison(cities_data):
        df = pd.DataFrame(cities_data)
        plt.figure(figsize=(10, 6))
        plt.bar(df['city'], df['temp'], color='skyblue')
        plt.title('Temperature Comparison')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_forecast(forecast_data):
        df = pd.DataFrame(forecast_data)
        df['datetime'] = pd.to_datetime(df['datetime'])
        plt.figure(figsize=(12, 6))
        plt.plot(df['datetime'], df['temp'], marker='o', linestyle='--')
        plt.title('24-hour Temperature Forecast')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

class WeatherApp:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_key = config['DEFAULT']['API_KEY']
        self.fetcher = WeatherFetcher(self.api_key)
        self.visualizer = WeatherVisualizer()

    def run(self):
        while True:
            print("\n1. 查询城市天气")
            print("2. 多城市温度对比")
            print("3. 查看天气预报")
            print("4. 显示查询历史")
            print("5. 退出")

            choice = input("请选择操作: ")

            if choice == '1':
                city = input("输入城市名: ")
                data = self.fetcher.get_current_weather(city)
                print(f"\n当前天气 ({data['city']}):")
                print(f"温度: {data['temp']}°C")
                print(f"湿度: {data['humidity']}%")
                print(f"天气状况: {data['condition']}")

            elif choice == '2':
                cities = input("输入对比城市（用逗号分隔）: ").split(',')
                comparison_data = []
                for city in cities:
                    data = self.fetcher.get_current_weather(city.strip())
                    comparison_data.append(data)
                self.visualizer.plot_temperature_comparison(comparison_data)

            elif choice == '3':
                city = input("输入城市名: ")
                forecast = self.fetcher.get_forecast(city)
                print("\n未来24小时预报:")
                print(tabulate(forecast, headers="keys", tablefmt="grid"))
                self.visualizer.plot_forecast(forecast)

            elif choice == '4':
                print("\n查询历史:")
                print(tabulate(self.fetcher.history, headers="keys", tablefmt="grid"))

            elif choice == '5':
                print("再见！")
                break

            else:
                print("无效输入，请重试")

if __name__ == "__main__":
    try:
        app = WeatherApp()
        app.run()
    except requests.exceptions.HTTPError as e:
        print(f"API请求失败: {str(e)}")
    except KeyError:
        print("配置文件错误，请检查config.ini")