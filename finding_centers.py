

import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance

print("Used to find the nearest center.")
print("1. Need 2 files: one for student city details, and second is for center city details.")
print("2. Both files must be in same folder.")
print("3. Column names must be student_cities & center_cities in respective file")
print("4. Excel files doesn't contain any empty values.")
print("5. Output will be 2 excel: one describe entire dataset with nearest center & second file describe city location that fail to match.")

student_file_name = input("Enter Student Details File Name in 'file_name.xlsx' format: ")
center_file_name = input("Enter Center Details File Name in 'file_name.xlsx' format: ")

try:
  st_city = pd.read_excel(student_file_name)
  center_city = pd.read_excel(center_file_name)
except:
  print("File is Not Found, or error while reading the file.")
  print("Please give correct name & Rerun.")

try:
  def find_latitude_longitude(city_list):
    i=0
    location_list = []
    for city in city_list:
      try: 
        locator = Nominatim(user_agent='myGeocoder')
        city = city + ", India"
        location = locator.geocode(city)
        location_list.append((location.latitude, location.longitude))

      except:
        location_list.append(("NoneType", city))

      i+=1
      if (i%20==0):
        print("processing...")
    return location_list


  st_city["location"] = find_latitude_longitude(st_city.student_cities)
  center_city["location"] = find_latitude_longitude(center_city.center_cities)

  def find_nearest_center(student_df, center_df):
    st_city_coord = student_df.location
    center_city_coord = center_df.location
    nearest_city = []
    dist_center = []
    for student_coord in st_city_coord:
      dist_diff = []
      center_list = []
      for center_coord, center in zip(center_city_coord, center_df.center_cities):    
        try: 
          dist = geopy.distance.distance(student_coord, center_coord)
          dist_diff.append(dist)
          center_list.append(center)
        except:
          dist_diff.append("not_able to calculate")
      try:
        min_dist = min(dist_diff)
        index = dist_diff.index(min_dist)
        nearest_city.append(center_list[index])
        dist_center.append(min_dist)
      except:
        nearest_city.append("Not able to find")
        dist_center.append("Not able to find")

    return nearest_city, dist_center

  nearest_city, dist_center = find_nearest_center(st_city, center_city)

  st_city['nearest_center'] = nearest_city
  st_city['distance_to_center'] = dist_center

  incomplete_df = st_city[st_city.nearest_center == "Not able to find"][["Email Address", "student_cities","nearest_center"]]
  incomplete_df.to_excel("pending_center.xlsx")
  print('Successfully File Created: pending_center.xlsx')

  data = st_city.sort_values("nearest_center")
  data.to_excel("data.xlsx")
  print('Successfully File Created: data.xlsx')

except:
  print("Something is wrong, please contact to developer.")