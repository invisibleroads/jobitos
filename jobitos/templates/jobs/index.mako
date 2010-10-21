<%inherit file="/base.mako"/>

<%def name="title()">Jobs</%def>

<%def name="toolbar()">
% if h.isPersonSuper():
<a class=linkOFF href="${h.url('job_register')}">Register job</a>
% endif
</%def>

<table class=maximumWidth>
% for job in c.jobs:
    <tr>
        <td>${h.getWhenIO().format(job.when_updated)}</td>
        <td>${job.title}</td>
        <td>${job.owner.nickname}</td>
        <td>$${job.budget}</td>
    </tr>
% endfor
</table>
