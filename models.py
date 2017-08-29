from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'M. Pereda'

doc = """
Group Size Effects. IBSEN.
"""


class Constants(BaseConstants):
    name_in_url = 'GSEapp'
    players_per_group = None
    num_rounds = 1
    show_up_fee = 5

    #My constants
    group_size = 2 #Virtual group size for payoff calculation

    # Beta functions
    y0_A = 0 #intercept for group A
    m_A = 5 #slope for group A
    xf_A = 10 # X value for the second part of the beta function
    yf_A = 50 # Y value in the constant part of the beta function

    y0_B = 10  # intercept for group B
    m_B = 5  # slope for group B
    xf_B = 10 # X value for the second part of the beta function
    yf_B = 60 # Y value in the constant part of the beta function


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_payoff=models.CurrencyField(default=0)

    def compute_payments(self):
        num_played = sum([1 for p in self.get_players() if p.automatic_decision==False])
        print('******* num_played', num_played)

        total_payoff = sum([p.payoff for p in self.get_players() if p.automatic_decision==False]) or 0.0000000001  # para no tener una división por cero

        self.total_payoff = total_payoff
        self.session.config['real_world_currency_per_point'] = self.session.config['budget_per_person'] * num_played / total_payoff
        print('******* cantidad', self.session.config['budget_per_person'] * num_played / self.total_payoff)
        print('******* real_world_currency_per_point is', self.session.config['real_world_currency_per_point'])

        for p in self.get_players():
            if p.automatic_decision==False:
                p.payment=p.participant.payoff.to_real_world_currency(self.session) #To write it on data base





class Player(BasePlayer):
    automatic_decision = models.IntegerField(default = False)
    choice = models.CharField(initial=None, widget=widgets.RadioSelectHorizontal(),
                                        verbose_name='Your choice',
                                        choices= ("A","B"))
    my_group = models.IntegerField(default = 0)
    size_group = models.IntegerField(default = 0)
    payment = models.FloatField(default=0)


