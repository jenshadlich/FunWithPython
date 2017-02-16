import geoip2.database

reader = geoip2.database.Reader('./db/GeoLite2-Country.mmdb')

response = reader.country('2601:646:8100:fee3:6d17:d0e:36df:8576')

print(response.country.name)