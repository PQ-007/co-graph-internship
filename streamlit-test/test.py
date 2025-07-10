
import requests
ip = "51.15.22.23"
result = requests.get(f"https://ipinfo.io/{ip}/json")

print(result.json()["region"])