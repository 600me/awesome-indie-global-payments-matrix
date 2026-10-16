# 【刚性施工令｜无自由裁量执行工单：Doola 与 Firstbase 联盟合作自动化申请】

## 一、唯一物理目标与路径
- **目标**：通过本地运行的独立 AI Chrome 实例（CDP 端口 9222，配置目录 `~/.ai-chrome`），自动化访问并提交 **Doola**（PartnerStack）与 **Firstbase.io** 的官方 Affiliate / Referral 推广合作申请。提取或申请专属推广链接，账号密码及申请状态同步至本地密码库（`/usr/local/bin/ai-pass`）；若获得即时 Referral 链接，自动热更新至美西 VPS（`us-server`）中继网关 `go.272738.xyz`。
- **物理路径**：
  1. 浏览器自动化操作：`agent-browser --cdp 9222` 或 Playwright 连接 `http://127.0.0.1:9222`
  2. 密码库同步：`/usr/local/bin/ai-pass save <domain> <user> <pass/oauth>`
  3. 美西 VPS 中继配置（若取得即时链接）：`us-server:/etc/nginx/sites-available/kais-proxy-links`
  4. 执行记录：追加至本工单末尾

---

## 二、执行硬红线（违反直接判不及格）
1. **优先复用既有 Google OAuth / 密码库铁律**：
   - 登录/注册优先点击 "Continue with Google" 复用 `600megd@gmail.com`。
   - 若平台不支持 Google OAuth 而需独立密码注册：先查 `ai-pass get <domain>`；确认无记录时，使用 `600megd@gmail.com` 配合随机生成的强密码注册，成功后立即执行 `ai-pass save <domain> 600megd@gmail.com "<密码>"` 并读回验证。
   - 严禁向聊天窗口或文档输出真实明文密码。
2. **免询问自动填写标准资料**：
   - 申请人姓名：Kais
   - 邮箱：`600megd@gmail.com`
   - 公司/组织：Kais Studio / Independent Developer
   - 推广载体主页：`https://pay.mybskm.top`
   - 开源矩阵仓库：`https://github.com/600me/awesome-indie-global-payments-matrix`
   - 推广渠道描述：Developer tool & interactive fee calculator, technical guides for non-US software founders and SaaS indie developers on choosing between Merchant of Record and US LLC + Stripe.
   - 勾选条款与协议：免询问直接勾选同意。
3. **资金与信用卡绝对红线**：
   - 严禁任何形式的充值、付费、绑定信用卡或预付款！联盟合作伙伴申请 100% 免费，若遇任何付款要求立即退出并标记。
4. **标签页用完即关铁律**：
   - 每个平台完成操作后，必须通过确定性命令或脚本关闭本次打开的标签页，严禁遗留活动标签。
5. **零等待人工假死锁**：
   - 若申请提交后提示“需官方人工审核（Under Review）”，记录申请提交成功、确认邮件状态后直接推进下一工序，严禁设立 `awaiting_human` 假死锁。

---

## 三、各平台具体实施动作

### 平台 1：Doola Affiliate / Partner（PartnerStack 体系）
- 官方入口：`https://doola.partnerstack.com/`
- 操作流程：
  1. 打开 `https://doola.partnerstack.com/`，查找 "Join the program" / "Sign Up" / "Apply" 入口。
  2. 优先通过 Google OAuth（`600megd@gmail.com`）登录 PartnerStack；若无 Google 登录则使用 `600megd@gmail.com` + 独立强密码注册，存入 `ai-pass save partnerstack.com 600megd@gmail.com <pass>`。
  3. 填写申请表单，填入上述推广载体（`https://pay.mybskm.top`）及推广策略说明。
  4. 提交申请。若即时进入后台生成 Referral 链接（如 `https://doola.partnerstack.com/xxx` 或专属参数），复制保存；若提示审核中，记录确认状态。

### 平台 2：Firstbase.io Referral Partner
- 官方入口：`https://www.firstbase.io/referral-partners`（或其 Rewards 伙伴申请页）
- 操作流程：
  1. 打开 `https://www.firstbase.io/referral-partners`，定位 "Apply Now" / "Become a Partner" 入口。
  2. 优先通过 Google OAuth 或按表单要求提交资料（`600megd@gmail.com`，网站 `https://pay.mybskm.top`）。
  3. 提交申请并记录账号至 `ai-pass save firstbase.io 600megd@gmail.com <pass/oauth>`。
  4. 检查是否即时分配 Referral Code / 链接；若需审核，记录审核状态。

---

## 四、中继热更新与客观验收（若取得即时推荐参数）
1. 若任一平台即时分配专属 Referral 参数：
   - 备份 `us-server:/etc/nginx/sites-available/kais-proxy-links`。
   - 将对应厂商 location 内的 `REPLACE_ME` 替换为真实专属参数。
   - 执行 `ssh us-server 'nginx -t && systemctl reload nginx'`。
   - 通过 `curl -Is https://go.272738.xyz/<vendor>` 验证 302 重定向已带上真实参数。
2. 检查 `ai-pass get doola.com`（或 `partnerstack.com`）与 `ai-pass get firstbase.io` 能读回记录。
3. 检查自动化标签页已全部精准关闭。
4. 将两个平台的最终申请结果（即时获批/审核中/确认凭证）完整记录在工单底部的执行记录中。

---

