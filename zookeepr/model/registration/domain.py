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
                 nick=None,
                 shell=None,
                 shelltext=None,
                 editor=None,
                 editortext=None,
                 distro=None,
                 distrotext=None,
                 silly_description=None,
                 type=None,
                 voucher_code=None,
                 teesize=None,
                 extra_tee_count=None,
                 extra_tee_sizes=None,
                 dinner=None,
                 diet=None,
                 special=None,
                 volunteer=None,
                 opendaydrag=None,
                 partner_email=None,
                 kids_0_3=None,
                 kids_4_6=None,
                 kids_7_9=None,
                 kids_10_11=None,
                 kids_12_17=None,
                 pp_adults=None,
                 speaker_pp_pay_adult=None,
                 speaker_pp_pay_child=None,
                 checkin=None,
                 checkout=None,
                 lasignup=None,
		 speaker_record=None,
		 speaker_video_release=None,
		 speaker_slides_release=None,
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
        self.nick = nick
        self.shell = shell
        self.shelltext = shelltext
        self.editor = editor
        self.editortext = editortext
        self.distro = distro
        self.distrotext = distrotext
        self.silly_description = silly_description
        self.type = type
        self.voucher_code = voucher_code
        self.teesize = teesize
        self.extra_tee_count = extra_tee_count
        self.extra_tee_sizes = extra_tee_sizes
        self.dinner = dinner
        self.diet = diet
        self.special = special
        self.volunteer = volunteer
        self.opendaydrag = opendaydrag
        self.partner_email = partner_email
        self.kids_0_3 = kids_0_3
        self.kids_4_6 = kids_4_6
        self.kids_7_9 = kids_7_9
        self.kids_10_11=kids_10_11,
        self.kids_12_17=kids_12_17,
        self.pp_adults=pp_adults,
        self.speaker_pp_pay_adult=speaker_pp_pay_adult,
        self.speaker_pp_pay_child=speaker_pp_pay_child,
        self.checkin = checkin
        self.checkout = checkout
        self.lasignup = lasignup
	self.speaker_record = speaker_record
	self.speaker_video_release = speaker_video_release 
	self.speaker_slides_release = speaker_slides_release 
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

class RegoNote(object):
    def __init__(self, note=None):
        self.note = note

    def __repr__(self):
        return '<RegoNote note=%r>' % (self.note)

