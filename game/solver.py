#!/usr/bin/env python

'''
This is a script that runs a solver for your cards.
To run it just run in cmd `solver.py`.
Feel free to change it however you like.
Add your code in the marked sections.
Without your code it doesn't really do anything.
(You can run it before adding your code just to see what happens...)

We used npyscreen to write the interactive cli.
To read about npyscreen see documentation here:
https://npyscreen.readthedocs.io/index.html#

Final notes:
We assume your cards have name, creator and riddle attributes
(card.name, card.creator and card.riddle should work).
If they don't, you might have to change this script a little.
Also:
Currently this script doesn't receive any arguments,
but you might have to add some (like the directory of your cards or something).
But you already know how to do that, so...
Good Luck!
'''
from typing import Optional
from pathlib import Path
import npyscreen
import argparse
import os


from game.card import Card
from data_management.saver import Saver

CARD_STR = 'Card {card.name} by {card.creator}'


class ChooseCardsForm(npyscreen.ActionForm):

    def __init__(self, unsolved_dir: str, *args, **kwargs):
        self.unsolved_dir = Path(unsolved_dir)
        super().__init__(*args, **kwargs)

    def get_cards(self) -> list[Card]:
        '''
        returns list of unsolved cards.
        replace this method with your own code
        (read files from memory etc.)
        '''
        """
        Unclear requirements, the option to choose the unsolved cards directory is a demand in the server, but there 
        isn't a simple way to do that in npyscreen? My solution is a bit gross, didn't want to do a deep dive to find 
        a normal way to do it. :/
        """
        card_files = os.listdir(self.unsolved_dir)
        cards = []
        for card_file in card_files:
            card_path = self.unsolved_dir / card_file
            cards.append(Saver.extract_card(card_path))
        return cards

    def create(self):
        self.cards = self.get_cards()
        self.cards_strs = [CARD_STR.format(card=card)
                           for card in self.cards]
        self.add(npyscreen.FixedText,
                 value='Welcome to your cards solver!',
                 editable=False,
                 color='STANDOUT')
        self.add(npyscreen.FixedText,
                 value='Lets solve some riddles!',
                 editable=False,
                 color='STANDOUT')
        self.nextrely += 1
        self.card = self.add(npyscreen.TitleSelectOne,
                             name='Pick a card. any card. '
                                  '[press cancel to exit]',
                             values=self.cards_strs,
                             exit_right=True,
                             labelColor='DEFAULT')

    def on_ok(self):
        if self.card.value:
            self.parentApp.card = self.cards[self.card.value[0]]
            self.parentApp.setNextForm('SolveCard')
        else:
            self.parentApp.setNextForm('MAIN')

    def on_cancel(self):
        self.parentApp.setNextForm(None)


class SolveCardForm(npyscreen.Form):

    def __init__(self, unsolved_dir: str, solved_dir: str, *args, **kwargs):
        self.unsolved_dir = Path(unsolved_dir)
        self.solved_dir = Path(solved_dir)
        super().__init__(*args, **kwargs)


    def check_solution(self, card, solution) -> bool:
        '''
        checks if solution is correct (returns True or False)
        replace this with your own code.
        '''
        return card.decrypt_card(solution)

    def get_unsolved_card_file(self, card: Card) -> Optional[Path]:
        """
        This function receives a card object and returns the path to the unsolved card file.
        """
        # Weird format demand, why not just use the card's name? This makes it way harder...
        unsolved_files = os.listdir(self.unsolved_dir)
        for unsolved_card_file in unsolved_files:
            file_path = self.unsolved_dir / unsolved_card_file
            unsolved_card = Saver.extract_card(file_path)
            if unsolved_card.name == card.name:
                return file_path
        return None

    def handle_correct_solution(self, card: Card, solution):
        '''
        this function handles a correct solution
        replace this with your own code.
        (move card to solved card etc.)
        '''
        Saver.save(card, self.solved_dir / card.name)
        unsolved_file = self.get_unsolved_card_file(card)
        if unsolved_file is None:
            print("Are the files moving around while the program is running? raising Exception.")
            raise FileNotFoundError("Can't delete unsolved card file, it doesn't exist all of a sudden.")
        print(f'Removing {unsolved_file}')
        if unsolved_file != "/":
            print(f"The file f{unsolved_file} has been removed!")
            # I'm running this on bare metal, not in a vm, I trust my programming, but not that much.
            # os.remove(unsolved_file)
        print(f'{CARD_STR.format(card=card)} was solved correctly!')
        print(f'The solution was: {solution}')

    def solve(self, card: Card, solution):
        if self.check_solution(card, solution):
            self.handle_correct_solution(card, solution)
            self.parentApp.setNextForm('RightSolution')
        else:
            self.parentApp.setNextForm('WrongSolution')

    def create(self):
        self.add(npyscreen.TitleText,
                 name=CARD_STR.format(card=self.parentApp.card),
                 editable=False,
                 labelColor='STANDOUT')
        self.nextrely += 1
        self.add(npyscreen.Textfield,
                 value=self.parentApp.card.riddle,
                 editable=False)
        self.nextrely += 1
        # What type is solution???
        self.solution = self.add(npyscreen.TitleText,
                                 name='Enter solution:',
                                 labelColor='DEFAULT')

    def afterEditing(self):
        self.solve(self.parentApp.card, self.solution.value)


class RightSolutionForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText,
                 name='Well Done!',
                 editable=False)
        self.nextrely += 1
        self.add(npyscreen.Textfield,
                 value=f'press ok to solve another card :)',
                 editable=False)

    def afterEditing(self):
        self.parentApp.card = None
        self.parentApp.setNextForm('MAIN')


class WrongSolutionForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText,
                 name='Incorrect :(',
                 editable=False,
                 labelColor='DANGER')
        self.nextrely += 1
        self.add(npyscreen.Textfield,
                 value='press ok to try again '
                       'or cancel to try a different card...',
                 editable=False)

    def on_ok(self):
        self.parentApp.setNextFormPrevious()

    def on_cancel(self):
        self.parentApp.card = None
        self.parentApp.setNextForm('MAIN')


class InteractiveCLI(npyscreen.NPSAppManaged):
    card = None
    unsolved_dir = ""
    solved_dir = ""

    def onStart(self):
        self.addFormClass('MAIN',
                          ChooseCardsForm,
                          name='Cards Solver',
                          unsolved_dir=self.unsolved_dir,
                          )
        self.addFormClass('SolveCard',
                          SolveCardForm,
                          name='Cards Solver',
                          unsolved_dir=self.unsolved_dir,
                          solved_dir=self.solved_dir,)
        self.addFormClass('WrongSolution',
                          WrongSolutionForm,
                          name='Cards Solver')
        self.addFormClass('RightSolution',
                          RightSolutionForm,
                          name='Cards Solver')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("unsolved_dir",
                        type=str,
                        help="The directory in which the unsolved cards are stored")
    parser.add_argument("solved_dir",
                        type=str,
                        help="The directory in which the solved cards are stored")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    unsolved_dir = args.unsolved_dir
    solved_dir = args.solved_dir
    App = InteractiveCLI()
    App.unsolved_dir = unsolved_dir
    App.solved_dir = solved_dir
    App.run()

