from decimal import Decimal
from django.db import models
from django import newforms as forms
from django.newforms.widgets import *
from django.core.mail import send_mail, BadHeaderError

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=Textarea())


class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2)
    active = models.BooleanField(default=True)
    max_credit = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    max_debit = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    terrorism_loss = models.DecimalField(decimal_places=2, max_digits=3, default=0)

    def __unicode__(self):
        return self.name


class StateModifier(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    modifier = models.DecimalField(decimal_places=4, max_digits=10)

    def __unicode__(self):
        return "%s %s" % (self.name, self.state)


class Carrier(models.Model):
    name = models.CharField(max_length=100)
    #code = models.IntegerField()
    #group = models.IntegerField()
    expense_constant = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    states = models.ManyToManyField(State, through='CarrierState')

    def __unicode__(self):
        return "%s" % (self.name)

class IndustryGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class ClassCode(models.Model):
    code = models.IntegerField()
    states = models.ManyToManyField(State, through='LossCost')
    #name = models.CharField(max_length=100)
    #industry_group = models.ForeignKey(IndustryGroup)

    def __unicode__(self):
        return "(%s)" % (self.code)


class LossCost(models.Model):
    state = models.ForeignKey(State)
    class_code = models.ForeignKey(ClassCode)
    loss_cost = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    flags = models.ManyToManyField('ClassFlag', blank=True)

    def __unicode__(self):
        return "%s (%s) %s" % (self.class_code, self.state, self.loss_cost)

    class Meta:
        unique_together = ('state', 'class_code')

class CarrierState(models.Model):
    carrier = models.ForeignKey(Carrier)
    state = models.ForeignKey(State)
    lcm = models.DecimalField(decimal_places=3, max_digits=10)
    premium = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)

    def set_inputs(self, loss_cost, payroll, mod):
        self._loss_cost = loss_cost
        self._payroll = Decimal(payroll)
        self._mod = Decimal(mod)

    def rate(self):
        return self.lcm * self._loss_cost.loss_cost

    def calc_premium(self):
        return (self._payroll / 100) * self.rate()

    def total_mod(self):
        return self.calc_premium() * (self._mod - Decimal(1))

    def manual_price(self):
        return self.calc_premium() * self._mod

    def max_price(self):
        return self.manual_price() * (1+self.state.max_debit)

    def min_price(self):
        return self.manual_price() * (1+self.state.max_credit)

    def terrorism_fee(self):
        return (self._payroll / 100) * self.state.terrorism_loss

    def total_premium(self):
        # TODO: This should eventually support multiple mod codes
        pass


    def estimate(self):
        return self.manual_price() + self.terrorism_fee() + self.carrier.expense_constant

    def __unicode__(self):
        return "%s - %s" % (self.carrier, self.state)

class ClassFlag(models.Model):
    description = models.CharField(max_length=255)
    flag_color = models.CharField(max_length=10, choices = (('red', 'Red'), ('green', 'Green'), ('yellow', 'Yellow')))

    def __unicode__(self):
        return self.description
