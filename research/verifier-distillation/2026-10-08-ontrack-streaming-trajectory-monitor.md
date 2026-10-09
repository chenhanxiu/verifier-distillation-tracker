# OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport

- **作者**：Babak Barazandeh；Connor Swanson；Chinmay Kulkarni；Nikhil Mungel
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12375
- **Canonical URL**：https://arxiv.org/abs/2610.12375
- **代码**：未发现公开代码链接

## 一句话结论

OnTrack 以流式结构匹配在约 1 毫秒/步内判断 Agent 是否偏离成功轨迹，提供了可在线部署的长时程过程 verifier 和早停信号。

## 真正新增的内容

【论文原文】方法不只比较文本相似度，而是同时比较步骤表示与依赖结构，并用流式结构感知最优传输将当前前缀对齐到成功轨迹；支持有完整参考、只有工具 schema、以及没有既有成功轨迹的不同冷启动条件。

【分析推断】它可作为 distributional verifier 的额外通道：输出“离成功流形的距离分布”，与语义 Judge 和环境 oracle 分账。

## 核心方法

1. 将 Agent 轨迹编码为带步骤内容与结构依赖的流式图/序列。
2. 用结构感知 optimal transport 将新前缀与成功参考对齐。
3. 每一步更新偏离分数，供实时告警、干预或早停。
4. 在参考信息逐渐减少的多个制度下评估，检验冷启动适应性。

## 关键实验结果

【论文原文】监控开销约 1 毫秒/步。在 SWE-bench 中，仅观察前 8 步时，失败排序相对内容相似度提高 0.057 AUROC；使用早停策略约节省 18% 计算，被中断轨迹中 83%（5/6）确实失败。

## 证据质量与局限

【论文原文】报告了在线成本、早期预测和资源节省，指标与实际 Agent 运维相关。  
【局限】5/6 的中断样本规模很小；成功轨迹可能不是唯一正确结构，结构距离会惩罚新颖但有效的策略。SWE-bench 结果不能自动泛化到开放世界工具环境。

## 最接近的相关工作

与 DynSTEER、STRIDE、DENSE、FARM、Speculative Uncertainty、Continual Search for Long-Horizon RCA 和 BATON 最接近。OnTrack 的独特贡献是低延迟的流式结构对齐。

## 如何复用或推进 LLM-as-a-Verifier

将 OnTrack 距离作为独立特征送入序数 verifier：低偏离不直接判“正确”，高偏离也不直接判“失败”；只有与环境约束、未完成义务和结果 oracle 一致时才触发硬干预。可蒸馏成功/失败轨迹的距离分布，而非单点阈值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把结构偏离分数作为过程级辅助目标，与 outcome score 分开校准。
- **A/B/T 与序数分布**：对齐明确且有可验证参考时输出 A/B；多路径都合理或参考缺失时提高 T。
- **程序化/环境真值门控**：结构相似度不能覆盖执行真值，早停前必须检查硬约束和可恢复性。
- **student-generated critique states**：在偏离突增点生成 critique，包含对应参考步骤、依赖差异和环境证据。
- **高熵分叉**：对新颖分支设探索豁免；若未违反硬约束，不因远离历史成功轨迹立即裁剪。
- **sealed eval**：用未进入参考库的新任务/新成功策略测试，防止 monitor 只记住成功模板。

总体判断：【分析推断】OnTrack 值得作为在线低成本 routing head，但不应成为唯一 verifier；最佳角色是“触发重检/干预”的结构告警器。