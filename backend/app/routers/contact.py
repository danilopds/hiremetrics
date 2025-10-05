"""Contact form endpoint"""
import os
from datetime import datetime

from fastapi import APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from ..schemas import ContactForm, ContactResponse

router = APIRouter()


@router.post("/contact", response_model=ContactResponse)
async def send_contact_email(contact_data: ContactForm):
    """Send contact form email"""
    try:
        # Email configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
            MAIL_FROM=os.getenv(
                "MAIL_FROM", "your-email@gmail.com"
            ),  # Should match MAIL_USERNAME for Gmail
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        # Create email message
        html_content = f"""
        <h2>Nova mensagem de contato - HireMetrics</h2>
        <p><strong>Nome:</strong> {contact_data.name}</p>
        <p><strong>E-mail:</strong> {contact_data.email}</p>
        <p><strong>Empresa:</strong> {contact_data.company or 'Não informado'}</p>
        <p><strong>Assunto:</strong> {contact_data.subject}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{contact_data.message.replace(chr(10), '<br>')}</p>
        <hr>
        <p><small>Enviado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>
        """

        message = MessageSchema(
            subject=f"Contato HireMetrics: {contact_data.subject}",
            recipients=["hiremetrics.contato@gmail.com"],
            body=html_content,
            subtype="html",
        )

        # Send email
        fm = FastMail(conf)
        await fm.send_message(message)

        return ContactResponse(
            success=True,
            message="Mensagem enviada com sucesso! Entraremos em contato em breve.",
        )

    except Exception as e:
        print(f"Error sending contact email: {e}")
        import traceback

        traceback.print_exc()

        # Provide more specific error messages
        error_message = "Erro ao enviar mensagem. Tente novamente ou entre em contato diretamente por e-mail."

        if "Authentication" in str(e):
            error_message = (
                "Erro de autenticação de e-mail. Verifique as credenciais configuradas."
            )
        elif "timeout" in str(e).lower():
            error_message = (
                "Timeout na conexão de e-mail. Verifique a configuração SMTP."
            )
        elif "connection" in str(e).lower():
            error_message = "Erro de conexão com servidor de e-mail. Verifique a configuração de rede."

        return ContactResponse(success=False, message=error_message)

