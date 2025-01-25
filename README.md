# Fetch Tor Bridges using Llama Vision

### Problem Statement
The Tor Project has a useful endpoint to obtain obfs4 bridges at `https://bridges.torproject.org/moat/fetch`. There is a visual word captcha however that needs to be solved to get the bridges. 

### Example

Leveraging [Llama3.2-Vision](http://ollama.com/library/llama3.2-vision), we can use Meta's AI model to decrypt and solve word captchas. In this example statement, I am using the model to decrypt Tor's Moat Captcha to obtain obfs4 bridges for Tor.

You can use the provided Dockerfile to give it a test, which should setup everything for you

```
docker build -t fetch-tor-bridges . && docker run --rm fetch-tor-bridges
```