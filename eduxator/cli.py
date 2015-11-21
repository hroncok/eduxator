import readline
import sys

from eduxator import io


class CLI:
    def __init__(self):
        self.prompt = '> '
        try:
            self.eduxio = io.EduxIO()
        except ValueError as ve:
            self.warn(ve)
            self.info('Please provide the name and value of your cookie from Edux. '
                      'The one where name looks like it\'s random generated is the one.')
            cookie_name = self.ask('Enter the cookie\'s name')
            cookie_value = self.ask('Enter the cookie\'s value')
            self.eduxio = io.EduxIO(cookie_dict={cookie_name: cookie_value})

            save = self.ask_bool('Good, I feel your anger. Should I save this to ~./.edux.cookie '
                                 'to save you some pain later?')
            # TODO save cookie to file, possibly implement in EduxIO
            if save:
                self.info('Saving.')

    def exit(self):
        sys.exit(0)

    def say(self, msg):
        return print(str(msg))  # for now

    def info(self, msg):
        return self.say(msg)  # for now

    def warn(self, msg):
        return self.say(msg)  # for now

    def error(self, msg):
        return self.say(msg)  # for now

    def possibilities_list(self, possibilities):
        if possibilities:
            if len(possibilities) < 8:
                return ' (' + '/'.join(possibilities) + '):'
            return ' (use tab to help yourself):'
        return ''

    def ask(self, question, possibilities=None):
        plist = self.possibilities_list(possibilities)
        self.say(question + plist)
        if possibilities:
            def completer(text, state):
                return [x for x in possibilities if x.upper().startswith(text.upper())][state]
        else:
            completer = None
        readline.set_completer(completer)
        try:
            ret = input(self.prompt)
            while (possibilities and ret not in possibilities) or not ret:
                if ret:
                    self.error('Invalid option!' + plist)
                ret = input(self.prompt)
        except EOFError:
            self.exit()
        return ret

    def ask_bool(self, question):
        plist = self.possibilities_list(['Y', 'n'])
        self.say(question + plist)
        readline.set_completer(None)
        try:
            ret = input(self.prompt)
            while ret and ret.lower() not in ['y', 'n']:
                if ret:
                    self.error('Invalid option!' + plist)
                ret = input(self.prompt)
        except EOFError:
            self.exit()
        return ret.lower() != 'n'
