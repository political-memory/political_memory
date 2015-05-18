from .models import Dossier

def export_all_dossiers():
    return [export_a_dossier(dossier) for dossier in Dossier.objects.all()]

def export_a_dossier(dossier):
    ret = {'dossier': {
        'title': dossier.title,
        'reference': dossier.reference,
        'text': dossier.text
    }}

    ret['proposals'] = [export_a_proposal(proposal) for proposal in dossier.proposal_set.all()]
           
    return ret

def export_a_proposal(proposal):
    ret = {
        'title': proposal.title,
        'reference': proposal.reference,
        'description': proposal.description,
        'date': proposal.datetime.isoformat(),
        'total_abstain': proposal.total_abstain,
        'total_against': proposal.total_against,
        'total_for': proposal.total_for
    }

    ret['votes'] = [export_a_vote(vote) for vote in proposal.vote_set.all()]
    return ret

def export_a_vote(vote):
    return {
        'representative': vote.representative_remote_id,
        'postion': vote.position
    }
