---
layout: post
title: "custom_domain"
date: 2014-04-10 23:38:30 +0800
comments: true
categories: [study, domain]
---

哎   弄个域名绑定也弄了一天。      
貌似绑定A级域名要用`192.30.252.153`才行了

照着一个外国大叔的配的：

<ol> <li>Set the <strong>@</strong> (used to denote the domain name for which you’re configuring the DNS) <strong>IP Address/URL</strong> to <code>192.30.252.153</code> and the <strong>Record Type</strong> to <code>A (Address)</code> with a <strong>TTL</strong> (an acronym for <strong>Time To Live</strong> that refers to the capability of the DNS servers to cache DNS records) of <code>1800</code>.</li> <li>Set the <strong>www</strong> (the subdomain www) <strong>IP Address/URL</strong> to <code>username.github.io.</code> (with trailing period) and the <strong>Record Type</strong> to <code>CNAME (Alias)</code> with a <strong>TTL</strong> of <code>1800</code>.</li> <li>In <strong>SUB-DOMAIN SETTINGS</strong>, add an <code>@</code> in the first field, and duplicate the settings in Step 1, save for the <strong>IP Address/URL</strong>, which should be <code>192.30.252.154</code>.</li> </ol>

<p><img src="http://davidensinger.com/assets/img/posts/2014-01-07-namecheap-dns-settings.png" alt="Image of DNS settings" class="media-center img-border"></p>

<p>Save and then you’re all set! Please note, however that it may take some time for the changes to the DNS to propagate.</p>

<div class="gray-box"> <p><strong>More Info:</strong> Google has a pretty good <a href="http://support.google.com/a/bin/answer.py?hl=en&amp;answer=48090">Basic Guide to DNS</a>.</p> </div>


github官方文档：[https://help.github.com/articles/setting-up-a-custom-domain-with-pages](https://help.github.com/articles/setting-up-a-custom-domain-with-pages)

