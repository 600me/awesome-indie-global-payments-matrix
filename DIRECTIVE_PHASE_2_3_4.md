# 【刚性施工令｜无自由裁量执行工单：Phase 2, 3, 4 全网发布与矩阵闭环】

## 一、唯一物理目标与路径
- **目标**：将《出海开发者收单与合规通道中继》（`kais-global-payments-matrix`）完成全网发布与基建三件套闭环，包括：
  1. 在 GitHub（`600me`）创建开源公开仓库 `awesome-indie-global-payments-matrix` 并推送代码；
  2. 使用 Codex 既有配置的 Cloudflare 自动化为 `mybskm.top` 添加 A 记录 `pay` ➔ `96.9.225.9`；
  3. 在美西 VPS（`us-server`）部署 `pay.mybskm.top` 静态看板，运行 Certbot 自动化申请 Let's Encrypt SSL 证书（公网 HTTPS 200）；
  4. 在美西 VPS `go.272738.xyz` 扩充 5 大中继路由桩（`doola`, `firstbase`, `lemonsqueezy`, `paddle`, `wise`）并 reload Nginx；
  5. 打通三大技术资产（Proxy / GPU / Payments）网页导航与 GitHub README 互链。
- **物理交付路径**：
  - 本地 Git 仓库：`/Users/a600/project-workspaces(项目工作区)/kais-global-payments-matrix/`
  - GitHub 远端：`git@github.com:600me/awesome-indie-global-payments-matrix.git`
  - 美西 VPS 站点目录：`us-server:/var/www/kais-payments-matrix/index.html`
  - 美西 VPS Nginx 配置：`us-server:/etc/nginx/sites-available/kais-payments-matrix`
  - 美西 VPS 中继配置：`us-server:/etc/nginx/sites-available/kais-proxy-links`
  - 互链资产：
    - `proxy.mybskm.top`（本地及 VPS `/var/www/kais-proxy-benchmark/index.html`）
    - `gpu.mybskm.top`（本地及 VPS `/var/www/kais-gpu-benchmark/index.html`）
    - 三大仓库 README.md 底部互链

---

## 二、执行硬红线（违反直接判不及格）
1. **零等待人工假死锁**：
   - 严禁创建任何 `awaiting_human` 标志或停留在原地等待人工确认！所有工序必须自动推进，客观指标全绿直接结束。
2. **Cloudflare 自动化解析铁律**：
   - 用户明确指示：**Cloudflare 已在 Codex 环境中配置**。必须使用既有 Cloudflare 连接器/API/工具，为 `mybskm.top` 添加 A 记录：`pay` ➔ `96.9.225.9`（DNS-only / 灰云，TTL 60 或自动）。
   - 严禁要求 Kais 手动前往控制台添加解析。
3. **VPS 中继平滑扩充与零破坏**：
   - 修改 `/etc/nginx/sites-available/kais-proxy-links` 前必须创建带时间戳的备份。
   - 只能在 `server_name go.272738.xyz;` 块内追加 5 个 location，严禁破坏既有的 Smartproxy、Bright Data、Apify、Oxylabs、RunPod、Vast.ai 等既有中继路由！
   - 修改后必须 `ssh us-server 'nginx -t'` 验证退出码为 0 后方可 `systemctl reload nginx`。
4. **Certbot 自动化非交互**：
   - 使用标准非交互命令：
     `ssh us-server 'certbot --nginx -d pay.mybskm.top --non-interactive --agree-tos -m 600megd@gmail.com --redirect'`
   - 严禁出现交互式挂起。
5. **GitHub 独立部署公钥**：
   - 鉴于 GitHub 限制同一公钥不能用于多个仓库的 Deploy Key，生成独立的 `~/.ssh/id_ed25519_payments_matrix` 并通过 AI Chrome 或 GitHub API 添加到仓库，在本地仓库配置 `git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_payments_matrix -F /dev/null"`，保证 `git push -u origin main` 顺畅成功。

---

## 三、具体实施步骤

### 任务 1：Cloudflare DNS A 记录添加
- 为 `mybskm.top` 添加 A 记录：`pay` ➔ `96.9.225.9` (DNS-only)。
- 验证解析：`dig +short pay.mybskm.top @8.8.8.8` 返回 `96.9.225.9`。

