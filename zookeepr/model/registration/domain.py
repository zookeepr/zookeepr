import datetime

class Registration(object):
    def __init__(self,
                 nick=None,
                 shell=None,
                 shelltext=None,
                 editor=None,
                 editortext=None,
                 distro=None,
                 distrotext=None,
                 silly_description=None,
                 voucher_code=None,
                 diet=None,
                 special=None,
                 volunteer=None,
                 opendaydrag=None,
                 partner_email=None,
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
        self.nick = nick
        self.shell = shell
        self.shelltext = shelltext
        self.editor = editor
        self.editortext = editortext
        self.distro = distro
        self.distrotext = distrotext
        self.silly_description = silly_description
        self.voucher_code = voucher_code
        self.diet = diet
        self.special = special
        self.volunteer = volunteer
        self.opendaydrag = opendaydrag
        self.partner_email = partner_email
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


class RegistrationProduct(object):
    def __init__(self, qty=0):
        self.qty = qty

    def __repr__(self):
        return '<RegistrationProduct registration_id=%r product_id=%r qty=%r>' % (self.registration_id, self.product_id, self.qty)

class RegoNote(object):
    def __init__(self, note=None):
        self.note = note

    def __repr__(self):
        return '<RegoNote note=%r>' % (self.note)

