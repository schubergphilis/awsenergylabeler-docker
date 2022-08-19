# energylabeler-docker

## awsenergylabeler

Running the container for your local machine (assuming you already setup `~/.aws` folder with your credentials and config)

```
docker run -v ~/.aws:/home/nonroot/.aws awsenergylabeler -s 747966750797
```

Or running with environment variables set:

```
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN awsenergylabeler -s 747966750797 --region eu-west-1
```
