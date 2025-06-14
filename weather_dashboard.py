import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import dateparser


# Your OpenWeatherMap API key
API_KEY = '86055c3f5c9c6a6b1e6e163c63ee7891'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'


# Fetch weather forecast data
def fetch_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()


    if response.status_code != 200 or "list" not in data:
        print("❌ Failed to fetch data:", data.get("message", "Unknown error"))
        return [], [], [], city


    forecast_data = data['list']
    times, temps, humidity = [], [], []


    for entry in forecast_data:
        time = datetime.datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        hum = entry['main']['humidity']


        times.append(time)
        temps.append(temp)
        humidity.append(hum)


    return times, temps, humidity, data['city']['name']


# Filter forecast by user-specified date
def filter_by_date(times, temps, humidity, target_date):
    parsed_date = dateparser.parse(target_date)
   
    if parsed_date is None:
        print(f"❌ Could not understand the date '{target_date}'. Try 'today', 'tomorrow', or 'YYYY-MM-DD'.")
        return [], [], []


    target = parsed_date.date()
    f_times, f_temps, f_humidity = [], [], []


    for t, temp, hum in zip(times, temps, humidity):
        if t.date() == target:
            f_times.append(t)
            f_temps.append(temp)
            f_humidity.append(hum)


    return f_times, f_temps, f_humidity


# Visualize the temperature and humidity
def plot_weather(times, temps, humidity, city, date_label):
    if not times:
        print(f"⚠️  No forecast data available for '{date_label}'.")
        return


    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")


    # Temperature Plot
    plt.subplot(2, 1, 1)
    sns.lineplot(x=times, y=temps, marker='o', color='tomato')
    plt.title(f'Temperature Forecast for {city} on {date_label}', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')


    # Humidity Plot
    plt.subplot(2, 1, 2)
    sns.lineplot(x=times, y=humidity, marker='s', color='skyblue')
    plt.title(f'Humidity Forecast for {city} on {date_label}', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel('Humidity (%)')


    plt.tight_layout()
    plt.show()


# Main driver function
def main():
    print("🌦️  Weather Forecast Dashboard (next 5 days)")
    city = input("Enter City Name (e.g., Mumbai): ")
    date_input = input("Enter date (e.g., 'today', 'tomorrow', '2025-05-27'): ")


    times, temps, humidity, real_city = fetch_weather_data(city)
    if not times:
        return


    f_times, f_temps, f_humidity = filter_by_date(times, temps, humidity, date_input)
    if not f_times:
        print("⚠️  No data to display. Please check your date input and try again.")
        return


    plot_weather(f_times, f_temps, f_humidity, real_city, date_input)


if __name__ == '__main__':
    main()
exit