### 任务 2：美西 VPS 静态站点部署与 Nginx 虚拟主机
- SSH 到 `us-server`：
  - 创建目录 `/var/www/kais-payments-matrix`。
  - 通过 rsync 或 scp 将本地 `web/index.html` 同步到 `/var/www/kais-payments-matrix/index.html`。
  - 写入 `/etc/nginx/sites-available/kais-payments-matrix`：
    ```nginx
    server {
        server_name pay.mybskm.top;
        root /var/www/kais-payments-matrix;
        index index.html;
        charset utf-8;
        add_header X-Content-Type-Options nosniff always;
        location / { try_files $uri $uri/ =404; }
        listen 80;
    }
    ```
  - 建立软链到 `/etc/nginx/sites-enabled/` 并测试 `nginx -t` 与 `systemctl reload nginx`。

### 任务 3：Certbot 自动化签发 SSL 并升级 HTTPS
- 在 `us-server` 运行：
  `certbot --nginx -d pay.mybskm.top --non-interactive --agree-tos -m 600megd@gmail.com --redirect`
- 测试 `nginx -t` 并 `systemctl reload nginx`。
- 验证 `curl -Is https://pay.mybskm.top` 返回 `HTTP/2 200` 或 `HTTP/1.1 200`。

### 任务 4：美西 VPS `go.272738.xyz` 扩充 5 大中继
- 在 `us-server` 的 `/etc/nginx/sites-available/kais-proxy-links` 中追加：
  ```nginx
    location = /doola { return 302 "https://www.doola.com/?ref=REPLACE_ME&utm_source=github&utm_campaign=payments_matrix"; }
    location = /firstbase { return 302 "https://www.firstbase.io/?ref=REPLACE_ME&utm_source=github&utm_campaign=payments_matrix"; }
    location = /lemonsqueezy { return 302 "https://www.lemonsqueezy.com/?ref=REPLACE_ME&utm_source=github&utm_campaign=payments_matrix"; }
    location = /paddle { return 302 "https://www.paddle.com/?ref=REPLACE_ME&utm_source=github&utm_campaign=payments_matrix"; }
    location = /wise { return 302 "https://wise.com/us/business/?ref=REPLACE_ME&utm_source=github&utm_campaign=payments_matrix"; }
  ```
- 测试 `nginx -t && systemctl reload nginx`。
- 验证 5 条中继均返回 302 重定向。

### 任务 5：GitHub 仓库关联与远端推送
- 在 GitHub 组织/用户 `600me` 创建公开仓库 `awesome-indie-global-payments-matrix`。
- 初始化本地 git，添加全部文件，提交并推送到远端 `main` 分支。
- 验证 `curl -Is https://github.com/600me/awesome-indie-global-payments-matrix` 返回 HTTP 200。

### 任务 6：三大技术资产互相打通（矩阵协同）
- 在 `proxy.mybskm.top`（本地及 VPS `/var/www/kais-proxy-benchmark/index.html`）、`gpu.mybskm.top`（本地及 VPS `/var/www/kais-gpu-benchmark/index.html`）的页眉/页脚或资源区添加指向 `https://pay.mybskm.top` 的外链。
- 确认三个站点的互链完全打通，实现基建三件套互相引流。

---

## 四、客观验收指令（必须全部通过）
1. `dig +short pay.mybskm.top @8.8.8.8`：返回 `96.9.225.9`。
2. `ssh us-server 'nginx -t'`：退出码为 0。
3. `curl -Is https://pay.mybskm.top | grep -E "HTTP/|location:"`：返回 `200 OK`。
4. 验证 5 大中继：
   - `curl -Is https://go.272738.xyz/doola | grep -E "HTTP/|location:"` 返回 302 且包含 doola.com
   - `curl -Is https://go.272738.xyz/firstbase | grep -E "HTTP/|location:"` 返回 302 且包含 firstbase.io
   - `curl -Is https://go.272738.xyz/lemonsqueezy | grep -E "HTTP/|location:"` 返回 302 且包含 lemonsqueezy.com
   - `curl -Is https://go.272738.xyz/paddle | grep -E "HTTP/|location:"` 返回 302 且包含 paddle.com
   - `curl -Is https://go.272738.xyz/wise | grep -E "HTTP/|location:"` 返回 302 且包含 wise.com
5. 既有中继不被破坏：
   - `curl -Is https://go.272738.xyz/smartproxy` 返回 301
   - `curl -Is https://go.272738.xyz/runpod` 返回 302
6. `curl -Is https://github.com/600me/awesome-indie-global-payments-matrix | head -n 5`：返回 HTTP 200。

---

## 五、交付指令
立即无条件执行上述工程落地与全网发布，完成验收后直接退出，绝不输出“建议等待人工确认”。
