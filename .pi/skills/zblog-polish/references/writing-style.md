# Henry 的文章风格

## 来源与适用范围

基于本次对话中按 front matter 日期读取的 20 篇非草稿文章，日期范围 2026-03-26 至 2026-10-01。以下是编辑参考，不是对所有文章的固定模板，也不代表样本中的技术论断已经核查。

## 技术文章与阅读笔记

- **从具体问题开始**：CPython #5 从 `a = b` 引出变量实现；#6 从 `x + 7` 引出对象系统。先让读者知道在解释什么，不铺宏观时代背景。
- **顺着疑问推进**：解释一个概念后，遇到实际障碍再引出下一个。例如“else 的代码还没生成，跳转地址从哪来？”比先列一串编译器术语更符合文章习惯。
- **术语后接解释或例子**：保留 agent、harness、bytecode、frame 等英文；用一句中文说明作用，然后给最小例子、源码或箭头图。不要每次出现都重复翻译。
- **重视过程与边界**：说清输入、输出、执行顺序、为什么需要这个设计。区分已有能力、新增机制，以及需要用户自行实现的部分。
- **来源与理解分开**：用“作者认为”“原文提到”交代转述；补充解释可以标“例如”，个人观点只有用户提供时才标“个人理解”。不替作者发明评价。
- **可以直接承认省略**：不重要的部分简短带过，没弄清的问题保留为问题，不为了完整而扩写泛泛的总结。
- **图和代码用于解释关系**：读者难以从文字跟上调用链或层级时再加图，不为了排版工整制造表格。

## 生活记录

- 由具体的小事、对话和动作承载情绪，例如奶瓶忘装吸管、孩子递纸巾；少用抽象评价代替细节。
- 原稿中有调侃、括号、P.S. 和轻微岔题时可以保留；不把文章修成正式报告。
- 家人的原话和实际经历是事实，不因追求简洁而改写引用含义，更不能另编故事。
- 不强行给每件小事提炼教育意义，不把生活文套成技术解说结构。

## 表达与版式

- 简体中文为主，中英文技术术语自然混用。
- 标题常直接提出问题，或沿原文的小节组织阅读笔记。
- 列表、1）2）、引用和 P.S. 都是可用形式，但是否使用取决于内容，不按固定数量凑点。
- 一句能解释清楚就不写一段；真正卡住的概念允许多写。简洁不等于删掉条件、因果或例子。
- 保留作者的自然用语，不照搬样本里的笔误、连续标点、密集破折号，也不刻意增加 emoji。
- 可以自然结束，不需要“最值得注意的一点”“未来值得期待”等总结包装。

## 本次对话明确的编辑要求

- 少套话，避免“slop”；不将每段包装成金句。
- 用户要求尊重原文时，保留原文顺序；一个小节一行的要求优先于扩写冲动。
- 需要解释术语时给简短具体例子，不只把术语换成另一个抽象词。
- 区分 Pi 已有能力与 Durable 新增机制；不要把产品介绍里的所有功能都说成独有。
- 编辑全文时，加删一个部分后仍返回全文；单句问题则只处理单句。
- 用户明确删去的泛泛结尾不在后续版本中重新补回。

## 样本清单

路径相对项目根目录。常规润色无需重新读全部文章；更新风格或需要确认原句时再读取。

1. `content/posts/you-said-no-mcp.markdown`
2. `content/posts/paipai-1year4month.markdown`
3. `content/posts/read-python-behind-the-scenes-6-how-python-object-system-works.markdown`
4. `content/posts/optiver-referral.markdown`
5. `content/posts/read-python-behind-the-scenes-5-how-variables-are-implemented-in-cpython.markdown`
6. `content/posts/how-to-talk-so-little-kids-will-listen-6-part2.markdown`
7. `content/posts/read-python-behind-the-scenes-4-how-python-bytecode-is-executed.markdown`
8. `content/posts/read-python-behind-the-scenes-3-stepping-through-the-cpython-source-code.markdown`
9. `content/posts/python-behind-scenes-2-compiler.markdown`
10. `content/posts/read-python-behind-the-scenes-1-cpython-vm.markdown`
11. `content/posts/paipai_one_year.markdown`
12. `content/posts/tools-in-action-part1.markdown`
13. `content/posts/paipai-growth-diary-14-daycare.markdown`
14. `content/posts/building-pi-and-self-modifying-software.markdown`
15. `content/posts/paipai_eleven_months.markdown`
16. `content/posts/macos_apps_2026.markdown`
17. `content/posts/read I've sold out.markdown`
18. `content/posts/cloudflare-outage-february-20-2026.markdown`
19. `content/posts/how to talk so little kids will listen - chapter5.markdown`
20. `content/posts/how to talk so little kids will listen - chapter4.markdown`
