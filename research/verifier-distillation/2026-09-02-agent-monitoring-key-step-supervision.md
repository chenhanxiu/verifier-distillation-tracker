# 无内部信号的 Web Agent 监控：Observable Trajectory 与 Key-Step Supervision

## 基本信息

- **论文标题**：Monitoring Web Agents Without Internal Signals: Observable Trajectories and Key-Step Supervision
- **作者**：Sitong Pan, Yipeng Shen, Yilin Lu, Caiwen Ding, Lu Cheng, Qianwen Wang
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **arXiv**：[2609.02057](https://arxiv.org/abs/2609.02057)
- **DOI**：[10.48550/arXiv.2609.02057](https://doi.org/10.48550/arXiv.2609.02057)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

论文用可观察的 Agent—环境交互和黑盒多次采样预测 prefix 失败风险，并只从“首个未被后续纠正且关联终局失败”的关键步开始标负，避免把失败轨迹的有效前缀全部误判。

## 真正新增的内容

**论文原文结论**：Macro 特征总结跨步行为与反馈；Micro 特征用重复黑盒查询测量意图、动作和预期状态变化的一致性。监督标签不是把终局失败复制到每个 prefix，而是定位第一个未被纠正、最终导致失败的 critical error，之前的 prefix 仍标为 on-track。

这直接解决长轨迹 verifier 常见的 outcome-label leakage，并适合无法获得 logits 的闭源 Agent。

## 核心方法

从 Web 轨迹提取循环、工具反馈、动作历史等 Macro 特征；以多次采样估计 decision consistency 等 Micro 特征。训练 prefix risk predictor，并以 E-AURC、Brier、AUROC 衡量选择性干预、校准和区分能力；测试固定 false-cut budget 下的提前停止及跨网站类别迁移。

## 关键实验结果

**论文报告**：在 Mind2Web 的 15 个 backbone×metric 比较中，可观察信号全部匹配或超过最强可用不确定性 baseline，WebArena-Lite 为 9/15。Claude 示例中 WebArena-Lite 的 Micro AUROC 为 0.739、Macro 为 0.709，而 verbalized confidence 为 0.645；Mind2Web 的 Macro 为 0.772。后段轨迹中 Macro/Macro+Micro 的 AUROC 达 0.778/0.779。Micro 重复采样在 N=5–8 后收益平台化；N=5 使用一半 N=10 decode 预算。

## 证据质量与局限

跨两个基准、五个开放/闭源 backbone，并报告校准、选择性风险、时间切片、显著性和预算消融，证据较强。局限是 key-step 标签依赖“观测到的 continuation”，不等同于所有可能恢复分支的因果点；Micro 成本来自重复查询。网站类别迁移也不能证明跨环境/任务迁移。

## 最接近的相关工作

接近 trajectory uncertainty quantification、LongRCA、EDGE、AGENTSCOPE、SOPD、DART-SD 与 process reward modeling。区别在于只使用黑盒可观察量，并显式保留失败轨迹中的有效早期 prefix。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将 prefix risk 输出为“on-track / 可恢复风险 / 不可恢复风险”的序数分布，并把关键步边界作为 score-level teacher。Macro/Micro 分歧可触发额外 rollout 或强 Judge；只有程序终态确认失败且后续未纠正时，才给关键动作负梯度。对于下一步动作评估，这比直接预测最终成败更贴合“对目标的边际贡献”。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏关键步前后的风险跃迁，而非把终局标签广播给所有 token。
- **A/B/T 与序数分布**：从同一 prefix 比较候选动作的恢复风险；差异小或可恢复性未知标 T。
- **真值门控**：终态与后续是否纠正由环境日志判定，LLM 只帮助找候选关键步。
- **critique states**：让 student 在风险上升时生成 critique，再检查后续是否恢复。
- **高熵探索**：高不确定且尚未越过关键边界的 prefix 不应提前终止；使用 false-cut budget 控制误剪。
- **sealed eval**：按未见网站类别、Agent backbone 和工具 schema 切分，避免 predictor 学到站点/模型特征。