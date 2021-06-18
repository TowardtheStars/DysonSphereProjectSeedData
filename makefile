
VERSION=0.7.18.7178

all: dirs assets zip svlik

assets: dirs
	python assets-converter.py

proto: assets
	python gen_proto.py

zip: dirs
	powershell Compress-Archive -Path "./data" -DestinationPath "./build/${VERSION}.zip" -Force

icon: dirs
	python iconbase64.py

dirs:
	powershell if (-not (Test-Path "./build")) {mkdir ./build}
	powershell if (-not (Test-Path "./data")) {mkdir ./data}
	powershell if (-not (Test-Path "./svlik")) {mkdir ./svlik}
	
svlik: dirs assets
	python svlik.py