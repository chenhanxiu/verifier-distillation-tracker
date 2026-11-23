# When Students Fail to Learn from Teachers: Learning Dynamics of On-Policy Distillation

- **作者**：Xinnan Zhang、Zeyi Liao、Siliang Zeng、Zhongruo Wang、Jiaxiang Li、Xinyan Zhao、Huan Sun、Mingyi Hong
- **首次公开日期**：2026-11-20
- **当前版本日期**：2026-11-20（v1）
- **原始论文**：https://arxiv.org/abs/2611.27125
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.27125；DOI: 10.48550/arXiv.2611.27125

## 一句话结论

OPD 即使在已访问状态上与 teacher 高度重合，也可能因 teacher top-p 区域质量不足、错配梯度串扰和终止 token 失配而把 student 推向重复且 teacher 不可靠的状态；分歧状态需要定向校正而非统一加权。

## 真正新增的内容

**论文原文**：论文从局部 sampled-token 更新、跨 token 梯度影响到后续 on-policy 采样，串起三类失效机制，并用终止 token 错配解释响应变长、重复和严重退化。

**分析推断**：这为 verifier × OPD 提供了“何时不该相信 teacher gap”的机制解释：已访问状态上的 agreement 可能是伪一致，不能作为训练收敛或 verifier 正确的证据。

## 核心方法

- 用 student 在 teacher top-p 集上的概率质量刻画错配状态。
- 分析 sampled-token OPD 在错配状态下为何难以修正 teacher–student 差距。
- 研究错配状态梯度对其他 token 学习的串扰。
- 以终止 token 为案例，追踪更新如何改变下一轮采样分布并进入 teacher 不可靠区域。

## 关键实验结果

**论文原文**：观察到 capable teacher 下仍会出现过长响应、重复和性能崩溃；“spurious agreement”表现为访问状态上的重合度高，但生成行为退化。分析解释了 SFT 初始化为何有帮助，并支持对错配状态做 targeted correction。摘要未提供跨基准数值幅度。

## 证据质量与局限

优点是连接局部梯度与分布演化，而非只报告最终性能。局限是 10 页、公开摘要缺少模型/任务覆盖与充分数值，终止 token 案例未必代表工具调用、视觉或长时程状态中的全部错配；因果机制仍需更多受控消融复现。

## 最接近的相关工作

接近 Divergence-Routed OPD、Entropy-aware OPD、SAVOR、AC-OPD、OPD-Aha，以及研究 KL 方向和 test-time scaling 的工作。本文重点不是提出新目标，而是解释失效动力学。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：为每个状态记录 teacher top-p 覆盖、student–teacher gap、termination/action-validity 概率和环境证据；当 gap 高且 teacher 在该状态缺少可靠证据时，verifier 应降权或拒绝，而不是加强蒸馏。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：新增 mismatch gate；只有 teacher 支持集覆盖足够且环境证据一致时传递 score。
- **A/B/T 与序数分布**：错配但 teacher 可靠度未知的状态标为 T，不强制 A/B。
- **真值门控**：终止、非法动作、工具返回和任务完成信号优先覆盖 teacher。
- **critique states**：重复或过长轨迹的 critique 要追溯首个错配状态，而非只批评最终文本。
- **高熵探索**：错配状态不应统一剪枝；保留少量替代分支以判断是 student 支持不足还是 teacher 失真。
- **sealed eval**：单独报告长度、重复、环境成功率和分布覆盖，避免只看 teacher agreement。