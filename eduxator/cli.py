import os
import readline
import sys

import colorama

from eduxator import io


class CLI:
    def __init__(self):
        self.prompt = '> '
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

        for item in ['tab: complete',
                     '"\\C-l": clear-screen',
                     'set show-all-if-ambiguous on',
                     '"\\C-o": tab-insert',
                     '"\\C-r": reverse-search-history',
                     '"\\C-s": forward-search-history',
                     '"\\C-p": history-search-backward',
                     '"\\C-n": history-search-forward',
                     '"\\e[A": history-search-backward',
                     '"\\e[B": history-search-forward',
                     '"\\C-k": kill-line',
                     '"\\C-u": unix-line-discard']:
            readline.parse_and_bind(item)

        # Do not treat dash as delimiter in tab completion
        readline.set_completer_delims(readline.get_completer_delims().replace('-', ''))

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
        self.asked = False
        args = list(set(sys.argv[1:]))
        self.eduxio.course = self.determine_course(args)
        self.eduxio.classpath = self.determine_classpath(args)
        self.column = self.determine_column(args)
        self.prompt = '[{}{}{}{}]> '.format(colorama.Fore.BLUE, colorama.Style.BRIGHT,
                                            self.column, colorama.Style.RESET_ALL)
        if self.asked:
            self.info('All set. Hint: Use the following command to start eduxator '
                      'with the same context:')
            self.info('\n    eduxator {} {} {}\n'.format(self.eduxio.course,
                                                         ' '.join(self.eduxio.classpath),
                                                         self.column))

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
        columns = tuple(self.eduxio.all_columns(data))
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
        return print(msg)

    def info(self, msg):
        return self.say(str(msg))

    def question(self, msg):
        return self.say(colorama.Fore.GREEN + colorama.Style.BRIGHT +
                        str(msg) + colorama.Style.RESET_ALL)

    def warn(self, msg):
        return self.say(colorama.Fore.YELLOW + colorama.Style.BRIGHT +
                        str(msg) + colorama.Style.RESET_ALL)

    def error(self, msg):
        return self.say(colorama.Fore.RED + colorama.Style.BRIGHT +
                        str(msg) + colorama.Style.RESET_ALL)

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
        self.asked = True
        plist = self.possibilities_list(possibilities)
        self.question(question + plist)
        if possibilities:
            completer = BufferAwareCompleter(possibilities).complete
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
        self.question(question + plist)
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


class BufferAwareCompleter:
    '''
    Buffer aware completer for tab tompletion

    See: https://pymotw.com/2/readline/
    Copyright Doug Hellmann, All Rights Reserved
    Originally published under BSD license
    '''
    def __init__(self, options):
        if isinstance(options, dict):
            self.options = options
        else:
            self.options = {}
            for option in options:
                self.options[option] = []
        self.current_candidates = []

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            if not words:
                self.current_candidates = sorted(self.options.keys())
            else:
                try:
                    if begin == 0:
                        # first word
                        candidates = self.options.keys()
                    else:
                        # later word
                        first = words[0]
                        candidates = self.options[first]

                    if being_completed:
                        # match options with portion of input
                        # being completed
                        self.current_candidates = [w + ' ' for w in candidates
                                                   if w.upper().startswith(being_completed.upper())]
                    else:
                        # matching empty string so use all candidates
                        self.current_candidates = candidates

                except (KeyError, IndexError):
                    self.current_candidates = []

        try:
            response = self.current_candidates[state]
        except IndexError:
            response = None
        return response
