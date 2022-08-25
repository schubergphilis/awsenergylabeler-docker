# energylabeler-docker

## awsenergylabeler

Running the container for your local machine (assuming you already setup `~/.aws` folder with your credentials and config)

```bash
docker run -v ~/.aws:/home/nonroot/.aws awsenergylabeler -s <ACCOUNT_NUMBER>
```

Or running with environment variables set:

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN awsenergylabeler -s <ACCOUNT_NUMBER> --region eu-west-1
```

## Container signature
All container in this repository are signed and their signature can be verified against the following public key:

#### **cosign.pub**
```bash
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEiiLa3LCyiwGcZeYNCktkJmllgYpN
+DXIRff+t1WcTinlWuIt5wMqVurKzAEqiOQdYylZq5UMclb1dSK9RXS95g==
-----END PUBLIC KEY-----
```

Manually verification can be performed by issuing:

```bash
cosign verify --key cosign.pub <IMAGE_NAME>
```
