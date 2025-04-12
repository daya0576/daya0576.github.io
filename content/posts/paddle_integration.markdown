---
title: "Paddle 全球收单攻略 - 让赚钱如同呼吸般简单"
date: 2025-04-12T09:54:56+08:00
categories:
- 独立开发
---

作为一个独立开发者，如果暂时无法前往香港开户，也没精力开设英国公司，如何为快速全球收款并验证产品呢？🤔

推荐老牌 [Paddle 平台](https://www.paddle.com/solutions/saas-billing)，让赚钱如同呼吸般简单：上线第一日还没来得及推广，便收入两笔交易 ^^（感谢来自澳洲的陌生用户的支持）。

最终集成效果：[https://beaverhabits.com/pricing](https://beaverhabits.com/pricing)

![](/images/blog/global/17444232133603.jpg)

# 接入步骤

## 1. 域名认证
官网申请发起后，不出意外被拒绝。但无需灰心，直接回复邮件根据要求继续耐心完善资料即可。

有趣的是邮件一来一回必定相隔一天.. 虽然态度特别友善，但每次对接的都是不同的客服，但效率极低。每次回复建议带上总结上下文，帮助对方快速通过审核。参考我的最后一次回复：
```
Hi xxx,

To make your review as convenient as possible, I have summarized our past conversations blew, hoping it can be helpful.

Pricing page: https://www.beaverhabits.com/pricing, i.e. the page to embed the Paddle checkout, which including:
- [x] Terms & Conditions page in the bottom of the page
- [x] Refund Policy (following Paddle's 14-day policy, and also mentioned on the Terms & Conditions page)
- [x] Privacy Policy page in the bottom of the page
- [x] Pricing plans, features and comprehensive video to helping customers better understand the product

Product page: https://www.beaverhabits.com/gui
- username: paddle@demo.com
- password: paddle

Other links:
- RESTful API documentation: https://github.com/daya0576/beaverhabits/wiki/Beaver-Habit-Tracker-API-How%E2%80%90to-Guide

Thanks
Henry
```

最终耗费两周通过审核。

# 2. 集成收款

简单根据文档一步步接入即可：[https://developer.paddle.com/build/onboarding/overview](https://developer.paddle.com/build/onboarding/overview)

## 注意点

1）⚠️ Paddle 提供了 Sandbox 环境供测试，所以申请审核与代码集成可并行开始。

2）⚠️ Paddle 提供了 js 代码，与各个语言的 sdk 减少工作量，例如：[PaddleHQ/paddle-python-sdk](https://github.com/PaddleHQ/paddle-python-sdk)

查询产品价格：
```python
paddle = Client(settings.PADDLE_API_TOKEN, options=Options(sandbox))
price_entity = paddle.prices.get(settings.PADDLE_PRICE_ID)
```

一键触发收银台：
```js
<script src="https://cdn.paddle.com/paddle/v2/paddle.js"></script>
<script type="text/javascript">
  Paddle.Initialize({ 
    token: '{{paddle_token}}' 
  });
  {% if sandbox %}Paddle.Environment.set("sandbox");{% endif %}

  // open checkout
  // https://developer.paddle.com/build/checkout/build-overlay-checkout
  function openCheckout() {
    Paddle.Checkout.open({
      items: [{ priceId: "{{price_id}}", quantity: 1 }],
      settings: {
        theme: "dark",
      }
    });
  }
</script>
```

处理 webhook 与验证签名（用户创建/下单/退款）：
```python
@callback("customer.created")
@callback("customer.updated")
async def customer_created(data: dict) -> None:
    ...

@router.post("/callback")
async def webhook(data: dict, request: FastAPIRequest) -> dict:
    // ...
    integrity_check = Verifier().verify(
        paddle_request, Secret(settings.PADDLE_CALLBACK_KEY)
    )
    // ...
```
[https://github.com/daya0576/beaverhabits/blob/239cbd27a291450aff6af27959e227f5f2aca4e3/beaverhabits/plan/paddle.py#L82-L94](https://github.com/daya0576/beaverhabits/blob/239cbd27a291450aff6af27959e227f5f2aca4e3/beaverhabits/plan/paddle.py#L82-L94)

3）⚠️ 小技巧：用户点击 checkout 时，支持通过传参自动填充邮箱地址简化流程：

![](/images/blog/global/17444269330291.jpg)

# That's all
如果有问题欢迎留言或发送邮件，祝老板们早日开单 ^^ 