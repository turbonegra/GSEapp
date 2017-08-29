from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Decision(Page):
    form_model = models.Player
    form_fields = ['choice']

    timeout_seconds = 20

    def vars_for_template(self):
        range_data = list(range(0,Constants.xf_A+1))
        yA_values = list(map(lambda x: Constants.y0_A + x*Constants.m_A, range_data))
        yB_values = list(map(lambda x: Constants.y0_B + x*Constants.m_B, range_data))

        data = [[] for i in range(Constants.xf_A+1)]
        for i in range(0, Constants.xf_A+1):
            data[i].append(i )
            data[i].append(yA_values[i])
            data[i].append(yB_values[i])

        #data = [range_data,yA_values,yB_values]
        return {
            'range_data': range_data,
            'yA_values': yA_values,
            'yB_values':yB_values,
            'data': data,
        }



    def before_next_page(self):
        if self.timeout_happened:
            self.player.automatic_decision = True


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        alive_players = [p for p in self.subsession.get_players() if p.automatic_decision==False]
        random.shuffle(alive_players)

        num_alive = sum(1 for p in self.subsession.get_players()if p.automatic_decision==False)
        print('*******num_alive is', num_alive)

        full_groups = num_alive // Constants.group_size
        print('*******full_groups is', full_groups)


        for i in range(1,full_groups+1):
            print('*******He entrado, vez', i)

            players = alive_players[0+Constants.group_size*(i-1):Constants.group_size +Constants.group_size*(i-1)]
            print('******* longitud players', len(players))
            SizeA= sum(1 if p.choice=="A" else 0 for p in players)
            SizeB= sum(1 if p.choice=="B" else 0 for p in players)

            if SizeA < Constants.xf_A:
                payoff_A = Constants.y0_A + SizeA*Constants.m_A

            else:
                payoff_A = Constants.yf_A

            if SizeB < Constants.xf_B:
                payoff_B = Constants.y0_B + SizeB*Constants.m_B

            else:
                payoff_B = Constants.yf_B

            print('*******payoff_A is', payoff_A)
            print('*******payoff_B is', payoff_B)

            for p in players:
                print('*******He entrado, player', p)
                p.my_group = i-1
                if p.choice=="A":
                    p.payoff=payoff_A
                    p.size_group = SizeA
                else:
                    p.payoff=payoff_B
                    p.size_group = SizeB

        #payoff of people without full group
        players_no_group = alive_players[Constants.group_size*(full_groups):num_alive]
        players_A = [p for p in alive_players if (p.choice=="A" and p.my_group>0)] #p.my_group>0 ensures the player belong to a full group
        players_B = [p for p in alive_players if (p.choice == "B" and p.my_group>0) ]
        print('******* Antes de entrar', players_no_group)

        for p in players_no_group:
            print('******* estoy entrando',players_no_group)
            p.my_group = full_groups
            if p.choice == "A":
                print('******* copiables', players_A)
                copy_to = random.choice(players_A)
                print('******* copy_to', copy_to)
                print('******* Con payoff', copy_to.payoff)
                p.payoff = copy_to.payoff
                print('******* nuevo payoff', p.payoff)
                p.size_group = copy_to.size_group

            else:
                print('******* copiables', players_B)
                copy_to = random.choice(players_B)
                print('******* copy_to', copy_to)
                print('******* Con payoff', copy_to.payoff)
                p.payoff = copy_to.payoff
                p.size_group = copy_to.size_group
                print('******* nuevo payoff', p.payoff )


        self.group.compute_payments()
        print('******* real_world_currency_per_point is', self.session.config['real_world_currency_per_point'])
        print('******* budget_per_person is',self.session.config['budget_per_person'])


class Results(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        rate= 1 / self.session.config['real_world_currency_per_point']

        return {
            'rate': rate,
        }



page_sequence = [
    Decision,
    ResultsWaitPage,
    Results
]
