import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from Conf.config import smtp_cfg, email_cfg

_FILESIZE = 20  # 单位M， 单个附件大小
_FILECOUNT = 10  # 附件个数
_smtp_cfg = smtp_cfg
_email_cfg = email_cfg
_logger = logging.getLogger('main.email')


class Email:
    def __init__(self, subject, context=None, attachment=None):
        self.subject = subject
        self.context = context
        self.attachment = attachment
        self.message = MIMEMultipart()
        self._message_init()

    def _message_init(self):
        if self.subject:
            self.message['subject'] = Header(self.subject, 'utf-8')  # 邮件标题
        else:
            raise ValueError("Invalid subject")

        self.message['from'] = _email_cfg['sender']  # 发件人
        self.message['to'] = _email_cfg['receivers']  # 收件人

        if self.context:
            self.message.attach(MIMEText(self.context, 'html', 'utf-8'))  # 邮件正文内容

        # 添加附件
        if self.attachment:
            if isinstance(self.attachment, str):
                self._attach(self.attachment)
            elif isinstance(self.attachment, list):
                count = 0
                for each in self.attachment:
                    if count < _FILECOUNT:
                        self._attach(each)
                        count += 1
                    else:
                        _logger.warning('Attachments exceed limit of %d', _FILECOUNT)
                        break

    def _attach(self, file):
        """定义处理附件的方法"""
        if os.path.isfile(file) and os.path.getsize(file) <= _FILESIZE * 1024 * 1024:
            with open(file, 'rb') as f:
                attach = MIMEApplication(f.read())
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            attach["Content-Type"] = 'application/octet-stream'
            self.message.attach(attach)
        else:
            _logger.error('The attachment does not exist or is larger than %dM: %s', _FILESIZE, file)

    def send_mail(self):
        try:
            print("_smtp_cfg['sender']:", _smtp_cfg.get('sender', 'Not Found'))
            print("_email_cfg['sender']:", _email_cfg.get('sender', 'Not Found'))
            print("self.message['from']:", self.message['from'])

            s = smtplib.SMTP_SSL(_smtp_cfg['host'], int(_smtp_cfg['port']))
            s.login(_smtp_cfg['user'], _smtp_cfg['passwd'])
            s.sendmail(_email_cfg['sender'], _email_cfg['receivers'], self.message.as_string())
            s.quit()  # 正确关闭连接
            return True
        except smtplib.SMTPAuthenticationError as e:
            _logger.error('SMTP Authentication Error: %s', e)
        except smtplib.SMTPConnectError as e:
            _logger.error('SMTP Connect Error: %s', e)
        except smtplib.SMTPServerDisconnected as e:
            _logger.error('SMTP Server Disconnected: %s', e)
        except smtplib.SMTPException as e:
            _logger.error('SMTP Exception: %s', e)
        except Exception as e:
            _logger.error('Unexpected Error: %s', e)
        finally:
            try:
                s.quit()
            except:
                pass  # 忽略可能出现的错误
        return False


# 示例用法
title = "测试邮件"
context = "这是一封测试邮件"
file = 'C:\\Users\\yinghai\\PycharmProjects\\TestFrame\\Comm\\data\\baidu_fanyi.xlsx'
mail = Email(title, context, file)
send = mail.send_mail()
print(send)
