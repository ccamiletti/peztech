import email
import smtplib
import datetime
import logging
import pytz

from email.mime.text import MIMEText
from email.header import Header
from pezInterface.models import Centro, CentroDestinatario

# Get an instance of a logger
logger = logging.getLogger(__name__)


def send_notification(desc_video, url_upload):
    # email_content = (''.join("""
    email_content = f"""
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Notificación - PezTech</title>
        </head>
        <body style="-webkit-text-size-adjust: none; box-sizing: border-box; color: #74787E; 
            font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; height: 100%; line-height: 1.4; 
            margin: 0; width: 100% !important;" bgcolor="#F2F4F6">
            <table width="100%" cellpadding="0" cellspacing="0" style="box-sizing: border-box; 
                font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; margin: 0; padding: 0; 
                width: 100%;" bgcolor="#F2F4F6">
                <tr>
                    <td align="center" style="box-sizing: border-box; word-break: break-word; 
                        font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; ">
                        <table class="email-content" width="100%" cellpadding="0" cellspacing="0" 
                            style="box-sizing: border-box; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                margin: 0; padding: 0; width: 100%;">
                            <tr>
                                <td class="email-masthead" style="box-sizing: border-box; 
                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                    padding: 25px 0; word-break: break-word;" align="center">
                                    <a href="#" class="email-masthead_name" style="box-sizing: border-box; 
                                        color: #bbbfc3; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                        font-size: 16px; font-weight: bold; text-decoration: none; 
                                        text-shadow: 0 1px 0 white;">
                                        PezTech - Notificación
                                    </a>
                                </td>
                            </tr>
                            
                            <tr>
                                <td class="email-body" width="100%" cellspacing="0" 
                                    style="-premailer-cellpadding: 0; -premailer-cellspacing: 0; 
                                        border-bottom-color: #EDEFF2; border-bottom-style: solid; 
                                        border-bottom-width: 1px; border-top-color: #EDEFF2; border-top-style: solid; 
                                        border-top-width: 1px; box-sizing: border-box; 
                                        font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                        margin: 0; padding: 0; width: 100%; word-break: break-word;" bgcolor="#FFFFFF">
                                    <table class="email-body_inner" align="center" width="570" cellpadding="0" 
                                        cellspacing="0" 
                                        style="box-sizing: border-box; margin: 0 auto; padding: 0; width: 570px; 
                                            font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;" 
                                            bgcolor="#FFFFFF">
                                        <tr>
                                            <td class="content-cell" style="box-sizing: border-box; 
                                                font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                padding: 35px; word-break: break-word;">
                                                <h1 style="box-sizing: border-box; color: #2F3133; 
                                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                    font-size: 19px; font-weight: bold; margin-top: 0;" align="left">
                                                    Hola,
                                                </h1>
                                                <p style="box-sizing: border-box; color: #74787E; 
                                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                    font-size: 16px; line-height: 1.5em; margin-top: 0;" align="left">
                                                    Recientemente se cargó video Necropsia: <b>{desc_video}</b>, 
                                                    <strong style = "font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;">
                                                       puede ver el video online con la cuenta otorgada por soporte 
                                                        AzurTech en el siguiente enlace.
                                                    </strong>
                                                </p>
                                                <table class="body-action" align="center" width="100%" cellpadding="0" 
                                                    cellspacing="0" 
                                                    style="box-sizing: border-box; 
                                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                    margin: 30px auto; padding: 0; text-align: center; width: 100%;">
                                                    <tr>
                                                        <td align="center" style="box-sizing: border-box; 
                                                            font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                            word-break: break-word;">
                                                            <table width="100%" border="0" cellspacing="0" 
                                                                cellpadding="0" style="box-sizing: border-box; 
                                                                font-family: Arial, 'Helvetica Neue', Helvetica, 
                                                                sans-serif;">
                                                                <tr>
                                                                    <td align="center" style="box-sizing: border-box; 
                                                                        font-family: Arial, 'Helvetica Neue', Helvetica, 
                                                                        sans-serif; word-break: break-word;">
                                                                        <table border="0" cellspacing="0" cellpadding="0" 
                                                                            style="box-sizing: border-box; 
                                                                            font-family: Arial, 'Helvetica Neue', 
                                                                                Helvetica, sans-serif;">
                                                                            <tr>
                                                                                <td style="box-sizing: border-box; 
                                                                                    font-family: Arial, 'Helvetica Neue', 
                                                                                    Helvetica, sans-serif; 
                                                                                    word-break: break-word;">
                                                                                    <a href="{url_upload}" class="button button--green" 
                                                                                        target="_blank" 
                                                                                        style="-webkit-text-size-adjust: none; 
                                                                                        background: #22BC66; 
                                                                                        border-color: #22bc66;
                                                                                        border-radius: 3px; 
                                                                                        border-style: solid; 
                                                                                        border-width: 10px 18px; 
                                                                                        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.16); 
                                                                                        box-sizing: border-box; 
                                                                                        color: #FFF; display: inline-block; 
                                                                                        font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                                                        text-decoration: none;">
                                                                                        Ver Video
                                                                                    </a>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                <p style="box-sizing: border-box; color: #74787E; 
                                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                    font-size: 16px; line-height: 1.5em; margin-top: 0;" align="left">
                                                    Atte,
                                                    <br />
                                                    <b>Equipo de soporte</b>
                                                    <br />
                                                </p>
                                                <img src="https://www.azurtech.cl/wp-content/uploads/2020/10/peztech.png" 
                                                    alt="Simply Easy Learning" height="60">
                                                <p style="box-sizing: border-box; color: #74787E; 
                                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                    font-size: 14px; line-height: 1.5em; margin-top: 0;" align="left">
                                                    <br />
                                                    <b>Santa Rosa 575 OF 31, Puerto Varas. Edificio Central Lake – Casa Matriz</b>
                                                    <br />
                                                    <b>T. Fijo:</b> 65 – 2201901 / 65 -2637315
                                                    <br />
                                                    <b>E-mail:</b>
                                                    <a href = "mailto: soporte.peztech@azurtech.cl">soporte.peztech@azurtech.cl</a>
                                                    <br />
                                                    <b>Teams:</b>
                                                    <a href = "mailto: atencion.clientes@azurtech.cl">atencion.clientes@azurtech.cl</a>
                                                    <br />
                                                    <b><a href="https://www.azurtech.cl" target="_blank">www.azurtech.cl</a></b>
                                                </p>
                                            </td>       
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td style="box-sizing: border-box; 
                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; word-break: break-word;">
                                    <table class="email-footer" align="center" width="570" cellpadding="0" 
                                        cellspacing="0" style="box-sizing: border-box; 
                                        font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; margin: 0 auto;
                                        padding: 0; text-align: center; width: 570px;">
                                        <tr>
                                            <td class="content-cell" align="center" style="box-sizing: border-box; 
                                                font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                padding: 35px; word-break: break-word;">
                                                <p class="sub align-center" style="box-sizing: border-box; 
                                                    color: #AEAEAE; 
                                                    font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
                                                    font-size: 12px; line-height: 1.5em; margin-top: 0;" align="center">
                                                     PezTech - Todos los derechos reservados. - Tecnología de AzurTech
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <!-- top message -->
                    </td>
                </tr>
            </table>
            <!-- wrapper -->
        </body>
    </html>
    """.encode("utf-8")
    # """)).encode("utf-8")

    centro_data = Centro.objects.all()
    destinatario_data = CentroDestinatario.objects.all()

    if centro_data and destinatario_data:
        id_centro = centro_data[0].id
        smtp_host = centro_data[0].smtpHost
        smtp_usuario = centro_data[0].smtpUsuario
        smtp_contrasena = centro_data[0].smtpContrasena
        smtp_puerto = centro_data[0].smtpPuerto
        centro_nombre = centro_data[0].nombre

        now_cl = datetime.datetime.now(pytz.timezone('America/Santiago'))
        now_cl_date = now_cl.strftime("%Y-%m-%d")
        now_cl_hour = now_cl.strftime("%H:%M")
        asunto = "Notificación: " + centro_nombre+" - "+now_cl_date+" "+now_cl_hour+" - Necropsia"

        destinatarios = CentroDestinatario.objects.all().filter(centro_id=id_centro)

        for dest in destinatarios:
            logger.info("UPLOAD MS: Email destinatario: " + dest.email)
            print("UPLOAD MS: Email destinatario: " + dest.email)

            # msg = email.message.Message()
            msg = MIMEText(email_content, 'plain', 'utf-8')
            # msg = email.message.Message()
            msg['Subject'] = Header(asunto, 'utf-8')

            msg['From'] = smtp_usuario
            msg['To'] = dest.email
            password = smtp_contrasena
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)

            s = smtplib.SMTP(smtp_host, smtp_puerto)
            s.starttls()

            # Login Credentials for sending the mail
            s.login(smtp_usuario, password)

            logger.info("UPLOAD MS: Enviando Email")
            print("UPLOAD MS: Enviando Email")
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.close()
    else:
        logger.warning("UPLOAD MS: NO VIENE DATO DEL CENTRO")
        print("UPLOAD MS: NO VIENE DATO DEL CENTRO")

# send_notification("NOMBRE DE PRUEBA")
