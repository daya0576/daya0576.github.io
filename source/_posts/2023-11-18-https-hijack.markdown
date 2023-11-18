---
title: HTTPS Hijack for Resiliency Test
tags:
  - sre
  - chaos
categories:
  - SRE
date: 2023-11-18 07:49:24
---

Recently I'm researching an internal tool to support chaos/resiliency testing, e.g. performing network delay on dependent redis/db/.., helps validate the service’s ability to handle and recover from unexpected network disruptions or delays in accessing external dependencies.

TCP layer network traffic can easily be classified and shaped using a Linux built-in tool called TC (traffic control). But how can we hijack and manipulate encrypted outbound HTTPS traffic?

<!--more-->

### 1. Traffic Takeover
After sending the [CONNECT](https://datatracker.ietf.org/doc/html/rfc7231#section-4.3.6) method request, the `https_proxy` can proxy the TCP stream to and from the client by establishing a HTTP tunnel to the destination origin server.
```shell
  curl                     nginx (proxy_connect)            github.com
    |                             |                          |
(1) |-- CONNECT github.com:443 -->|                          |
    |                             |                          |
    |                             |----[ TCP connection ]--->|
    |                             |                          |
(2) |<- HTTP/1.1 200           ---|                          |
    |   Connection Established    |                          |
    |                             |                          |
    |                                                        |
    ========= CONNECT tunnel has been established. ===========
    |                                                        |
    |                             |                          |
    |                             |                          |
    |   [ SSL stream       ]      |                          |
(3) |---[ GET / HTTP/1.1   ]----->|   [ SSL stream       ]   |
    |   [ Host: github.com ]      |---[ GET / HTTP/1.1   ]-->.
    |                             |   [ Host: github.com ]   |
    |                             |                          |
    |                             |                          |
    |                             |                          |
    |                             |   [ SSL stream       ]   |
    |   [ SSL stream       ]      |<--[ HTTP/1.1 200 OK  ]---'
(4) |<--[ HTTP/1.1 200 OK  ]------|   [ < html page >    ]   |
    |   [ < html page >    ]      |                          |
    |                             |                          |
```

### 2. Traffic Processing
Currently we can only filter traffic by domain (from the `CONNECT` method request). The TLS encryption prevents us from inspecting the specific endpoints and body within the encrypted traffic.

<u>How can we Hijack https requests and classify the network traffic by endpoint?</u>

We have to address two issues:
1. Identity:
    1. client → server:   ask for appropriate certificate
    2. server → client:   provide server certificate (and intermediate)
    3. client:                   receive certificate and ensure Common Name(domain name) of request matching
    4. client:                   Confirm that the root certificate (valid  Certificate Chain)
2. Encryption:
    1. TLS handshake: asymmetric Encryption →  generates a symmetric encryption key (the session key)
    2. Data transmission: session key → data encryption

Appropriate workflow (i.e. MITM attack):
![rtf MITM.drawio -1-](../images/blog/2021-09-04-jvm-note/rtf%20MITM.drawio%20-1-.svg)


### Reference 
1. https://github.com/chobits/ngx_http_proxy_connect_module
2. https://manual.nssurge.com/book/understanding-surge/en/#tls-https-and-mitm
3. https://github.com/tinyproxy/tinyproxy