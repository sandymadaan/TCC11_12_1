# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Amt(models.Model):
    jobno = models.IntegerField(primary_key=True)
    clg = models.IntegerField()
    admn = models.IntegerField()
    consult = models.IntegerField()
    dev = models.IntegerField()
    total = models.IntegerField()
    edu = models.IntegerField()
    hedu = models.IntegerField()
    stax = models.IntegerField()
    nett = models.IntegerField()
    tdu = models.IntegerField()
    bal = models.IntegerField()
    testdone = models.CharField(max_length=150)
    class Meta:
        db_table = u'amt'


class Bill(models.Model):
    prono = models.IntegerField(primary_key=True)
    ser = models.IntegerField()
    hedu = models.IntegerField()
    edu = models.IntegerField()
    total = models.IntegerField()
    class Meta:
        db_table = u'bill'

class Bricks(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    absorption = models.IntegerField(null=True, db_column='Absorption', blank=True) # Field name made lowercase.
    strength = models.IntegerField(null=True, db_column='Strength', blank=True) # Field name made lowercase.
    effloresces = models.IntegerField(null=True, db_column='Effloresces', blank=True) # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'bricks'

class Cement(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    curing = models.IntegerField(null=True, db_column='Curing', blank=True) # Field name made lowercase.
    soundness = models.IntegerField(null=True, db_column='Soundness', blank=True) # Field name made lowercase.
    fineness = models.IntegerField(null=True, db_column='Fineness', blank=True) # Field name made lowercase.
    consistency = models.IntegerField(null=True, db_column='Consistency', blank=True) # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'cement'

class Client(models.Model):
    jono = models.IntegerField(unique=True)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=3000)
    receipt = models.CharField(max_length=180)
    phno = models.CharField(max_length=150)
    type = models.CharField(max_length=45)
    rdate = models.DateField()
    site = models.CharField(max_length=600)
    org = models.CharField(max_length=60)
    class Meta:
        db_table = u'client'

class Coarse(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    sieve = models.IntegerField(null=True, db_column='Sieve', blank=True) # Field name made lowercase.
    abrasion = models.IntegerField(null=True, db_column='Abrasion', blank=True) # Field name made lowercase.
    crushing = models.IntegerField(null=True, db_column='Crushing', blank=True) # Field name made lowercase.
    flakiness = models.IntegerField(null=True, db_column='Flakiness', blank=True) # Field name made lowercase.
    impact = models.IntegerField(null=True, db_column='Impact', blank=True) # Field name made lowercase.
    specifc = models.IntegerField(null=True, db_column='Specifc', blank=True) # Field name made lowercase.
    soaked = models.IntegerField(null=True, db_column='Soaked', blank=True) # Field name made lowercase.
    unsoaked = models.IntegerField(null=True, db_column='Unsoaked', blank=True) # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'coarse'

class Contacts(models.Model):
    name = models.CharField(unique=True, max_length=150)
    address = models.CharField(max_length=600)
    phno = models.CharField(max_length=150)
    class Meta:
        db_table = u'contacts'

class Cubes(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'cubes'



class JobRegister(models.Model):
    job_no = models.IntegerField(primary_key=True)
    date = models.DateField()
    letter_no = models.CharField(max_length=30)
    letter_date = models.DateField()
    address = models.CharField(max_length=3000)
    material_type = models.CharField(max_length=150)
    file_disposal = models.CharField(max_length=60)
    phone = models.IntegerField()
    class Meta:
        db_table = u'job_register'

class Pavers(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    absorption = models.IntegerField(null=True, db_column='Absorption', blank=True) # Field name made lowercase.
    strength = models.IntegerField(null=True, db_column='Strength', blank=True) # Field name made lowercase.
    flex_strength = models.IntegerField(null=True, db_column='Flex_Strength', blank=True) # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'pavers'

class Proformabill(models.Model):
    prono = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=210)
    address = models.CharField(max_length=750)
    chargesfor = models.CharField(max_length=450)
    site = models.CharField(max_length=750)
    sample = models.CharField(max_length=270)
    refno = models.CharField(max_length=300)
    rate = models.IntegerField()
    amount = models.IntegerField()
    pdate = models.DateField()
    transpotation = models.IntegerField()
    class Meta:
        db_table = u'proformabill'

class Soil(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    sieve = models.IntegerField(null=True, db_column='Sieve', blank=True) # Field name made lowercase.
    fineness = models.IntegerField(null=True, db_column='Fineness', blank=True) # Field name made lowercase.
    silt = models.IntegerField(null=True, db_column='Silt', blank=True) # Field name made lowercase.
    moisture = models.IntegerField(null=True, db_column='Moisture', blank=True) # Field name made lowercase.
    liquid = models.IntegerField(null=True, db_column='Liquid', blank=True) # Field name made lowercase.
    compaction = models.IntegerField(null=True, db_column='Compaction', blank=True) # Field name made lowercase.
    specifc = models.IntegerField(null=True, db_column='Specifc', blank=True) # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'soil'

class Steel(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    name = models.CharField(max_length=24)
    five = models.IntegerField(null=True, blank=True)
    eight = models.IntegerField(null=True, blank=True)
    ten = models.IntegerField(null=True, blank=True)
    twelve = models.IntegerField(null=True, blank=True)
    twenty = models.IntegerField(null=True, blank=True)
    twentyfive = models.IntegerField(null=True, blank=True)
    thirty = models.IntegerField(null=True, blank=True)
    thirtyfour = models.IntegerField(null=True, blank=True)
    other = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'steel'

class Steel1(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField()
    date = models.DateField()
    name = models.CharField(max_length=24)
    barbed = models.IntegerField(null=True, db_column='Barbed', blank=True) # Field name made lowercase.
    hing = models.IntegerField(null=True, db_column='Hing', blank=True) # Field name made lowercase.
    structural = models.IntegerField(null=True, db_column='Structural', blank=True) # Field name made lowercase.
    angle = models.IntegerField(null=True, db_column='Angle', blank=True) # Field name made lowercase.
    flats = models.IntegerField(null=True, db_column='Flats', blank=True) # Field name made lowercase.
    tees = models.IntegerField(null=True, db_column='Tees', blank=True) # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'steel1'

class Suspence(models.Model):
    jono = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=60)
    num = models.CharField(max_length=27)
    wc = models.IntegerField()
    ta = models.IntegerField()
    lc = models.IntegerField()
    bo = models.IntegerField()
    fs = models.CharField(max_length=90)
    ls = models.CharField(max_length=90)
    date = models.DateField()
    test_date = models.DateField()
    ctc = models.IntegerField()
    suspence_bill_no = models.IntegerField()
    class Meta:
        db_table = u'suspence'

class TaDa(models.Model):
    id = models.IntegerField(primary_key=True)
    jono = models.IntegerField()
    g_departure_t = models.TextField() # This field type is a guess.
    g_arrival_t = models.TextField() # This field type is a guess.
    b_departure_t = models.TextField() # This field type is a guess.
    b_arrival_t = models.TextField() # This field type is a guess.
    fts1 = models.CharField(max_length=60)
    fts2 = models.CharField(max_length=60)
    fts3 = models.CharField(max_length=60)
    fts4 = models.CharField(max_length=60)
    fts5 = models.CharField(max_length=60)
    fts6 = models.CharField(max_length=60)
    fts7 = models.CharField(max_length=60)
    fts8 = models.CharField(max_length=60)
    fts9 = models.CharField(max_length=60)
    fts10 = models.CharField(max_length=60)
    tada_amount = models.IntegerField()
    reach_site = models.CharField(max_length=60)
    test_date = models.DateField()
    class Meta:
        db_table = u'ta_da'

class Teachers(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=300)
    da = models.CharField(max_length=30)
    position = models.CharField(max_length=150)
    class Meta:
        db_table = u'teachers'

class TileBricks(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'tile_bricks'

class TileChipps(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'tile_chipps'

class TileUnglazed(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'tile_unglazed'

class Transport(models.Model):
    id = models.IntegerField(primary_key=True)
    jono = models.IntegerField()
    bill_no = models.IntegerField()
    kilometer = models.CharField(max_length=150)
    rate = models.IntegerField()
    amount = models.CharField(max_length=180)
    total = models.IntegerField()
    date = models.DateField()
    test_date = models.CharField(max_length=300)
    class Meta:
        db_table = u'transport'

class Wood(models.Model):
    serial = models.IntegerField(primary_key=True)
    jobno = models.IntegerField(unique=True)
    date = models.DateField()
    no_samples = models.IntegerField(db_column='No_Samples') # Field name made lowercase.
    rate = models.FloatField(db_column='Rate') # Field name made lowercase.
    total = models.IntegerField(db_column='Total') # Field name made lowercase.
    class Meta:
        db_table = u'wood'

