"""Email service for sending transactional emails"""

import os

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


async def send_verification_email(email: str, token: str):
    """Send email verification email"""
    try:
        # Email configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
            MAIL_FROM=os.getenv("MAIL_FROM", "your-email@gmail.com"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Create verification URL
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        verification_url = f"{frontend_url}/auth/verify-email?token={token}"

        # Create email message
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Bem-vindo ao HireMetrics!</h2>
            <p>Obrigado por se registrar. Para ativar sua conta e começar a usar a plataforma, clique no botão abaixo:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Verificar Email
                </a>
            </div>
            
            <p>Ou copie e cole este link no seu navegador:</p>
            <p style="word-break: break-all; color: #6b7280;">{verification_url}</p>
            
            <p><strong>Importante:</strong></p>
            <ul>
                <li>Este link expira em 24 horas</li>
                <li>Após a verificação, você terá acesso completo à plataforma</li>
                <li>Se você não solicitou este registro, pode ignorar este email</li>
            </ul>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="color: #6b7280; font-size: 14px;">
                Este email foi enviado automaticamente. Não responda a este email.
            </p>
        </div>
        """

        message = MessageSchema(
            subject="Verifique seu email - HireMetrics",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        # Send email
        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print(f"Error sending verification email: {e}")
        raise e


async def send_password_reset_email(email: str, token: str):
    """Send password reset email"""
    try:
        # Email configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
            MAIL_FROM=os.getenv("MAIL_FROM", "your-email@gmail.com"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Create reset URL
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        reset_url = f"{frontend_url}/auth/reset-password/{token}"

        # Create email message
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Redefinir Senha - HireMetrics</h2>
            <p>Você solicitou a redefinição da sua senha. Para criar uma nova senha, clique no botão abaixo:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    Redefinir Senha
                </a>
            </div>
            
            <p>Ou copie e cole este link no seu navegador:</p>
            <p style="word-break: break-all; color: #6b7280;">{reset_url}</p>
            
            <p><strong>Importante:</strong></p>
            <ul>
                <li>Este link expira em 1 hora</li>
                <li>Se você não solicitou esta redefinição, pode ignorar este email</li>
                <li>Sua senha atual permanecerá inalterada se você não clicar no link</li>
            </ul>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="color: #6b7280; font-size: 14px;">
                Este email foi enviado automaticamente. Não responda a este email.
            </p>
        </div>
        """

        message = MessageSchema(
            subject="Redefinir Senha - HireMetrics",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        # Send email
        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print(f"Error sending password reset email: {e}")
        raise e
