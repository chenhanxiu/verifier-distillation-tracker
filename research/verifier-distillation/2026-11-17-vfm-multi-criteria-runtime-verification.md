# Runtime Verification of Multiple Natural Language Criteria for Agent Governance

- **作者**：Silviu Pitis、Parand A. Alamdari、Jessica Tang、Toryn Q. Klassen、Sheila A. McIlraith
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.23074
- **代码链接**：https://github.com/spitis/vfm
- **标识符**：arXiv:2611.23074；DOI: 10.48550/arXiv.2611.23074

## 一句话结论

【论文原文】VFM 通过共享前缀与 tree attention，在一次前向中对上千条自由文本规则输出独立 yes/no/n/a 概率，使多标准 verifier 从昂贵的逐条 Judge 调用变成可运行时部署的分布式判定器。

## 真正新增的内容

【论文原文】提出 verifier foundation model：共享编码 context/target，让每条 criterion 在隔离分支中读取共享 KV cache，并输出三元概率；同时发布 CriteriaBank（394K 四元组、超过 321K 条不同规则）及训练/评测代码。

## 核心方法

1. 输入为 `(context, target, {criterion_i})`，每条规则独立输出 `P(yes/no/n/a)`。
2. tree-attention 阻止规则分支互相泄漏，同时复用长 trace 前缀计算。
3. CriteriaBank 由多数据流预训练，再对治理、事实、指令、过程奖励等任务微调；难例可升级到大型 CoT judge。

## 关键实验结果

【论文原文】VFM-4B 在合成治理基准上超过 GPT-5.4，在 DynaBench 的 trace-level failure detection 上超过 DynaGuard-4B，并能定位违反的具体规则。单张 H100 对约 4K-token context 评估 1,000 条规则用时 1.81 秒、显存低于 11GB；预训练在低数据迁移中收益最明显。

## 证据质量与局限

【论文原文】覆盖治理、保险对话、DynaBench 与五类跨域任务，并有人类复核；但规则必须先被分解为 trace-verifiable 原子问题。`n/a` 同时混合“确实不适用”和“证据不足”，二者在 Agent 路由中含义不同；自由文本规则翻译的覆盖率仍可能成为主要误差源。

## 最接近的相关工作

接近 LMUnit、DynaGuard、Sparrow rule-conditioned RM、SingGuard、Prometheus/Nemotron Judge、TRAC 的自然语言谓词标注。其关键差异是开放规则集、三元分布输出与共享前缀的并行效率。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把每个长轨迹 rubric、权限条件、阶段义务和完成证据拆成 criterion，保留完整三元概率而非只取 argmax；以高 `P(n/a)` 或高熵触发环境查询/大 Judge，以 `P(no)` 做定位信用。VFM 可作为低成本 student verifier，teacher 使用环境 oracle 与生成式 Judge 共同标注。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：直接蒸馏每条 criterion 的三元 logit，而不是只蒸馏总分；总分由冻结聚合器计算。
- **pairwise A/B/T 与序数分布**：将 yes/no/n/a 映射为 A/B/T 时保留 criterion 级分布；`n/a` 不等于 tie，应拆成 inapplicable 与 insufficient-evidence。
- **程序化/环境真值门控**：可执行规则覆盖 VFM 的 soft verdict；VFM 仅在无 oracle 或作路由时生效。
- **student-generated critique states**：critique 必须引用具体 criterion 与 trace 证据，随后由该 criterion 的 oracle/teacher 复核。
- **高熵分叉探索**：以 criterion 级熵和规则间冲突选择分叉，避免平均分掩盖少数高风险规则。
- **sealed eval**：冻结规则分解、聚合方式和独立人类/程序标签；单独评估 rule translation coverage，防止 verifier 与训练 rubric 共适应。
