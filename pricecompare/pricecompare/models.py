from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2)
    active = models.BooleanField(default=True)
    max_credit = models.IntegerField(default=0)
    max_debit = models.IntegerField(default=0)

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

    def __unicode__(self):
        return "%s" % (self.name)

class IndustryGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class ClassCode(models.Model):
    code = models.IntegerField()
    #name = models.CharField(max_length=100)
    #industry_group = models.ForeignKey(IndustryGroup)

    def __unicode__(self):
        return "(%s)" % (self.code)


class LossCost(models.Model):
    state = models.ForeignKey(State)
    class_code = models.ForeignKey(ClassCode, unique=True)
    loss_cost = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __unicode__(self):
        return "%s (%s) %s" % (self.class_code, self.state, self.loss_cost)

class CarrierState(models.Model):
    carrier = models.ForeignKey(Carrier)
    state = models.ForeignKey(State)
    lcm = models.DecimalField(decimal_places=2, max_digits=10)
    premium = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.carrier, self.state)
