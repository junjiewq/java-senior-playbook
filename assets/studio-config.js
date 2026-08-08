/**
 * 公众号 / H5 合体页用的 Studio 公网地址配置。
 *
 * 填写示例（二选一）：
 *   1) 稳定域名：https://studio.example.com
 *   2) 临时隧道：https://xxxx.trycloudflare.com  （本机 bash scripts/remote-access.sh）
 *
 * 也可用 wechat.html?studio=https://… 或页面内「粘贴 Studio 地址」写入本机 localStorage。
 * 勿把 API Key / AGENT_WS_TOKEN 写进本文件并提交公开仓库。
 */
window.PLAYBOOK_STUDIO = {
  /** @type {string} 公网 HTTPS Studio 根地址，末尾不要斜杠也可 */
  publicStudioUrl: "",
  /** 打开对话时附加的 query（embed=1 为微信轻量壳） */
  chatQuery: "embed=1",
};
