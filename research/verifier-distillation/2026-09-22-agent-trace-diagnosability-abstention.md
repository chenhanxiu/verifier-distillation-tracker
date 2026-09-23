# When Are Aggregate Agent Traces Diagnosable? Traffic-Governed Interpretation and Calibrated Abstention

- **作者**：Peiying Zhu, Sidi Chang
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.25806
- **Canonical URL**：https://arxiv.org/abs/2609.25806
- **DOI**：10.48550/arXiv.2609.25806（arXiv DataCite，待注册）
- **代码/复现材料**：论文内链接的 reproducibility artifact；arXiv 摘要页未给出独立仓库 URL
- **arXiv ID**：2609.25806

## 一句话结论

【论文原文】聚合 Agent 轨迹只有在“参考策略确实访问相关状态”且“当前运行与参考流存在可比支持”时才有资格用于故障判断；两级门控与显式 abstention 比直接对轨迹打分更重要。

## 真正新增的内容

【论文原文】论文把“轨迹是否足以支持某个诊断”定义成评分之前的独立决策，并区分 REFERENCE_ABSTAIN、RUNTIME_ABSTAIN、SIGNAL_ELIGIBLE、DETECTED/NOT_DETECTED。它提出 affected clean traffic，用策略实际访问到的受影响状态占比代替名义上修改了多少网格，并用预注册 heldout 检验门控、误接纳和跨 mask-family 的实用充分性。

【分析推断】这为长轨迹 verifier 增加了此前常缺失的“可判定性”类别：没有证据支持不等于负例，应该输出 T/INCONCLUSIVE 并阻止蒸馏更新。

## 核心方法

- 在模拟酒店定价 Agent 中，用 clean reference stream 建立组件支持图，再对当前 stream 检查共同支持。
- 只有两个支持门都通过后才解释 aggregate signal；零暴露、漂移或不可比状态显式弃权。
- 以受影响 clean traffic 预测稳定检测概率，并与受影响 cell fraction 对比。
- 把安全误接纳、覆盖率、结构拟合和执行完整性分别报告，不合并为单一“成功”结论。
- 独立 shift detector 触发 reference map 刷新，不把分布漂移误判成故障。

## 关键实验结果

- 72 个 regime-component 单元中 55 个通过参考门控，54/55 通过运行时门控；20 个代表性物理组件中稳定 false admission 为 0/20，单侧 95% 上界 0.1391。
- 受影响 traffic 相比 cell coverage 将负对数似然降低 29.3%（每行改善 0.1264 nats，组件 bootstrap 95% CI [0.0593, 0.1918]）。
- 加入 mask family 与交互只改善 0.0015 nats/row，单侧上界 0.0066，低于预注册 0.01 实用边界。
- 44 个零暴露观测全部 abstain，且无稳定信号。
- exact minimum hitting set 与 propagation-aware greedy 在开发集 12/12 场景选择相同支持，揭示上游证据单例化让“高级定位器”优势不可检验。

## 证据质量与局限

【论文原文】设计包含冻结协议、开发/heldout 分离、组件粒度 bootstrap、显式否定结果和预注册阈值，证据纪律较强。但仅使用一个模拟器、24 个物理组件、一档故障幅度和两种 mask family；误接纳上界是 0.20 而非 0.05；结果验证的是定位前信号资格，不是实际故障定位准确率。clean reference stream 也并非所有线上系统都有。

【分析推断】它不能直接证明 LLM verifier 的置信度可校准，却强烈说明任何轨迹评分器若忽略策略访问分布，就会把“没看到”当成“没有发生”。

## 最接近的相关工作

最接近 selective prediction、offline RL 的 support/overlap 检查、AgentDiagnose、FARM/HaWMPO 的轨迹风险估计，以及 ClaimReceipt 的 INCONCLUSIVE 机制。与普通 process reward 不同，本方法先判断观测是否足以支撑结论，再允许评分。

## 如何复用或推进 LLM-as-a-Verifier

- 在 pointwise/ordinal verifier 输出中增加“证据覆盖不足”状态，并将其映射为 A/B/T 中的 T 或拒答，而非 0 分。
- 用 on-policy visitation 估计每条 rubric/义务的 exposure；只有 exposure 与当前运行支持同时满足时，才蒸馏 teacher score。
- 对 student-generated critique 附带证据指针和状态覆盖率；无法重放到相关组件的 critique 不进入 memory。
- 将漂移检测和失败检测分开，漂移只触发重新采样/更新 reference map。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】在 score-level OPD 前增加 eligibility gate：程序真值决定是否有可判定证据，distributional verifier 再输出评分分布。训练损失应把 abstention mask 掉，而不是作为低分；报告 conditional performance 与把弃权计为无动作的 operational performance。高熵分叉应优先补采低 exposure 分支。sealed eval 需冻结 reference policy、支持阈值和漂移规则，并在独立流量分布上检验 false admission，防止 evaluator 只适配训练策略访问过的状态。