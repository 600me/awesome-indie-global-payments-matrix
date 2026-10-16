# 【刚性施工令｜无自由裁量执行工单】

## 一、唯一物理目标与路径
- **目标**：在 `/Users/a600/project-workspaces(项目工作区)/kais-global-payments-matrix/` 目录下，单次物理闭环完成 Phase 1 全部落地代码与静态资产，并确保本地客观验收测试退出码为 0。
- **物理交付路径（严格限于以下 3 个最简文件，严禁新增其他多层目录、抽象层或中间件）**：
  1. `web/index.html`：单文件纯静态 Web 费率与合规计算器看板（暗黑极客风，内嵌 CSS 与原生 JS）。
  2. `README.md`：高权重全球技术社区 GitHub 决策矩阵文档（全英文，含痛点、算术模型、对比大表与互链）。
  3. `.gitignore`：标准忽略文件。

---

## 二、执行硬红线（违反直接判不及格）
1. **文案主权与商业常识三要素**：
   - 严禁将 `README.md` 简化为干瘪的 API 调试日志或单调代码文档！
   - 必须包含商业常识三要素：
     - 【痛点痛击】：直击非美独立开发者在 Stripe 遇到的“无实体代开被封号 120 天并冻结资金”、欧盟/美国 40+ 州复杂销售税（Sales Tax / VAT）合规暴雷等真实生产痛点；
     - 【金额与成本精准算例】：列出低流水（\$1,000/月）、临界流水（\$7,500/月）、高流水（\$20,000/月）在不同客单价下的 MoR vs 原生 Stripe + LLC 的透明账本对照；
     - 【对比大表与明确行动出口】：完整涵盖 Lemon Squeezy, Paddle, Stripe + US LLC (Doola), Wise Business 的横向对比，保留精确带参中继跳转链接。
2. **零等待人工假死锁**：
   - 严禁创建任何 `awaiting_human` 标志或停留在原地等待人类确认！所有代码、静态页与文档必须单次执行完毕。
3. **最简物理路径与单文件原则**：
   - Web 看板全部逻辑收敛在 `web/index.html` 单文件内（零 npm 依赖、零构建工具、纯原生 HTML/CSS/JS）。
   - 严禁引入 Node.js 后端、React/Vue 复杂工程化框架、SQLite、Redis 或任何常驻守护进程。
4. **算术模型客观真实铁律（采纳跨模型讨论共识）**：
   - 严禁单凭流水得出粗暴省钱结论！必须引入平均客单价（AOV）与美国 LLC 年度维持固定合规成本（预设 \$1,000/年，即 \$83.33/月），计算真实盈亏平衡点：
     $$\text{月交易笔数 } N = \frac{\text{MRR}}{\text{AOV}}$$
     $$\text{MoR 费用} = \text{MRR} \times 5\% + N \times \$0.50$$
     $$\text{Stripe 原生费用} = \text{MRR} \times 2.9\% + N \times \$0.30$$
     $$\text{自营总成本} = \text{Stripe 原生费用} + \$83.33 \text{（LLC 年报/税表摊销）}$$
     $$\text{净差额} = \text{MoR 费用} - \text{自营总成本}$$
   - 当净差额 $\le 0$ 时，高亮推荐 MoR（早期首选，0 合规包袱）；当净差额 $> 0$ 时，高亮推荐 Doola 设立 US LLC + Stripe（规模化盈利首选）。
5. **商业中继桩 1:1 锚定（严禁擅改）**：
   所有外链落地页必须严格使用解耦网关：
   - Doola: `https://go.272738.xyz/doola`
   - Firstbase: `https://go.272738.xyz/firstbase`
   - Lemon Squeezy: `https://go.272738.xyz/lemonsqueezy`
   - Paddle: `https://go.272738.xyz/paddle`
   - Wise: `https://go.272738.xyz/wise`

---

## 三、各交付文件核心规范

