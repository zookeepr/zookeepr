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
        self.checkin = checkin
        self.checkout = checkout
        self.lasignup = lasignup
        self.announcesignup = announcesignup
        self.delegatesignup = delegatesignup
        self.prevlca = prevlca
        self.miniconf = miniconf

    def __repr__(self):
        return '<Registration id=%r type=%r person_id=%r>' % (self.id, self.type, self.person_id)


class AccommodationLocation(object):
    def __init__(self, name=None, beds=None):
        self.name = name
        self.beds = beds

    def __repr__(self):
        return '<AccommodationLocation name=%r beds=%r>' % (self.name, self.beds)


class AccommodationOption(object):
    def __init__(self, name=None, cost_per_night=None, location=None):
        self.name = name
        self.cost_per_night = cost_per_night
        self.location = None

    def __repr__(self):
        return '<AccommodationOption name=%r cost_per_night=%r location=%r>' % (self.name, self.cost_per_night, self.location)


class Accommodation(object):
    """Read-only object for referring to accommodation."""
    
    def get_available_beds(self):
        """Return the number of beds not yet claimed."""
        return self.beds - self.beds_taken

    def __repr__(self):
        return '<Accommodation name=%r option=%r beds=%d available_beds=%d cost_per_night=%r>' % (self.name, self.option, self.beds, self.get_available_beds(), self.cost_per_night)
