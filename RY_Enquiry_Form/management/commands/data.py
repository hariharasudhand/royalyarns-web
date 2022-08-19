from faker import Faker
from django.core.management import BaseCommand
import faker.providers
import datetime
from RY_Enquiry_Form.models import RY_Enquiry_Items, RY_Enquiry_Header

# dummy data
agent = ['aishu', 'abi', 'agent1', 'agent2',
         'agent3', 'agent4', 'agent5', 'agent6', ]
count = ['20s', '30s', '70s', '10s', '40s', '100s', '80s', '50s', '60s', ]
blend = ['100% cotton', '40%polly', '30% bamboo']
shade = ['red', 'green', 'black', 'purple', 'pink']
qlt = ['light', 'strong', 'elastic']
typ = ['lycra', 'organic', 'pure', 'mixed']
ref = ['#jsdofjewo', '#ndjfwsodjew', '#jfhwkjhw']
dep = ['light', 'dark', 'strong']
mil = ['royalyarns', 'varthamam', 'legend']


class Provider(faker.providers.BaseProvider):
    def createagent(self):
        return self.random_element(agent)

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
    help = "data nu podu"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)
        # print(fake.name())

        for i in range(1, 201):
            # this is for items
            coun = fake.createcount()
            Quality = fake.createquality()
            Type = fake.createtype()
            blends = fake.createblend()
            shd = fake.createshade()
            Shde_Ref = fake.createshaderef()
            Dept = fake.createdepth()
            unitom = "kg"
            sts = fake.random_int(-1, 14)
            Supplier_Rate = fake.random_int(10000, 50000)
            Supplier_Amount = fake.random_int(20000, 40000)
            agents = fake.createagent()
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
            emml = fake.email()
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
                CreatedByUser=agents,
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
                CreatedByUser=agents,
                LastUpdateby=agents,
                LastUpdateddate=dates,
            )
