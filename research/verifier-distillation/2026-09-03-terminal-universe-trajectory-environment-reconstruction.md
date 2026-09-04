# Terminal-Universe: Turning Agent Trajectories into Scalable Terminal Environments

## 基本信息

- **作者**：Jie Wu, Zhenru Zhang, Beichen Zhang, Xuwu Wang, Yuhui Su, Mouxiang Chen, Peng Wang, Zhihai Wang, Que Shen, Hao Zhou, An Yang, Fei Huang, Yujiu Yang, Dayiheng Liu
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **原始论文**：https://arxiv.org/abs/2609.04148
- **代码**：公开页未提供
- **arXiv**：2609.04148
- **DOI**：https://doi.org/10.48550/arXiv.2609.04148

## 一句话结论

Terminal-Universe 不把历史 Agent 轨迹仅当静态示范，而是逆向恢复为可重复查询、可执行验证的环境，并产出 37.3k 个 task-sufficient workspaces。

## 真正新增的内容

**论文原文结论**：从工具执行历史恢复文件修改前状态，由 completion agent 补齐缺失文件/依赖，再重建原任务和合成跨 workspace、多轮任务。

**分析推断**：它为 Agent verifier × OPD 提供了高杠杆数据引擎：旧轨迹可以转为有环境真值、可生成局部反事实 A/B/T 的 on-policy playground，而不是只做行为克隆。

## 核心方法

- 逆向重放轨迹中的文件操作，恢复 agent 修改前的部分 workspace。
- completion agent 补齐缺失文件与依赖，形成 task-sufficient environment。
- 重建原始意图任务，并在恢复环境上合成新任务。
- breadth 方向通过依赖关系生成跨代码库任务；depth 方向用 user agent 扩展为多轮需求演化会话。

## 关键实验结果

- 从公开 terminal-agent trajectories 生成 **37.3k** 个 task-sufficient environments。
- Qwen3.5-27B 在该语料 SFT 后，Terminal-Bench 2.1 单轮性能提升 **11.9 点**。
- EvoCode-Bench v2 多轮 MT@4 提升 **13.8 点**。
- 摘要没有报告环境重建的独立错误率、verifier 精确率或 sealed contamination 审计。

## 证据质量与局限

- **质量：中高。** 数据规模大，含单轮和多轮下游结果。
- completion agent 补齐内容可能引入与原环境不一致的隐变量；“task-sufficient”不等于完全重建。
- 下游只报告 SFT 收益，尚未直接验证 verifier distillation、score-level OPD 或反事实信用分配。
- 从公开轨迹恢复的环境可能与常用评测仓库重叠，sealed eval 需做代码与任务谱系去重。

## 最接近的相关工作

与 CLI-Universe、EnvHarness、FACET、ToolGate、LongWoF-Bench 和 AgentMercury 的可执行环境/任务生成最接近。不同点是它从已有轨迹反演可复用环境，而不是主要从规范或新生成任务出发。

## 如何复用或推进 LLM-as-a-Verifier

- 在恢复 workspace 中从同一 prefix fork 多个动作，运行测试与状态 diff，生成带硬真值的局部 A/B/T。
- 将执行 receipt、测试覆盖、副作用和多轮约束编译成分项 rubric，再蒸馏给轻量 verifier。
- 用 student 自生成 critique 提议要检查的文件/测试；环境执行决定 critique 是否准入。
- 把“补齐环境的不确定性”作为 verifier 输入特征，而不是默认环境完美。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：可直接在 student rollout 状态上查询 teacher，并以真实执行差值决定梯度方向。
- **A/B/T 与序数分布**：测试差值、需求覆盖和副作用共同生成序数评分；结果近似或证据不足时保留 Tie。
- **真值门控**：测试、构建、文件状态和用户约束为不可覆盖的 teacher gate。
- **critique states**：只保留能预测失败测试、定位文件或推动后续修复的 critique。
- **高熵探索**：环境可重复重放，使高熵分叉能被并行保留和事后验证。
- **sealed eval**：按原始轨迹、仓库、依赖谱系隔离，严禁由同一恢复环境的近邻任务同时进入训练和 sealed 集。