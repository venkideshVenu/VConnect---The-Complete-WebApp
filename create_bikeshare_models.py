from bikeshare.models import Station, Bike

# Adding stations
def create_stations_and_bikes():
    stations = [
        {"station_name": "MG Road Station", "station_latitude": 12.971598, "station_longitude": 77.594566},
        {"station_name": "Marine Drive Station", "station_latitude": 18.944000, "station_longitude": 72.821000},
        {"station_name": "Connaught Place Station", "station_latitude": 28.631451, "station_longitude": 77.216667},
        {"station_name": "Park Street Station", "station_latitude": 22.553500, "station_longitude": 88.350999},
        {"station_name": "Marina Beach Station", "station_latitude": 13.050000, "station_longitude": 80.282500},
        {"station_name": "Cyber Hub Station", "station_latitude": 28.494847, "station_longitude": 77.088800},
    ]

    for data in stations:
        Station.objects.create(**data)

    # Adding bikes
    bikes = [
        {"name": "Bike 1", "station": Station.objects.get(station_name="MG Road Station"), "in_use": False, "is_faulty": False},
        {"name": "Bike 2", "station": Station.objects.get(station_name="MG Road Station"), "in_use": True, "is_faulty": False},
        {"name": "Bike 3", "station": Station.objects.get(station_name="Marine Drive Station"), "in_use": False, "is_faulty": True},
        {"name": "Bike 4", "station": Station.objects.get(station_name="Marine Drive Station"), "in_use": False, "is_faulty": False},
        {"name": "Bike 5", "station": Station.objects.get(station_name="Connaught Place Station"), "in_use": True, "is_faulty": False},
        {"name": "Bike 6", "station": Station.objects.get(station_name="Park Street Station"), "in_use": False, "is_faulty": False},
        {"name": "Bike 7", "station": Station.objects.get(station_name="Park Street Station"), "in_use": False, "is_faulty": False},
        {"name": "Bike 8", "station": Station.objects.get(station_name="Marina Beach Station"), "in_use": True, "is_faulty": False},
        {"name": "Bike 9", "station": Station.objects.get(station_name="Marina Beach Station"), "in_use": False, "is_faulty": True},
        {"name": "Bike 10", "station": Station.objects.get(station_name="Cyber Hub Station"), "in_use": False, "is_faulty": False},
    ]

    for data in bikes:
        Bike.objects.create(**data)
