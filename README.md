# nkcrawler
nkcrawler is a container batch application for collecting [netkeiba.com](https://www.netkeiba.com/) data. nkcrawler depend on [nkparser](https://github.com/new-village/nkparser) which is a python library.   
  
## Description
This application execute below:  
1. Download SQLite database file from Azure Blob Storage, if the database file is exists on Azure.  
2. Collect netkeiba.com data by defined year of environment variables.  
3. Insert collected data to SQLite Database.  
4. Upload SQLite database file to Azure Blob Storage.  
  
## Usage
RECCOMEND: You shoud use async execution like tmux due to long time execution (over 10 hours per month).
```sh:
$ export CONNECTION_STRING="YOUR CONNECTION STRING"
  
$ pip install -U pip
$ pip install -r requirements.txt
$ python run.py
```

### Docker Container
```sh:
$ docker build -t nkcrawler .
$ docker run --rm -e CONNECTION_STRING=${CONNECTION_STRING} -it nkcrawler
```
  
### Azure Docker Registry  
1. Push Image to Azure Container Registry   
You can see pushed contaier image on Azure Container Registry > Repository after below commands.
```sh:
$ ACR_USERNAME="AZURE CONTAINER REGISTRY USERNAME"
$ ACR_PASSWORD="AZURE CONTAINER REGISTRY PASSWORD"
$ ACR_REGISTRY="YOUR AZURE CONTAINER REGISTRY REGISTRY"
  
$ docker login -u ${ACR_USERNAME} -p ${ACR_PASSWORD} ${ACR_REGISTRY}
$ docker tag nkcrawler ${ACR_REGISTRY}/nkcrawler
$ docker push ${ACR_REGISTRY}/nkcrawler
```
  
2. Run Container by Azure Container Instance
Access to `Azure Container Instance` and then you select `Create`. See [Set environment variables in container instances](https://docs.microsoft.com/en-US/azure/container-instances/container-instances-environment-variables)  
In Advance Tab, you might set `restart policy` to `None`. and you also set `CONNECTION_STRING` and `YEAR` environment variables.
