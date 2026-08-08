/**
 * 公众号 / H5 合体页用的 Studio 公网地址配置。
 *
 * 目标拓扑（域名审核通过并完成解析后）：
 *   Hub（Pages 自定义域）：https://xjj985.top/wechat.html
 *   Studio（cloudflared 命名隧道）：https://chat.xjj985.top
 *
 * 审核期间临时方案：
 *   Hub：https://junjiewq.github.io/java-senior-playbook/wechat.html
 *   Studio：本机 bash scripts/remote-access.sh 打印的 https://….trycloudflare.com
 *           用 wechat.html?studio=… 或页面内粘贴覆盖下方默认值。
 *
 * 也可用 wechat.html?studio=https://… 或页面内「粘贴 Studio 地址」写入本机 localStorage。
 * 勿把 API Key / AGENT_WS_TOKEN 写进本文件并提交公开仓库。
 */
window.PLAYBOOK_STUDIO = {
  /** @type {string} 公网 HTTPS Studio 根地址，末尾不要斜杠也可 */
  publicStudioUrl: "https://chat.xjj985.top",
  /** 打开对话时附加的 query（embed=1 为微信轻量壳） */
  chatQuery: "embed=1",
};
