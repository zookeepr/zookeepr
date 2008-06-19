"""
import sys

class MiniProposalSchema(BaseSchema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = ProposalTypeValidator()
    assistance = AssistanceTypeValidator()
    #project = validators.String(not_empty=True)
    url = validators.String()
    #abstract_video_url = validators.String()

class NewMiniProposalSchema(BaseSchema):
    person = NewMiniPersonSchema()
    proposal = MiniProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]

class ExistingMiniProposalSchema(BaseSchema):
    person = ExistingMiniPersonSchema()
    proposal = MiniProposalSchema()
    attachment = FileUploadValidator()
    pre_validators = [NestedVariables]


class CfpController(SecureController):
    #permissions removed since submit* displays appropirate template file upon closed/not_open settings.
    permissions = {
      'index': True,
    }

    def index(self):
        return render_response("cfp/list.myt")
"""
