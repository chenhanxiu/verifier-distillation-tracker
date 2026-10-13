# Unsupervised Multimodal Reward Modeling

- **作者**：Yueying Li；Jingxuan Fan；Kianté Brantley；Sham M. Kakade；Hanlin Zhang
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12707
- **Canonical URL**：https://arxiv.org/abs/2610.12707
- **DOI**：10.48550/arXiv.2610.12707
- **代码**：未发现公开代码链接

## 一句话结论

该工作用冻结 VLM 中间层上的轻量线性头和自动语义扰动学习 reward，并证明 benchmark 排名不足以定义奖励；真正决定 verifier 行为的是训练比较分布及其 on-policy 更新。

## 真正新增的内容

【论文原文】不使用人工偏好标签，只让 reward head 把原始网页 caption 排在同图扰动 caption 之上；标注数据仅用于选层，并在 policy 自身候选上用 verifier 标签做一次 bootstrap。  
【分析推断】这为低成本 distributional verifier 提供了“冻结 backbone＋可审计扰动生成器＋轻量头”的实现，但扰动器本身就是隐式 rubric，必须被版本化和验证。

## 核心方法

1. 冻结 Qwen3-VL，探测不同中间层并选择最有效表示。
2. 自动生成同图 caption 的语义扰动对。
3. 用凸优化训练数千参数的线性 reward head。
4. 在当前策略候选上以 verifier 标签再训练，使 reward 分布贴近 on-policy 状态。

## 关键实验结果

【论文原文】选中间层比末层高 5.8 点；32B 设置在三个 benchmark 上不弱于 GPT-4o，并在 VL-RewardBench 高 6.6 点，计算量约为微调的千分之一。同预算下自动扰动比 curated RLAIF-V 高 3–5 点。on-policy bootstrap 使 caption hallucination 降低 5.1 CHAIR 点、图像生成 pass rate 提高 5.4 点，尽管所有 reward benchmark 分数更低。

## 证据质量与局限

有跨 benchmark、层选择、pair 来源和 on-policy 下游实验，证据中等偏强。重要局限是两个在 benchmark 上并列的头，在 hallucination judging 上可相差 6.4 点，说明离线榜单并不标识构念；视觉 caption 扰动结论也不能直接等同长轨迹 Agent 评价。

## 最接近的相关工作

与 RoboRef、OmniHallu、DreamTrue、FARM、GLARE 和 IWD 最接近。独特处是冻结表示层、以扰动分布定义 reward，并用真实策略候选闭环修正。

## 如何复用或推进 LLM-as-a-Verifier

可在 Agent 轨迹编码器的中间层训练小型 ordinal head；用语义保持、错误注入、证据删除和工具结果交换构造成对监督，并把扰动类型作为显式 rubric 版本。最终选择依据应是 sealed 下游成功，而非 Judge benchmark 单分。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：轻量 head 输出分数/分布，定期用当前 student 轨迹 bootstrap。
- **A/B/T 与序数分布**：不同扰动强度可构成序数等级；近界样本输出 T。
- **程序化/环境真值门控**：自动扰动必须经环境或规则确认确实改变/保持真值。
- **student-generated critique states**：只接收能识别预先定义扰动、且在执行后验证的 critique。
- **高熵分叉**：在当前策略候选的高不确定区域补采样，而非追求离线 benchmark。
- **sealed eval**：冻结扰动集、真实任务集和另一架构 verifier，检查构念漂移。