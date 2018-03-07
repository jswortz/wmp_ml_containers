# WMP Machine Learning Container



## Building the Container

``` docker build -t wmp-ml .```

## Running the Container Interactively

Note that this is not really necessary unless you want to get into the guts of the container interactively

```docker run -a stdin -a stdout -i -t ubuntu /bin/bash```

## Running Jupyter

```docker run -d -p 8888:8888 -v $(pwd)/python/notebooks:/home/ds/notebooks -v $(pwd)/python/trainedModels:/home/ds/trained_models wmp-ml```

Now Jupyter should be running in the background. Go to:
<http://localhost:8888>
If it's your first time logging in go to here to get the token:
```docker logs <container id>```. Container ID can be obtained from ```docker ps```

* Note that this will load and save any notebooks in the ./python/notebook directory in the local repo
* Also note that the trained models can be saved locally and remotely via the 2nd '-v' command above
* The python packages are in the 'requirements' folder and can be changed as needed


Example of building a model can be found in python/notebooks


## Running Predictions
### Build:
```docker build -f Dockerfile.predict -t wmp-ml-predict .```

### Running:

```docker run -d -p 5000:5000 wmp-ml-predict```

Using your favorite JSON/CURL tool (Postman is a good one) you should be able to make predictions!

```0.0.0.0:5000/api/v1.0/iris```
```{"inputs": [4.1, 3.5, 1.4, 0.2]}```

Output:

``` 
{
    "outputs": [
        {
            "label": 0
        }
    ]
}
```
_____________

Note that there is a pre-built docker image that contains all of the various versions for model creation if needed:

<https://github.com/jupyter/docker-stacks>


