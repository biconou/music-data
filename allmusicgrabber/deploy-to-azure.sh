
docker build -t allmusicgrabber:latest .

az webapp create --name allmusicgrabber-api --resource-group music-data-dev --plan music-data --deployment-container-image-name allmusicgrabber:latest
