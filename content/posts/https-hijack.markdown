---
title: "[SRE] Resiliency Test - HTTP/HTTPS Hijack"
tags:
  - sre
  - chaos
categories:
  - SRE
date: 2023-11-18 07:49:24
---

Recently researching an internal tool to support resiliency testing, e.g. performing network delay on dependent redis/db/.., helps validate the service’s ability to handle and recover from unexpected network disruptions or delays in accessing external dependencies.

TCP layer network traffic can easily be classified and shaped using a Linux built-in tool called TC (traffic control). 

<u>**But how can we hijack and manipulate encrypted outbound HTTPS traffic?**</u>

<!--more-->

## 1. Traffic Takeover
Enable traffic through a proxy server via HTTP(S)_PROXY  environment variable, and most standard libraries follow this convention.

```
export https_proxy=http://127.0.0.1:<port>;export http_proxy=http://127.0.0.1:<port>
```

After sending the [CONNECT](https://datatracker.ietf.org/doc/html/rfc7231#section-4.3.6) method request, the `https_proxy` can proxy the TCP stream to and from the client by establishing a HTTP tunnel to the destination origin server.
![http_proxy_original.drawio](/images/blog/2021-09-04-jvm-note/http_proxy_original.drawio.svg)


## 2. Traffic Processing
Implement a lightweight HTTP proxy by native http.server module in Python.

### HTTP (Transparent Proxy)
According to [rfc7231](https://datatracker.ietf.org/doc/html/rfc7231#section-4.3.6). As long as the `CONNECT` method request is handled, the proxy can forward the TCP stream to and from the client by establishing a HTTP tunnel.

### HTTPS (Hijack)
As we know, the TLS encryption prevents us from inspecting the specific endpoints and headers within the encrypted traffic.

We must hijack HTTPS requests to determine the type of dependency service (such as ACM, OSS, etc.):

1. Identity:
    1. client → server:   ask for appropriate certificate
    2. server → client:   provide server certificate (and intermediate)
    3. client:                   receive certificate and ensure Common Name(domain name) of request matching
    4. client:                   Confirm that the root certificate (valid  Certificate Chain)
2. Encryption:
    1. TLS handshake: asymmetric Encryption →  generates a symmetric encryption key (the session key)
    2. Data transmission: session key → data encryption

Appropriate workflow (i.e. MITM attack):
![rtf MITM1.drawio](/images/blog/2021-09-04-jvm-note/rtf%20MITM1.drawio.svg)

## Reference 
1. https://github.com/chobits/ngx_http_proxy_connect_module
2. https://manual.nssurge.com/book/understanding-surge/en/#tls-https-and-mitm
3. https://github.com/tinyproxy/tinyproxy