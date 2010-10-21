<%inherit file="/base.mako"/>

<%def name="title()">Account ${'Registration' if c.isNew else 'Update'}</%def>

<%def name="js()">
function getMessageObj(id) { return $('#m_' + id); }
var ids = ['title', 'description', 'budget'];
var defaultByID = {};
for (var i=0; i<ids.length; i++) {
    var id = ids[i];
    defaultByID[id] = getMessageObj(id).html();
}
function showFeedback(messageByID) {
    for (var i = 0; i < ids.length; i++) {
        var id = ids[i];
        var o = getMessageObj(id);
        if (messageByID[id]) {
            o.html('<b>' + messageByID[id] + '</b>');
        } else {
            o.html(defaultByID[id]);
        }
    }
}
$('#buttonSave').click(function() {
    // Get
    var title = $('#title').val(),
        description = $('#description').val(), 
        budget = $('#budget').val();
    // Lock
    $('.lockOnSave').attr('disabled', 'disabled');
    // Post
    $.post("${h.url('job_register_' if c.isNew else 'job_update_')}", {
        title: title,
        description: description,
        budget: budget
    }, function(data) {
        if (data.isOk) {
            window.location = "${h.url('job_show', jobID='XXX')}".replace('XXX', data.jobID);
        } else {
            $('.lockOnSave').removeAttr('disabled');
            messageByID = data.errorByID;
        }
        showFeedback(messageByID);
    }, 'json');
});
$('#title').focus();
</%def>

<%def name="toolbar()">
${'Register job' if c.isNew else 'Update job'}
</%def>

<label for=title>What is the job?</label>&nbsp; <span id=m_title></span><br>
<input id=title name=title class="lockOnSave maximumWidth" autocomplete=off><br>
<br>

<label for=budget>How much are you willing to spend?</label>&nbsp; <span id=m_budget></span><br>
<input id=budget name=budget class="lockOnSave maximumWidth" autocomplete=off><br>
<br>

<label for=description>Who? What? Where? When? Why?</label>&nbsp; <span id=m_description></span><br>
<textarea id=description name=description class="lockOnSave maximumWidth" rows=20></textarea><br>
<br>

<input id=buttonSave class=lockOnSave type=button value="${'Register' if c.isNew else 'Update'}">
