import os
import readline
import sys

from eduxator import io


class CLI:
    prompt = '> '

    def __init__(self):
        self.readline_setup()
        self.cookie_setup()
        self.context_setup()
        self.exit()

    def readline_setup(self):
        self.histfile = os.path.join(os.path.expanduser('~'), '.eduxator_history')
        try:
            readline.read_history_file(self.histfile)
        except FileNotFoundError:
            pass
        readline.parse_and_bind('tab: complete')

    def cookie_setup(self):
        try:
            self.eduxio = io.EduxIO()
        except ValueError as ve:
            self.warn(ve)
            self.info('Please provide the name and value of your cookie from Edux. '
                      'The one where name looks like it\'s random generated is the one.')
            cookie_name = self.ask('Enter the cookie\'s name')
            cookie_value = self.ask('Enter the cookie\'s value')
            self.eduxio = io.EduxIO(cookie_dict={cookie_name: cookie_value})

            if self.ask_bool('Good, I feel your anger. Should I save this to ~./.edux.cookie '
                             'to save you some pain later?'):
                self.info('Saving.')
                self.eduxio.save_cookie()

    def context_setup(self):
        args = list(set(sys.argv[1:]))
        self.eduxio.course = self.determine_course(args)
        self.eduxio.classpath = self.determine_classpath(args)
        self.column = self.determine_column(args)

    def find_candidates(self, args, possibilities, case_sentitive=False):
        if len(possibilities) == 1:
            return possibilities

        candidates = []

        lowers = possibilities if case_sentitive else [x.lower() for x in possibilities]
        for i, arg in enumerate(args):
            larg = arg if case_sentitive else arg.lower()
            if larg in lowers:
                if case_sentitive:
                    # shortcut, just add the arg as it is
                    candidates.append(arg)
                else:
                    # save the item as it is in the possibilities
                    candidates.append(possibilities[lowers.index(larg)])

        if len(candidates) == 1:
            # we only remove the thing form args if we are sure we are going to use it
            args.remove(candidates[0])

        return candidates

    def determine_course(self, args):
        courses = self.eduxio.parse_courses_list()
        candidates = self.find_candidates(args, courses)
        if not candidates:
            return self.ask('What course do you want?', courses)
        if len(candidates) > 1:
            self.warn('Found multiple possible courses.')
            return self.ask('What course do you want?', candidates)
        return candidates[0]

    def determine_column(self, args):
        data = self.eduxio.parse_form_edit_score()
        columns = self.eduxio.all_columns(data)
        candidates = self.find_candidates(args, columns)
        if not candidates:
            return self.ask('What column do you want?', columns)
        if len(candidates) > 1:
            self.warn('Found multiple possible columns.')
            return self.ask('What column do you want?', candidates)
        return candidates[0]

    def determine_classpath(self, args):
        tree = self.eduxio.parse_classification_tree()
        if not tree:
            raise ValueError('The classification tree is empty!')
        classpath = []
        while tree:
            candidates = self.find_candidates(args, list(tree.keys()))
            if not candidates:
                one = self.ask('What class do you want?', tree.keys())
            elif len(candidates) > 1:
                self.warn('Found multiple possible classes.')
                one = self.ask('What class do you want?', candidates)
            else:
                one = candidates[0]
            classpath.append(one)
            tree = tree[one]
        return classpath

    def exit(self, say=False):
        readline.write_history_file(self.histfile)
        if say:
            print('exit')
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
                return ' (' + '/'.join(sorted(possibilities)) + '):'
            return ' (use tab to help yourself):'
        return ''

    def input(self):
        try:
            return input(self.prompt).rstrip()
        except KeyboardInterrupt:
            print('^C')
            return ''

    def ask(self, question, possibilities=None):
        plist = self.possibilities_list(possibilities)
        self.say(question + plist)
        if possibilities:
            def completer(text, state):
                return [x for x in possibilities if x.upper().startswith(text.upper())][state] + ' '
        else:
            completer = None
        readline.set_completer(completer)
        try:
            ret = self.input()
            while (possibilities and ret not in possibilities) or not ret:
                if ret:
                    self.error('Invalid option!' + plist)
                ret = self.input()
        except EOFError:
            self.exit(say=True)
        return ret

    def ask_bool(self, question):
        plist = self.possibilities_list(['Y', 'n'])
        self.say(question + plist)
        readline.set_completer(None)
        try:
            ret = self.input()
            while ret and ret.lower() not in ['y', 'n']:
                if ret:
                    self.error('Invalid option!' + plist)
                ret = self.input()
        except EOFError:
            self.exit(say=True)
        return ret.lower() != 'n'
