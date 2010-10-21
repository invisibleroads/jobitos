<%inherit file="/base.mako"/>

<%def name="title()">
Job ${c.jobID}
</%def>

% if c.job:
${c.job.title}
<br><br>
$${c.job.budget}
<br><br>
${c.job.owner.nickname}
<br><br>
${h.getWhenIO().format(c.job.when_updated)}
<br><br>
${c.job.description}
% else:
Job ${c.jobID} does not exist
% endif
