# Unpacking the Compute Efficiency of Strong-to-Weak OPD against GRPO

- **作者**：Zeyu Leo Liu, Yang Li, Bo Pang, Emre Can Acikgoz, Xuan-Phi Nguyen, Anurag Koul, Srijan Bansal, Erik Nijkamp, Shafiq Joty, Semih Yavuz
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08453
- **DOI**：https://doi.org/10.48550/arXiv.2611.08453
- **代码**：论文页面未给出公开代码链接

## 一句话结论

外部强 teacher 的 vanilla reverse-KL OPD 并不天然比 GRPO 更省算力；真正高效的场景是把 student 自身的分域 GRPO checkpoint 当作 teacher，再以多 teacher OPD 合并能力。

## 真正新增的内容

论文首次在统一 FLOPs 口径下系统比较 strong-to-weak OPD 与 GRPO，并把“蒸馏阶段便宜”与“端到端训练便宜”明确区分。关键反例是：外部 post-trained teacher 的密集 token 监督常伴随回答长度膨胀，准确率/FLOP 反而落后于 GRPO；关键正例则是 checkpoint consolidation。

## 核心方法

在任务难度、student/teacher 规模、领域、优化设置等条件下比较 vanilla reverse-KL OPD 与 GRPO，以 held-out accuracy 对训练 FLOPs 作主指标。随后用 student 各分域 GRPO checkpoint 作为冻结 teacher，对同一个 student 做多 teacher OPD 合并。

## 关键实验结果

- 外部 post-trained teacher 下，OPD 在匹配设置中通常不及 GRPO 的准确率/FLOP，并常出现响应长度膨胀。
- 用 student 自身 GRPO checkpoint 作 teacher 时，数学能力可用比原 GRPO 少 **50×** 的蒸馏 FLOPs 恢复；该现象在更大 student、代码任务及第二个模型族中复现。
- 多 teacher OPD 的合并阶段仅占 specialist 训练 FLOPs 的 **5.2%（2 域）/8.0%（4 域）**。
- 两域端到端 pipeline 达到 joint GRPO 表现时，总 FLOPs 少 **42.0%**。

## 证据质量与局限

**论文原文结论**：结果覆盖多任务、两模型族与多种规模，且显式核算训练 FLOPs，证据比只报 wall-clock 或最终准确率更强。  
**局限**：主方法仍是 vanilla reverse-KL；未直接检验 score-level verifier 蒸馏、长时程 Agent 轨迹或 evaluator 共适应；FLOPs 也不等于真实部署成本。

## 最接近的相关工作

最接近的是 multi-teacher OPD、checkpoint/model merging、GRPO/RLVR，以及 RouteOPD、CompassOPD、GVPO++ 等跨 teacher/跨模型族的概率或序列迁移方法。

## 如何复用或推进 LLM-as-a-Verifier

可将每个环境或 verifier 维度上的已验证 checkpoint 视为 specialist teacher，蒸馏其**相对 score 位移**而非完整 token 分布；把程序化真值作为方向门控，把 teacher 的校准分布作为幅度，并单独计入 specialist 训练与 consolidation 的总成本。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 的首要基线不应只对比“外部强 Judge”，还应加入“student 自身经真值 RL 得到的分域 checkpoint teacher”。
2. A/B/T 或序数分布可按领域分别训练 specialist verifier，再做多 teacher consolidation；若只报告蒸馏阶段成本会高估优势。
3. 高熵分叉可保留各 specialist 的分歧，避免合并后过早平均成单一策略。
4. sealed eval 必须同时报告最终能力、响应长度、总 FLOPs 与分域遗忘，防止把长度膨胀或 evaluator 特化误判为效率提升。