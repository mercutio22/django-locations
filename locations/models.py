from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    country = models.CharField(_(u'country'), max_length=255, unique=True, db_index=True)
    code = models.CharField(_(u'code'), max_length=2, unique=True)

    def __unicode__(self):
        return self.country

    class Meta:
        ordering = ['country']

class Region(models.Model):
    region = models.CharField(_(u'region'), max_length=255, unique=True)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.region

    class Meta:
        ordering = ['region']

class State(models.Model):
    state = models.CharField(_(u'state'), max_length=255, unique=True, db_index=True)
    code = models.CharField(_(u'code'), max_length=2, unique=True)
    region = models.ForeignKey(Region)

    def __unicode__(self):
        return self.state

    class Meta:
        ordering = ['state']

class MesoRegion(models.Model):
    mesoregion = models.CharField(_(u'mesoregion'), max_length=255, unique=True)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.mesoregion

    class Meta:
        ordering = ['mesoregion']

class MicroRegion(models.Model):
    microregion = models.CharField(_(u'microregion'), max_length=255)
    mesoregion =  models.ForeignKey(MesoRegion)

    def __unicode__(self):
        return self.microregion

    class Meta:
        ordering = ['microregion']
        unique_together = ('microregion', 'mesoregion')

class Municipality(models.Model):
    municipality = models.CharField(_(u'municipality'), max_length=255, db_index=True)
    microregion = models.ForeignKey(MicroRegion)

    def __unicode__(self):
        return self.municipality

    class Meta:
        ordering = ['municipality']
        unique_together = ('municipality', 'microregion')

class District(models.Model):
    district = models.CharField(_(u'district'), max_length=255)
    municipality = models.ForeignKey(Municipality)

    def __unicode__(self):
        return self.district

    class Meta:
        ordering = ['district']
        unique_together = ('district', 'municipality')

class Point(models.Model):
    latitude = models.FloatField(_('latitude'), blank=True, null=True)
    longitude = models.FloatField(_('longitude'), blank=True, null=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True, null=True)
    street_name = models.CharField(_('street name'), max_length=255)
    street_number = models.CharField(_('street number'), max_length=24)

class Place(models.Model):
    city = models.ForeignKey(Municipality)
    district = models.ForeignKey(District, blank=True, null=True)
    point = models.ForeignKey(Point)

    @property
    def country(self):
        return self.city.microregion.mesoregion.state.country

    @property
    def state(self):
        return self.city.microregion.mesoregion.state

    @property
    def mesoregion(self):
        return self.city.microregion.mesoregion

    @property
    def microregion(self):
        return self.city.microregion

    @property
    def latitude(self):
        return self.point.latitude

    @property
    def longitude(self):
        return self.point.longitude

    @property
    def address(self):
        return u'%s, %s - %s' % (self.point.street_name, self.point.street_number, self.point.city)

    class Meta:
        abstract = True