### 1. `web/index.html`（极客暗黑风单页计算器）：
- **设计风格**：顶级暗黑极客风（Dark Mode, `#0a0a0c` 背景，深灰卡片 `#141418`，高对比度荧光青 `#00f2fe` / 琥珀橙 `#f59e0b` / 翡翠绿 `#10b981` 强调色，极简等宽数字字体）。
- **交互组件**：
  - **月流水滑块（MRR）**：范围 \$500 ~ \$50,000，步长 \$100，默认 \$8,000。
  - **平均客单价滑块（AOV）**：范围 \$5 ~ \$500，步长 \$5，默认 \$40。
  - **LLC 年度合规预算折叠设置**：默认 \$1,000/年（透明注明包含 Franchise Tax, Registered Agent, IRS 5472/1120 申报）。
  - **实时结果看板**：
    - 三列高保真卡片：Lemon Squeezy (MoR)、Paddle (MoR)、US LLC + Stripe (Doola 办理)；
    - 动态展示：月度手续费、年化总费用、明细构成（百分比费率 vs 每笔交易费 vs 合规固定费）；
    - 动态差额与胜出者徽章（"Early Stage Winner" 或 "Scale Winner - Saves $X/yr"）；
    - 醒目行动按钮（"Get Doola Discount" / "Open Lemon Squeezy" 等，直接跳转上述中继链接）。
- **URL Query 双向响应（自传播特性）**：
  - 页面初次加载时检查 `window.location.search`，支持 `?mrr=8000&aov=40` 初始化滑块数值；
  - 滑块拖动时通过 `history.replaceState` 实时更新 URL Query，并提供“Copy Shareable Link”一键复制按钮。
- **自包含与免责声明**：
  - 包含移动端响应式布局适配；
  - 页脚包含客观免责声明（Independent comparison tool, not financial advice, verified 2026）。

### 2. `README.md`（GitHub 顶级权威评测文档）：
- 全英文高权重结构：
  1. **Hero Title & One-sentence Value**：*Awesome Indie Global Payments Matrix: MoR (Lemon Squeezy, Paddle) vs US LLC + Stripe (Doola, Firstbase) — Interactive Fee Calculator & Compliance Guide for Non-US Founders*.
  2. **Core Pain Points Solved**：
     - Non-US founder Stripe bans: Why buying fake accounts is suicide (120-day fund hold).
     - Global Sales Tax / VAT compliance hell in 2026.
  3. **The Real Math: MoR vs Stripe + US LLC**：
     - Detailed formula & 3 transparent scenarios (Micro SaaS $1k MRR, Growing Tool $8k MRR, High Volume $25k MRR).
     - The true breakeven calculation including LLC annual franchise tax & IRS filing.
  4. **The Complete Comparison Matrix (Table)**：
     - Provider, Type, Processing Fee, Payout Speed, Sales Tax/VAT Handling, Invoicing, US Entity Required, Best For, Setup Link.
  5. **Interactive Web Calculator Link**：
     - 指向 `https://pay.mybskm.top`（提供即时测算）。
  6. **Sister Projects (Matrix Interlinks)**：
     - Proxy Infrastructure Benchmark: `https://proxy.mybskm.top`
     - Global GPU Cloud Benchmark: `https://gpu.mybskm.top`

### 3. `.gitignore`：
- 标准忽略配置（`.DS_Store`, `*.log`, `.env` 等）。

---

## 四、客观验收指令（必须在工单结束前自行验证）
在工单完成时，必须确保以下客观命令全部通过：
1. `test -f web/index.html && test -f README.md && test -f .gitignore`：文件全部存在。
2. `grep -q "https://go.272738.xyz/doola" web/index.html README.md`：中继链接 100% 准确埋入。
3. `grep -q "https://go.272738.xyz/lemonsqueezy" web/index.html README.md`：中继链接 100% 准确埋入。
4. HTML 文件大小检查：`wc -c web/index.html` 必须 > 3000 字节，确保 UI 与 JS 计算逻辑完整非空。

---

## 五、交付指令
立即无条件执行上述工程落地，完成全部代码编写与文件创建。完成后直接退出，绝不输出“建议等待人工确认”。
