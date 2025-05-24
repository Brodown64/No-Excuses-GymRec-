import folium
import requests

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

bbox = [40.70, -74.02, 40.78, -73.95]

query = f"""
[out:json];
(
  node["amenity"="gym"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["amenity"="gym"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  relation["amenity"="gym"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});


  node["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  relation["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
);
out center;
"""

response = requests.post(OVERPASS_URL, data={"data": query})
data = response.json()

map_center = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
m = folium.Map(location=map_center, zoom_start=14)

for element in data['elements']:
    # Get coordinates
    if 'lat' in element and 'lon' in element:
        lat = element['lat']
        lon = element['lon']
    elif 'center' in element:
        lat = element['center']['lat']
        lon = element['center']['lon']
    else:
        continue

    name = element['tags'].get('name', 'Unnamed Gym')
    folium.Marker(
    	location=[lat, lon],
    	popup=name,
    	tooltip=name,
    	icon=folium.Icon(color="red", icon="dumbbell", prefix="fa")
    ).add_to(m)

m.save("osm_gyms_map.html")
print("Map saved as 'osm_gyms_map.html'")