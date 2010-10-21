'Jobs controller'
# Import pylons modules
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify
# Import system modules
import logging; log = logging.getLogger(__name__)
import datetime
import sqlalchemy.orm as orm
import formencode
import formencode.validators
# Import custom modules
from jobitos import model
from jobitos.model import Session
from jobitos.config import parameter
from jobitos.lib import helpers as h
from jobitos.lib.base import BaseController, render


class JobsController(BaseController):

    def index(self):
        'Show information about jobs registered in the database'
        c.jobs = Session.query(model.Job).options(orm.eagerload(model.Job.owner)).order_by(model.Job.when_updated.desc()).all()
        return render('/jobs/index.mako')

    def register(self):
        'Show job registration page'
        # If the user is not a superuser,
        if not h.isPersonSuper():
            c.message = 'You must be logged in as a superuser to register jobs'
            return render('/jobs/err.mako')
        # Return
        c.isNew = True
        return render('/jobs/change.mako')

    @jsonify
    def register_(self):
        'Store proposed changes'
        # If the user is not a superuser,
        if not h.isPersonSuper():
            return dict(isOk=0, message='You must be logged in as a superuser to register jobs')
        # Return
        return changeJob(dict(request.POST), h.getPersonID())

    def show(self, jobID):
        'Show specific job'
        c.job = Session.query(model.Job).options(orm.eagerload(model.Job.owner)).get(jobID)
        c.jobID = jobID
        return render('/jobs/show.mako')


# Helpers

def changeJob(valueByName, ownerID, job=None):
    'Validate values and send confirmation email if values are okay'
    try:
        # Validate form
        form = JobForm().to_python(valueByName, job)
    except formencode.Invalid, error:
        return dict(isOk=0, errorByID=error.unpack_errors())
    # If the job does not exist, add it
    if not job:
        job = model.Job()
        Session.add(job)
    # Set fields
    job.title = form['title'].strip()
    job.budget = form['budget']
    job.description = form['description'].strip()
    job.when_updated = datetime.datetime.utcnow()
    job.owner_id = ownerID
    # Commit
    Session.commit()
    # Return
    return dict(isOk=1, jobID=job.id)


# Validators

class Unique(formencode.validators.FancyValidator):
    'Validator to ensure unique values in a field'

    def __init__(self, fieldName, errorMessage):
        'Store fieldName and errorMessage'
        super(Unique, self).__init__()
        self.fieldName = fieldName
        self.errorMessage = errorMessage

    def _to_python(self, value, job):
        'Check whether the value is unique'
        # If the job is new or the value changed,
        if not job or getattr(job, self.fieldName) != value:
            # Make sure the value is unique
            if Session.query(model.Job).filter(getattr(model.Job, self.fieldName)==value).first():
                # Raise
                raise formencode.Invalid(self.errorMessage, value, job)
        # Return
        return value

class JobForm(formencode.Schema):
    'Validate job credentials'

    title = formencode.All(
        formencode.validators.UnicodeString(
            min=parameter.TITLE_LENGTH_MINIMUM, 
            max=parameter.TITLE_LENGTH_MAXIMUM,
        ),
        Unique('title', 'That title already exists'),
    )
    budget = formencode.All(
        formencode.validators.Int(
            min=parameter.BUDGET_MINIMUM,
            not_empty=True,
        ), 
    )
    description = formencode.All(
        formencode.validators.UnicodeString(
            min=parameter.DESCRIPTION_LENGTH_MINIMUM,
        ),
        Unique('description', 'That description already exists'),
    )
