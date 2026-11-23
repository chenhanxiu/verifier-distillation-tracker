# ProbeAgent: Principled Diagnosis of Agent Failures in Verifiable Environments

- **作者**：Yue Huang、Yuchen Ma、Shuhang Lin、Yuyang Wu、Zixuan Weng、Zixiang Xu、Xiangqi Wang、Yuexing Hao、Yujun Zhou、Yue Zhao、Olexandr Isayev、Stefan Feuerriegel、Xiangliang Zhang
- **首次公开日期**：2026-11-19
- **当前版本日期**：2026-11-19（v1）
- **原始论文**：https://arxiv.org/abs/2611.26897
- **代码**：截至本记录未在 arXiv 页面确认作者公开代码链接
- **标识符**：arXiv:2611.26897；DOI: 10.48550/arXiv.2611.26897

## 一句话结论

ProbeAgent 把“失败原因解释”转化为经参考解与自动检查验证的可执行反事实任务，再测试错误是否复现；这是将 student-generated critique 从自然语言意见升级为可验因果假设的直接模板。

## 真正新增的内容

**论文原文**：框架从失败轨迹提出原因、生成保持该原因但改变上下文的新任务、执行 Agent 检验错误是否复现，最后聚类为共享失败模式；因此诊断不只依赖事后叙述。

**分析推断**：对 verifier 蒸馏最关键的是 critique state 带有可执行测试和复现结果，可作为高置信 teacher 信号；未复现的解释应保留为 T，而不是负标签。

## 核心方法

- 从基准任务构造可执行测试，并用参考解、自动检查与任务要求审查验证测试本身。
- 对每条失败轨迹生成具体错误解释和因果保持型新任务。
- 重新运行 Agent，观察同一错误是否跨上下文复现。
- 聚类相似原因并生成可区分的失败模式描述。

## 关键实验结果

**论文原文**：

- 覆盖 10 个基准、22 种 Agent 配置，收集 1,244 次失败并生成 536 个失败模式描述。
- 人工评估接受 90.0% 的匹配描述，并能正确拒绝 83.3% 的相似替代描述。
- 可区分“只规划未行动”“交付文件前提前停止”等同属未完成但机制不同的错误。

## 证据质量与局限

覆盖面与执行复现设计较强，且人工验证了描述的准确性和特异性。局限是摘要未报告每类测试生成的假阳性/假阴性、复现实验预算和跨模型迁移；框架依赖可验证环境，开放式任务难以获得同等强度的参考解。

## 最接近的相关工作

接近 PaperDoctor 的证据指针式 critique、SkillAA 的归因—验证—回滚、Ground-truth-as-code、Continual Search for Long-Horizon RCA 与反事实测试生成。ProbeAgent 的区别是直接以复现来筛选失败原因。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：让生成式 verifier 输出“原因—最小反事实—预期可观察结果—执行证书”，再由独立 runner 回放。可把复现频率蒸馏成序数失败概率，并将不可复现或测试无效的案例标为 T/INCONCLUSIVE。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：以复现率和证书质量校准 critique-level teacher score。
- **A/B/T 与序数分布**：同一原因在反事实中稳定复现为 A，不复现但测试有效为 B，测试本身无效为 T。
- **真值门控**：参考解和自动检查是 critique 写入的硬 gate。
- **critique states**：仅接纳附带可执行测试、环境证据与复现日志的 student critique。
- **高熵分叉**：优先在多个失败原因均可解释的分叉生成最小反事实，以信息增益分配预算。
- **sealed eval**：训练期可见的诊断任务与最终失败模式发现集分离，防止 verifier 学会测试模板。