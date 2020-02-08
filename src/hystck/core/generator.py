import sys
import logging
import random
import time
import yaml

from hystck.utility.logger_helper import create_logger
from hystck.application.mail_interface import MailAccount
from hystck.application.mail_interface import Mail
from hystck.application.mail_interface import send_mail



class Generator(object):
    """

    """

    def __init__(self, guest, path, logger=None):
        """

        :param guest:
        :param path:
        :param logger:
        """
        self.guest = guest
        self.logger = logger
        self.actions = []
        self.collections = {'mail': {'default': {}}, 'chat': {'default': {}},
                            'http': {'default': []}, 'printer': {'default': {}}}

        self.browser = None

        if self.logger is None:
            self.logger = create_logger('generator', logging.DEBUG)

        # Parse YAML config.
        try:
            with open(path, 'r') as f:
                self.config = yaml.safe_load(f)
        except (IOError, yaml.YAMLError) as error:
            self.logger.error('[-] Could not find or parse config file %s: %s', path, error)
            sys.exit(1)

        # Check if minimum requirements are fulfilled.
        if 'hay' not in self.config or 'needles' not in self.config:
            self.logger.error('[-] Config file does not contain both hay and needle sections.')
            sys.exit(1)

        self.logger.info('[~] Loading collections.')

        # Load parameters for different applications.
        self._load_collections()

        self.logger.info('[~] Generating randomized action suite.')

        # Collect actions used for the hay and needle(s).
        for key, entry in self.config['hay'].items() + self.config['needles'].items():
            # Generate action with specified parameters and generated missing parameters if needed.
            self.actions.extend(self._generate_action_content(entry))
            self.logger.info('\t Created %s set.', key)

        # Randomize action suite.
        random.shuffle(self.actions, random.random)

        # Generate action suite from config.
        self.logger.info('[~] Generated randomized action suite.')

    def shutdown(self):
        """

        :return:
        """
        self._shutdown_browser()

    def execute(self):
        """

        :return:
        """
        # Execute actions.
        for entry in self.actions:
            self.logger.debug('[~] Executing %s.', entry)
            self._execute_action(entry)

    def _execute_action(self, entry):
        """

        :param entry:
        :return:
        """
        if entry['type'] == 'http':
            self._execute_http_action(entry)
        elif entry['type'] == 'mail':
            self._execute_mail_action(entry)
        elif entry['type'] == 'chat':
            pass
        elif entry['type'] == 'printer':
            pass

    def _execute_http_action(self, entry):
        """
        Executes a http (browser) action.
        :param entry:
        :return:
        """
        browser = self._get_browser()

        # Open URL.
        browser.open(url=entry['url'])

        while browser.is_busy is True:
            self.logger.debug("[~] Firefox is busy.")
            time.sleep(1)

        time.sleep(5)

    def _execute_mail_action(self, entry):
        """
        Executes a mail action.
        :param entry:
        :return:
        """
        # Create new mail application.
        mailer = self.guest.application("mailClientThunderbird", {})

        # Set mail configuration for application from config file.
        mail_data = self.config['applications'][entry['application']]

        mail_account = MailAccount(mail_data['imap_hostname'],
                                   mail_data['smtp_hostname'],
                                   mail_data['email'],
                                   mail_data['password'],
                                   mail_data['username'],
                                   mail_data['full_name'],
                                   mail_data['socket_type'],
                                   mail_data['socket_type_smtp'],
                                   mail_data['auth_method_smtp'])

        mail = Mail(entry['recipient'], entry['subject'], entry['message'], entry['attachment_path_list'])

        send_mail(mailer, mail_account, mail)

    def _execute_chat_action(self, entry):
        pass

    def _execute_printer_action(self, entry):
        pass

    def _generate_action_content(self, entry):
        if entry['application'] == 'http':
            action_type = 'http'
        else:
            # Check if application configuration exists for the action.
            if entry['application'] not in self.config['applications']:
                logging.error('[-] No application configuration found for %s.', entry['application'])
                sys.exit(1)

            action_type = self.config['applications'][entry['application']]['type']

        if action_type == 'http':
            return self._generate_action_http(entry)
        if action_type == 'mail':
            return self._generate_action_mail(entry)
        elif action_type == 'chat':
            return self._generate_action_chat(entry)
        elif action_type == 'printer':
            return self._generate_action_printer(entry)

    def _generate_action_http(self, entry):
        """

        :param entry:
        :return:
        """
        actions = []

        if 'collection' in entry:
            if entry['collection'] in self.collections['http']:
                collection = self.collections['http'][entry['collection']]
            else:
                collection = self.collections['http']['default']
        else:
            collection = self.collections['http']['default']

        for _ in range(0, entry['amount']):
            if 'url' in entry:
                url = entry['url']
            else:
                if len(collection) > 0:
                    url = random.choice(collection)
                else:
                    url = random.choice(self.collections['http']['default'])

            actions.append(
                {'type': 'http', 'url': url})

        return actions

    def _generate_action_mail(self, entry):
        """

        :param entry:
        :return:
        """
        actions = []

        if 'collection' in entry:
            if entry['collection'] in self.collections['mail']:
                collection = self.collections['mail'][entry['collection']]
            else:
                collection = self.collections['mail']['default']
        else:
            collection = self.collections['mail']['default']

        for _ in range(0, entry['amount']):
            if 'subject' in entry:
                subject = entry['subject']
            else:
                if len(collection['subjects']) > 0:
                    subject = random.choice(collection['subjects'])
                else:
                    subject = random.choice(self.collections['mail']['default']['recipients'])

            if 'recipient' in entry:
                recipient = entry['recipient']
            else:
                if len(collection['recipients']) > 0:
                    recipient = random.choice(collection['recipients'])
                else:
                    recipient = random.choice(self.collections['mail']['default']['recipients'])

            if 'message' in entry:
                message = entry['message']
            else:
                if len(collection['messages']) > 0:
                    message = random.choice(collection['messages'])
                else:
                    message = random.choice(self.collections['mail']['default']['messages'])

            if 'attachment_path_list' in entry:
                attachment_path_list = entry['attachment_path_list']
            else:
                if len(collection['attachment_path_list']) > 0:
                    attachment_path_list = random.choice(collection['attachment_path_list'])
                else:
                    attachment_path_list = random.choice(self.collections['mail']['default']['attachment_path_list'])

            actions.append(
                {'type': 'mail', 'recipient': recipient,
                 'subject': subject,
                 'message': message,
                 'attachment_path_list': attachment_path_list})

        return actions

    def _generate_action_chat(self, entry):
        """

        :param entry:
        :return:
        """
        actions = []

        if 'collection' in entry:
            if entry['collection'] in self.collections['chat']:
                collection = self.collections['chat'][entry['collection']]
            else:
                collection = self.collections['chat']['default']
        else:
            collection = self.collections['chat']['default']

        for _ in range(0, entry['amount']):
            if 'recipient' in entry:
                recipient = entry['recipient']
            else:
                if len(collection['recipients']) > 0:
                    recipient = random.choice(collection['recipients'])
                else:
                    recipient = random.choice(self.collections['chat']['default']['recipients'])

            if 'message' in entry:
                message = entry['message']
            else:
                if len(collection['messages']) > 0:
                    message = random.choice(collection['messages'])
                else:
                    message = random.choice(self.collections['chat']['default']['messages'])

            if 'attachments' in entry:
                attachments = entry['attachments']
            else:
                if len(collection['attachments']) > 0:
                    attachments = random.choice(collection['attachments'])
                else:
                    attachments = random.choice(self.collections['chat']['default']['attachments'])

            actions.append(
                {'type': 'chat', 'recipient': recipient, 'message': message, 'attachments': attachments})

        return actions

    def _generate_action_printer(self, entry):
        """

        :param entry:
        :return:
        """
        actions = []

        if 'collection' in entry:
            if entry['collection'] in self.collections['printer']:
                collection = self.collections['printer'][entry['collection']]
            else:
                collection = self.collections['printer']['default']
        else:
            collection = self.collections['printer']['default']

        for _ in range(0, entry['amount']):
            if 'file' in entry:
                document = entry['file']
            else:
                if len(collection) > 0:
                    document = random.choice(collection)
                else:
                    document = random.choice(self.collections['printer']['default'])

            actions.append({'type': 'printer', 'file': document})

        return actions

    def _load_collections(self):
        """

        :return:
        """
        # Load custom collections if specified.
        for key, collection in self.config['collections'].items():
            if collection['type'] == 'http':
                if 'urls' in collection:
                    with open(collection['urls'], 'r') as f:
                        self.collections['http'][key] = f.read().splitlines()
                else:
                    self.collections['http'][key] = []

            elif collection['type'] == 'mail':
                self.collections['mail'][key] = {}

                if 'recipients' in collection:
                    with open(collection['recipients'], 'r') as f:
                        self.collections['mail'][key]['recipients'] = f.read().splitlines()
                else:
                    self.collections['mail'][key]['recipients'] = []

                if 'subjects' in collection:
                    with open(collection['subjects'], 'r') as f:
                        self.collections['mail'][key]['subjects'] = f.read().splitlines()
                else:
                    self.collections['mail'][key]['subjects'] = []

                if 'messages' in collection:
                    with open(collection['messages'], 'r') as f:
                        self.collections['mail'][key]['messages'] = f.read().splitlines()
                else:
                    self.collections['mail'][key]['messages'] = []

                if 'attachment_path_list' in collection:
                    with open(collection['attachment_path_list'], 'r') as f:
                        self.collections['mail'][key]['attachment_path_list'] = f.read().splitlines()
                else:
                    self.collections['mail'][key]['attachment_path_list'] = []

            elif collection['type'] == 'chat':
                self.collections['chat'][key] = {}

                if 'recipients' in collection:
                    with open(collection['recipients'], 'r') as f:
                        self.collections['chat'][key]['recipients'] = f.read().splitlines()
                else:
                    self.collections['chat'][key]['recipients'] = []

                if 'messages' in collection:
                    with open(collection['messages'], 'r') as f:
                        self.collections['chat'][key]['messages'] = f.read().splitlines()
                else:
                    self.collections['chat'][key]['messages'] = []

                if 'attachments' in collection:
                    with open(collection['attachments'], 'r') as f:
                        self.collections['chat'][key]['attachments'] = f.read().splitlines()
                else:
                    self.collections['chat'][key]['attachments'] = []

            elif collection['type'] == 'printer':
                self.collections['printer'][key] = {}

                if 'documents' in collection:
                    with open(collection['documents'], 'r') as f:
                        self.collections['printer'][key] = f.read().splitlines()
                else:
                    self.collections['printer'][key] = []

        # Load default fallback collections for http.
        with open('./generator/http_default_urls.txt', 'r') as f:
            self.collections['http']['default'] = f.read().splitlines()

        # Load default fallback collections for mails.
        with open('./generator/mail_default_recipients.txt', 'r') as f:
            self.collections['mail']['default']['recipients'] = f.read().splitlines()

        with open('./generator/mail_default_subjects.txt', 'r') as f:
            self.collections['mail']['default']['subjects'] = f.read().splitlines()

        with open('./generator/mail_default_messages.txt', 'r') as f:
            self.collections['mail']['default']['messages'] = f.read().splitlines()

        with open('./generator/general_default_attachments.txt', 'r') as f:
            self.collections['mail']['default']['attachment_path_list'] = f.read().splitlines()

        # Load default fallback collections for chat.
        with open('./generator/chat_default_recipients.txt', 'r') as f:
            self.collections['chat']['default']['recipients'] = f.read().splitlines()

        with open('./generator/chat_default_messages.txt', 'r') as f:
            self.collections['chat']['default']['messages'] = f.read().splitlines()

        with open('./generator/general_default_attachments.txt', 'r') as f:
            self.collections['chat']['default']['attachments'] = f.read().splitlines()

        # Load default fallback collections for printer.
        with open('./generator/printer_default_documents.txt', 'r') as f:
            self.collections['printer']['default']['documents'] = f.read().splitlines()

    def _get_browser(self):
        """

        :return:
        """
        if not self.browser:
            # Create a new Firefox application.
            self.browser = self.guest.application("webBrowserFirefox", {'webBrowser': "firefox"})

            # Wait for Firefox to start.
            while self.browser.is_busy is True:
                self.logger.debug("[~] Firefox is starting. Waiting.")
                time.sleep(1)

        # Return the browser.
        return self.browser

    def _shutdown_browser(self):
        """

        :return:
        """
        if self.browser:
            self.browser.close()