from faker import Faker
from django.core.management import BaseCommand
import faker.providers
import datetime
from RY_Enquiry_Form.models import RY_Enquiry_Items, RY_Enquiry_Header

# dummy data
agent = ['malika.tahseen@gmail.com', 'ardorbytes@gmail.com']

buyer = ['logeshwari.m.k@weeroda.com', 'spacerockbot@gmail.com']

count = ['20s', '30s']
blend = ['100% cotton', '40%polly', '30% bamboo']
shade = ['red', 'green', 'black', 'purple', 'pink']
qlt = ['light', 'strong', 'elastic']
typ = ['Melange', 'Kora-Cotton Yarn']
ref = ['#jsdofjewo', '#ndjfwsodjew', '#jfhwkjhw']
dep = ['light', 'dark', 'strong']
mil = ['royalyarns', 'vardhman', 'XYRoyalMill']


class Provider(faker.providers.BaseProvider):
    def createagent(self):
        return self.random_element(agent)

    def createbuyer(self):
        return self.random_element(buyer)

    def createcount(self):
        return self.random_element(count)

    def createblend(self):
        return self.random_element(blend)

    def createshade(self):
        return self.random_element(shade)

    def createquality(self):
        return self.random_element(qlt)

    def createtype(self):
        return self.random_element(typ)

    def createshaderef(self):
        return self.random_element(ref)

    def createdepth(self):
        return self.random_element(dep)

    def createmil(self):
        return self.random_element(mil)


class Command(BaseCommand):
    help = "ask me for any help - i will come and fall at your feet"

    def add_arguments(self, parser):
        parser.add_argument('reg_start_index')
        parser.add_argument('totalEnq')

    def handle(self, *args, **options):

        reg_start_index = int(options['reg_start_index'])
        totalEnq = int(options['totalEnq'])

        fake = Faker()
        fake.add_provider(Provider)
        # print(fake.name())

        for i in range(reg_start_index, totalEnq):
            # this is for items
            coun = fake.createcount()
            Quality = fake.createquality()
            Type = fake.createtype()
            blends = fake.createblend()
            shd = fake.createshade()
            Shde_Ref = fake.createshaderef()
            Dept = fake.createdepth()
            unitom = "kg"
            sts = '0'
            Supplier_Rate = fake.random_int(10000, 50000)
            Supplier_Amount = fake.random_int(20000, 40000)
            agents = fake.createagent()
            buyers = fake.createbuyer()
            Agent_Rate = fake.random_int(30000, 60000)
            Agent_Amount = fake.random_int(50000, 90000)
            qtn = fake.random_int(100, 5000)
            startdate = datetime.date(year=2022, month=1, day=1)
            enddate = datetime.date(year=2022, month=12, day=31)
            dates = fake.date_between(start_date=startdate, end_date=enddate)
            # this is for header
            mils = fake.createmil()
            cus = fake.name()
            ptm = 'cash'
            emml = '[Demo Email] /r/n Dear sir\r\n\r\n\r\n\xa0\r\n\r\n\r\nKindly advise the price and lead time for the below\r\n\r\n\r\n\xa0\r\n\r\n\r\n1)\xa0\xa0\xa0\xa0\xa0 24s 60%BCI Cotton 40%Poly -10000 Kgs\r\n\r\n\r\n\xa0\r\n\r\n\r\n2)\xa0\xa0\xa0\xa0\xa0 42s 45%Bamboo 55%Cotton Compact spn-40000 Kgs\r\n\r\n\r\n\xa0\r\n\r\n\r\n\r\n\r\n'
            mrtzone = fake.country()

            ##table, columns

            RY_Enquiry_Items.objects.create(
                Counts=coun,
                Quality=Quality,
                Type=Type,
                Blend=blends,
                Shade=shd,
                Shade_Ref=Shde_Ref,
                Depth=Dept,
                UOM=unitom,
                Quantity=qtn,
                Status=sts,
                Reg_no=i,
                Agent_Last_order=dates,
                CreatedByUser=buyers,
                LastUpdateby=agents,
                LastUpdateddate=dates,

            )

            RY_Enquiry_Header.objects.create(
                Reg_no=i,
                Mill=mils,
                Customer=cus,
                Marketing_Zone=mrtzone,
                Payment_Term=ptm,
                Date=dates,
                Email_Details=emml,
                Status=sts,
                CreatedByUser=buyers,
                LastUpdateby=agents,
                LastUpdateddate=dates,
            )
