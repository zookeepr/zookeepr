import datetime

class Registration(object):
    def __init__(self,
                 address1=None,
                 address2=None,
                 city=None,
                 state=None,
                 country=None,
                 postcode=None,
                 phone=None,
                 company=None,
                 shell=None,
                 shelltext=None,
                 editor=None,
                 editortext=None,
                 distro=None,
                 distrotext=None,
                 silly_description=None,
                 type=None,
                 discount_code=None,
                 teesize=None,
                 dinner=None,
                 diet=None,
                 special=None,
                 opendaydrag=None,
                 partner_email=None,
                 kids_0_3=None,
                 kids_4_6=None,
                 kids_7_9=None,
                 kids_10=None,
                 accommodation=None,
                 checkin=None,
                 checkout=None,
                 lasignup=None,
                 announcesignup=None,
                 delegatesignup=None,
                 prevlca=None,
                 miniconf=None,
                 ):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.country = country
        self.postcode = postcode
        self.phone = phone
        self.company = company
        self.shell = shell
        self.shelltext = shelltext
        self.editor = editor
        self.editortext = editortext
        self.distro = distro
        self.distrotext = distrotext
        self.silly_description = silly_description
        self.type = type
        self.discount_code = discount_code
        self.teesize = teesize
        self.dinner = dinner
        self.diet = diet
        self.special = special
        self.opendaydrag = opendaydrag
        self.partner_email = partner_email
        self.kids_0_3 = kids_0_3
        self.kids_4_6 = kids_4_6
        self.kids_7_9 = kids_7_9
        self.kids_10 = kids_10
        self.accommodation = accommodation
        self.checkin = checkin
        self.checkout = checkout
        self.lasignup = lasignup
        self.announcesignup = announcesignup
        self.delegatesignup = delegatesignup
        self.prevlca = prevlca
        self.miniconf = miniconf


class Accommodation(object):
    def __init__(self, name, option, cost_per_night, beds):
        self.name = name
        self.option = option
        self.cost_per_night = cost_per_night
        self.beds = beds
