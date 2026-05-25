"""文件职责：提供 SMTP 邮件发送能力，支持 mock 模式，不处理认证编排逻辑。"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailSendError(Exception):
    """邮件发送失败。"""


class EmailService:
    """邮件服务。"""

    def __init__(self) -> None:
        self._mock = not settings.smtp_host

    def send_reset_password_email(self, *, to: str, reset_link: str) -> None:
        """发送重置密码邮件。"""
        subject = "Serenova - 密码重置"
        html_body = self._build_reset_password_html(reset_link)

        if self._mock:
            logger.info(
                "[MOCK 邮件] 收件人: %s | 主题: %s | 重置链接: %s",
                to,
                subject,
                reset_link,
            )
            return

        self._send_email(to=to, subject=subject, html_body=html_body)

    def _send_email(self, *, to: str, subject: str, html_body: str) -> None:
        """通过 SMTP 发送邮件。"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.smtp_from or settings.smtp_user
        msg["To"] = to
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            if settings.smtp_use_tls:
                server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)

            if settings.smtp_user and settings.smtp_pass:
                server.login(settings.smtp_user, settings.smtp_pass)

            server.sendmail(msg["From"], [to], msg.as_string())
            server.quit()
        except Exception as exc:
            logger.error("邮件发送失败: %s", exc)
            raise EmailSendError(f"邮件发送失败: {exc}") from exc

    @staticmethod
    def _build_reset_password_html(reset_link: str) -> str:
        """构建重置密码邮件 HTML 内容。"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f4f8; padding: 40px 20px;">
          <div style="max-width: 480px; margin: 0 auto; background: #ffffff; border-radius: 16px; padding: 32px; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
            <h2 style="color: #0f172a; margin: 0 0 16px;">密码重置</h2>
            <p style="color: #475569; line-height: 1.6; margin: 0 0 24px;">
              你好，你正在重置 Serenova 账号的密码。请点击下方按钮完成重置，链接有效期为 <strong>{settings.reset_token_expire_minutes} 分钟</strong>。
            </p>
            <a href="{reset_link}"
               style="display: inline-block; background: linear-gradient(180deg, rgba(59,130,246,0.96), rgba(37,99,235,0.9)); color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 12px; font-weight: 600; font-size: 16px;">
              重置密码
            </a>
            <p style="color: #94a3b8; font-size: 13px; margin: 24px 0 0;">
              如果你没有发起此请求，请忽略此邮件，你的密码不会被更改。
            </p>
          </div>
        </body>
        </html>
        """
