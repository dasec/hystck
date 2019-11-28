import logging
import random
import time
import yaml

from hystck.utility.logger_helper import create_logger


class Generator(object):
    def __init__(self, guest, path, logger=None):
        self.guest = guest
        self.logger = logger
        self.actions = []

        if self.logger is None:
            self.logger = create_logger('generator', logging.DEBUG)

        # Parse YAML config.
        try:
            with open(path, 'r') as f:
                self.config = yaml.safe_load(f)
        except (IOError, yaml.YAMLError) as error:
            self.logger.error('[-] Could not find or parse config file %s.', path)
            raise error

        # Check if minimum requirements are fulfilled.
        if 'hay' not in self.config or 'needles' not in self.config:
            self.logger.error('[-] Config file does not contain both hay and needle sections.')
            raise RuntimeError

        self.logger.info('[~] Generating randomized action suite.')

        # Collect actions used for the hay and needle(s).
        for key, entry in self.config['hay'].items() + self.config['needles'].items():
            # Decide whether the contents of the action are already specified or if we need to generate them with our
            # data sets.
            if 'randomize' in entry:
                self.actions.extend(self._generate_action_content(entry))
            else:
                self.actions.append(entry)
            self.logger.info('\t Created %s set.', key)

        # Randomize action suite.
        random.shuffle(self.actions, random.random)

        # Generate action suite from config.
        self.logger.info('[~] Generated randomized action suite.')

    def execute(self):
        # Execute actions.
        for entry in self.actions:
            self.logger.debug('[~] Executing %s.', entry)
            self._execute_action(entry)

    def _execute_action(self, entry):
        if entry['service'] == 'http':
            pass
        elif entry['service'] == 'mail':
            self._execute_mail_action(entry)
        elif entry['service'] == 'chat':
            pass
        elif entry['service'] == 'printer':
            pass

    def _execute_http_action(self, entry):
        pass

    def _execute_mail_action(self, entry):
        mailer = self.guest.application("mail_client", {})

        mailer.set_config("guest", self.config['services']['mail']['email'],
                          self.config['services']['mail']['password'], self.config['services']['mail']['email'],
                          self.config['services']['mail']['imap_hostname'],
                          self.config['services']['mail']['smtp_hostname'])

        mailer.open()

        while mailer.is_busy is True:
            self.logger.debug("[~] Thunderbird is busy!")
            time.sleep(1)

        mailer.send_mail(entry['recipient'], entry['subject'], entry['content'])

        while mailer.is_busy is True:
            self.logger.debug("[~] Thunderbird is busy.")
            time.sleep(1)

        mailer.close()
        time.sleep(5)

    def _execute_chat_action(self, entry):
        pass

    def _execute_printer_action(self, entry):
        pass

    def _generate_action_content(self, entry):
        if entry['service'] == 'http':
            return []
        elif entry['service'] == 'mail':
            return self._generate_action_mail(entry)
        elif entry['service'] == 'chat':
            return []
        elif entry['service'] == 'printer':
            return []

    @staticmethod
    def _generate_action_mail(entry):
        actions = []

        # TODO: Load recipients, subject, content and attachments from files.
        recipients = ['1@gmx.de', '2@gmx.de', '3@gmx.de']
        subjects = ['Hello World', 'What a wonderful day', 'Hello there']
        contents = ['I\'ve attached a document', 'What\'s up?', 'Hello my friend']
        attachments = ['document.pdf', 'image.jpeg', 'song.mp3']

        for _ in range(0, entry['amount']):
            actions.append({'recipient': random.choice(recipients), 'subject': random.choice(subjects),
                            'content': random.choice(contents), 'attachment': random.choice(attachments)})

        return actions
