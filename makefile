
VERSION=0.7.18.6931

all: dirs assets zip

assets: dirs
	python assets-converter.py

proto: assets
	python gen_proto.py

zip: dirs
	powershell Compress-Archive -Path "./data" -DestinationPath "./build/${VERSION}.zip"

dirs:
	powershell if (-not (Test-Path "./build")) {mkdir ./build}
	powershell if (-not (Test-Path "./data")) {mkdir ./data}
	