## 五、交付指令
立即无条件执行上述联盟自动化申请，完成验收后直接退出，严禁设立人工等待。

---

## 六、执行记录｜2026-10-16 23:45 Asia/Shanghai（15:45 UTC）

### Doola：已提交，官方审核中

- 通过 AI Chrome（CDP 9222）的既有 `600megd@gmail.com` PartnerStack 登录态，进入 `https://dash.partnerstack.com/application?company=doola&gref=page`，填写并提交申请。
- 公司填写 `Kais Studio / Independent Developer`，网站填写 `https://pay.mybskm.top`，仓库填写 `https://github.com/600me/awesome-indie-global-payments-matrix`；推广说明包含开发者工具、交互费用计算器、非美国 SaaS 创始人及 MoR 与 US LLC + Stripe 对比。付费广告选 No，视频通话选 No，未虚构历史销量或收入。
- 既有账户的名/姓由平台锁定为 `sccdsd / dfsav`，申请页不允许修改；角色介绍明确填写 “I am Kais”。未另建重复账号，未改动共享账户的全局资料。
- Gmail 已收到 PartnerStack 确认邮件《您加入 doola 的申请》，时间 `2026-10-16T15:40:33Z`，message ID `1a1455f4802ce7a6`，正文摘要明确“申请已收到”“已提交给 doola 审核”。邮件仍为 UNREAD。
- 最终后台首页显示 doola（自动翻译为“杜拉”）“申请待处理”。未取得专属 Referral，因此 `/doola` 尚未热更新，仍含 `REPLACE_ME`，不能视为已具备佣金归因。

### Firstbase.io：既有合作关系已启用，已取得可用 Referral

- 从官方 `https://www.firstbase.io/referral-partners` 跟随入口至 `https://firstbaseio.partnerstack.com/?group=affiliate`，页面显示当前账号已加入 Firstbase.io；复用既有合作关系，没有重复注册或虚报本次新申请获批。
- 后台最初要求接受项目条款。已打开并阅读平台所链接的 `https://www.firstbase.io/terms`，关闭条款标签后勾选并确认；后台显示“已确认服务条款”，条款时间线显示已于 2026-10-16 签署。
- 后台 Summary 与 Links 均显示平台创建的默认推荐链接：`https://get.firstbase.io/slcdxtscxrh7`。最终 PartnerStack 首页显示 Firstbase.io “已启用”。无待填的独立 Firstbase 申请表。
- 本次 Gmail 查询未发现 Firstbase 确认邮件；以已启用的后台状态、已签条款及平台实际分配链接为凭证。

### 密码库同步与读回

- PartnerStack 设置 → 安全页确认邮箱为 `600megd@gmail.com`，Google 身份验证已配置；页面提示需先删除 Google 配置才能设置/更新独立密码。
- 已分别执行 `ai-pass save` 保存 `partnerstack.com`、`doola.com`、`firstbase.io` 的同一邮箱账号、真实 Google OAuth 登录方式及各自申请/合作状态；Firstbase 记录还包含专属链接与中继地址。
- 三条记录均通过 `ai-pass get <domain> --user 600megd@gmail.com --json` 在进程内逐字段读回匹配。保存的是明确注明“无独立密码”的 OAuth 说明，没有编造独立密码，没有导出会话或将真实密码写入本工单/聊天。

### 中继热更新与公网验收

- 已备份美西 VPS 配置至 `us-server:/etc/nginx/sites-available/kais-proxy-links.bak-affiliate-20261016T154307Z`。
- 仅修改 `/firstbase` 的 302 目标为平台实际提供的完整链接 `https://get.firstbase.io/slcdxtscxrh7`，由官方短链生成真实归因参数；未将短链标识误塞入未经证实的 `?ref=` 参数。其他厂商路由未修改。
- `nginx -t` 输出 syntax is ok / test is successful；`systemctl reload nginx` 退出码 0。
- 公网 HEAD 与 GET 验收：`https://go.272738.xyz/firstbase` → HTTP 302，`Location: https://get.firstbase.io/slcdxtscxrh7`，无占位符。
- 官方短链 GET 验收：HTTP 302 → `https://www.firstbase.io/`，带有 `source=6e42338f89bc`、`utm_medium=partnerstack`、`utm_source=affiliate`、`ps_partner_key=NmU0MjMzOGY4OWJj`、`gspk=NmU0MjMzOGY4OWJj` 及每次点击生成的跟踪参数。短链自身 HEAD 返回 404，而实际 GET 正常；没有把 HEAD 结果当作真实访问失败。
- Firstbase 后台显示收入、待处理佣金与已支付佣金均为 0。本次技术验证不代表真实客户访问、成交或佣金到账。

### 收尾验收

- 本次 Doola 标签 ID `D7A38709E92AF24236283AB678CB3688`、Firstbase 标签 ID `31CE230B3612E73CB5749ABCFCC97FA5`、条款标签 ID `00D580FF68791344CBB3FBB72340D0DD` 均已按确切标识关闭；最终检查本任务标签残留为 0，原有其他 4 个页面保持打开。
- 未付款、未充值、未绑定信用卡，未创建开发者云项目或后台调度。
- 工单已执行完毕：Doola 处于平台审核中；Firstbase 合作关系已启用、OAuth 记录已同步、专属中继已热更新并通过公网验收。无需要 Kais 立即处理的步骤。
