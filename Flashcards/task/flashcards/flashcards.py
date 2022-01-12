import pickle
from random import choice
import io
from argparse import ArgumentParser


class FlashCard:
    def __init__(self, term, definition, error_count=0):
        self.term = term
        self.definition = definition
        self.error_count = error_count


    def display(self):
        # print('Card:')
        print(self.term)
        # print('Definition:')
        print(self.definition)

    def reset_stats(self):
        self.error_count = 0

    def __getstate__(self):
        attributes = self.__dict__.copy()
        print(attributes.keys())
        # del attributes['display']

    # def read_input(self):
    #     return input()

    def check_answer(self):
        answer = input(f'Print the definition of "{self.term}":\n')
        if answer == self.definition:
            print('Correct!')
        else:
            print(f'Wrong. The right answer is "{self.definition}".')


class CardStack:
    def __init__(self, import_from='', export_to=''):
        # self.max_cards = int(input("Input the number of cards:\n"))
        self.n_card = 1
        self.stack = []
        self.output = io.StringIO()
        self.import_from = import_from
        self.export_to = export_to
        if import_from:
            self.import_cards_from_file()

    def menu(self):
        while True:
            outstring = "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
            print(outstring)
            self.output.write(outstring + '\n')
            action = input()
            if action == 'add':
                self.add_card()
            elif action == 'remove':
                self.remove_card()
            elif action == 'import':
                self.import_cards_from_file()
            elif action == 'export':
                self.export_cards_to_file()
            elif action == 'ask':
                self.test_random()
            elif action == 'exit':
                self.exit()
            elif action == 'log':
                self.log()
            elif action == 'hardest card':
                self.find_hardest_card()
            elif action == 'reset stats':
                self.reset_stats()

    def reset_stats(self):
        for card in self.stack:
            card.reset_stats()
            outstream = 'Card statistics have been reset.'
            print(outstream)
            self.output.write(outstream + '\n')

    def find_hardest_card(self):
        highest_score = 1
        highest_terms = []
        for card in self.stack:
            if card.error_count > highest_score:
                highest_terms.clear()
                highest_terms.append(f'"{card.term}"')
                highest_score = card.error_count
            elif card.error_count == highest_score and f'"{card.term}"' not in highest_terms:
                highest_terms.append(f'"{card.term}"')
        if len(highest_terms) == 1:
            outstream = f'The hardest card is {highest_terms[0]}. You have {highest_score} errors answering it'
            print(outstream)
            self.output.write(outstream + '\n')
        elif len(highest_terms) > 1:
            terms = ', '.join(highest_terms)
            outstream = f'The hardest cards are {terms}. You have {highest_score} errors answering them.'
            print(outstream)
            self.output.write(outstream + '\n')
        else:
            outstream = 'There are no cards with errors.'
            print(outstream)
            self.output.write(outstream + '\n')

    def exit(self):
        if self.export_to:
            self.export_cards_to_file()
        outstream = 'Bye bye'
        print(outstream)
        self.output.write(outstream + '\n')
        exit()

    def log(self):
        outstream = 'File name:'
        print(outstream)
        filename = input()
        self.output.write(filename + '\n')
        with open(filename, 'w') as f:
            f.write(self.output.getvalue())
        outstream = 'The log has been saved.'
        print(outstream)
        self.output.write(outstream + '\n')

    def add_card(self):
        # print(f'The term for card #{self.n_card}:')
        outstream = 'The card'
        print(outstream)
        self.output.write(outstream)
        while True:
            term = input()
            if self.term_exist(term):
                outstream = f'The term "{term}" already exists. Try again:'
                print(outstream)
                self.output.write(outstream + '\n')
                continue
            else:
                break
        # print(f"The definition for card #{self.n_card}:")
        outstream = 'The definition of the card'
        print(outstream)
        self.output.write(outstream + '\n')
        while True:
            definition = input()
            if self.def_exist(definition):
                outstream = f'The definition "{definition}" already exists. Try again:'
                print(outstream)
                self.output.write(outstream + '\n')
                continue
            else:
                break
        self.stack.append(FlashCard(term, definition))
        outstream = f'"The pair ("{term}":"{definition}") has been added."'
        print(outstream)
        self.output.write(outstream + '\n')
        self.n_card += 1

    def remove_card(self):
        outstream = 'Which card?'
        print(outstream)
        self.output.write(outstream + '\n')
        term = input()
        self.output.write(term + '\n')
        card = self.find_by_term(term)
        if card:
            del self.stack[self.stack.index(card)]
            outstream = "The card has been removed."
            print(outstream)
            self.output.write(outstream + '\n')
        else:
            outstream = "Can't remove " + f'"{term}": there is no such card.'
            print(outstream)
            self.output.write(outstream + '\n')

    def export_cards_to_file(self):
        if not self.export_to:
            outstream = "File name:"
            print(outstream)
            self.output.write(outstream + '\n')
            self.export_to = input()
            self.output.write(self.export_to + '\n')
        with open(self.export_to, 'wb') as f:
            pickle.dump([el.__dict__ for el in self.stack], f)
            outstream = f'{len(self.stack)} cards have been saved.'
            print(outstream)
            self.output.write(outstream + '\n')

    def import_cards_from_file(self):
        if not self.import_from:
            outstream = "File name:"
            print(outstream)
            self.output.write(outstream + '\n')
            self.import_from = input()
            self.output.write(self.import_from + '\n')
        try:
            with open(self.import_from, 'rb') as f:
                loaded_cards = pickle.load(f)
                self.stack = self.stack + \
                             [FlashCard(card['term'], card['definition'], card['error_count']) for card in loaded_cards]
                outstream = f'{len(loaded_cards)} cards have been loaded.'
                print(outstream)
                self.output.write(outstream + '\n')

        except FileNotFoundError:
            self.import_from = ''
            outstream = "File not found."
            print(outstream)
            self.output.write(outstream + '\n')

    def term_exist(self, term):
        for card in self.stack:
            if card.term == term:
                return True
        return False

    def def_exist(self, definition):
        for card in self.stack:
            # if definition == 'ankle':
            #     print(self.stack)
            #     print(f'{card.definition}:{definition}')
            if card.definition == definition:
                return True
        return False

    def find_by_definition(self, definition):
        for card in self.stack:
            if card.definition == definition:
                return card

    def find_by_term(self, term):
        for card in self.stack:
            if card.term == term:
                return card

    def test_random(self):
        outstream = "How many times to ask?"
        print(outstream)
        self.output.write(outstream)
        instream = input()
        self.output.write(instream + '\n')
        n = int(instream)
        for _ in range(n):
            card = choice(self.stack)
            outstream = f'Print the definition of "{card.term}":\n'
            answer = input(outstream)
            self.output.write(outstream + answer + '\n')
            # if answer == 'ankle':
            #     print("Got it!")
            if answer == card.definition:
                outstream = 'Correct!'
                print(outstream)
                self.output.write(outstream + '\n')
            elif self.def_exist(definition=answer):
                correct_card = self.find_by_definition(definition=answer)
                card.error_count += 1
                outstream = f'Wrong. The right answer is "{card.definition}", ' + \
                            f'but your definition is correct for "{correct_card.term}".'
                print(outstream)
                self.output.write(outstream + '\n')
            else:
                card.error_count += 1
                outstream = f'Wrong. The right answer is "{card.definition}".'
                print(outstream)
                self.output.write(outstream + '\n')

    def test(self):
        for card in self.stack:
            outstream = f'Print the definition of "{card.term}":\n'
            answer = input(outstream)
            self.output.write(outstream)
            # if answer == 'ankle':
            #     print("Got it!")
            if answer == card.definition:
                outstream = 'Correct!'
                print(outstream)
                self.output.write(outstream + '\n')
            elif self.def_exist(definition=answer):
                correct_card = self.find_by_definition(definition=answer)
                outstream = f'Wrong. The right answer is "{card.definition}", ' \
                            + f'but your definition is correct for "{correct_card.term}".'
                print(outstream)
                self.output.write(outstream + '\n')
            else:
                outstream = f'Wrong. The right answer is "{card.definition}".'
                print(outstream)
                self.output.write(outstream + '\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--import_from', help='name of the file with flashcards to import')
    parser.add_argument('--export_to', help='name of the file for saving the flashcards')
    args = parser.parse_args()
    import_file_name = args.import_from
    export_file_name = args.export_to
    print('*', export_file_name, import_file_name)
    cards = CardStack(import_file_name, export_file_name)
    cards.menu()


